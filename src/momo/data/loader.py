"""High-level data loading orchestrator.

This module coordinates fetching data from Norgate (via bridge) or cache,
with validation.

The loader implements a cache-first strategy:
1. Check if cached Parquet exists for the given universe and date range
2. If cache exists (and not force_refresh), return cached data
3. If cache misses (or force_refresh=True), fetch from bridge and save to cache

See docs/architecture/components.md for detailed component specification.
"""

from datetime import date
from time import perf_counter

import pandas as pd
import structlog

from momo.data import bridge, cache
from momo.utils.exceptions import (
    NDUNotRunningError,
    NorgateBridgeError,
    WindowsPythonNotFoundError,
)

logger = structlog.get_logger()


def load_universe(
    symbols: list[str],
    start_date: date,
    end_date: date,
    universe: str,
    force_refresh: bool = False,
) -> pd.DataFrame:
    """Load price data for a universe of symbols with cache-first orchestration.

    This function implements the core data loading workflow:
    1. Check cache unless force_refresh=True
    2. If cache hit, return cached data immediately
    3. If cache miss, fetch data from Norgate via bridge for each symbol
    4. Handle partial failures gracefully (continue with remaining symbols)
    5. Save successfully fetched data to cache (partial results if some failed)
    6. Return the DataFrame with available data

    DataFrame Schema (Output):
        Index:
            - MultiIndex (date: datetime64[ns], symbol: str)
        Columns:
            - open (float64): Opening price (adjusted)
            - high (float64): High price (adjusted)
            - low (float64): Low price (adjusted)
            - close (float64): Closing price (adjusted)
            - volume (int64): Trading volume
            - unadjusted_close (float64): Raw close for reference
            - dividend (float64): Dividend amount (TOTALRETURN adjustment)

    Args:
        symbols: List of ticker symbols to fetch (e.g., ["AAPL", "MSFT"])
        start_date: Start date for price data range
        end_date: End date for price data range
        universe: Universe identifier for cache naming (e.g., "russell_1000_cp")
        force_refresh: If True, bypass cache and fetch fresh data (default: False)

    Returns:
        DataFrame with price data for all symbols, MultiIndex (date, symbol)

    Raises:
        ValueError: If all symbols fail to fetch (logs partial failures as warnings)
        CacheError: If cache save operation fails

    Note on Error Handling:
        Individual symbol fetch failures are logged but do not stop execution.
        The function continues fetching remaining symbols and caches partial
        results. Only if ALL symbols fail does the function raise ValueError.

    Example:
        >>> df = load_universe(
        ...     symbols=["AAPL", "MSFT", "GOOGL"],
        ...     start_date=date(2020, 1, 1),
        ...     end_date=date(2020, 12, 31),
        ...     universe="test_universe"
        ... )
        >>> df.index.names
        ['date', 'symbol']
        >>> df.columns.tolist()
        ['open', 'high', 'low', 'close', 'volume', 'unadjusted_close', 'dividend']

    Note:
        This implementation uses sequential single-symbol fetching. Batch
        fetching optimization is deferred to a future story for improved
        performance (~10x speedup expected).
    """
    # Step 1: Try cache first (unless force_refresh)
    if not force_refresh:
        cached_df = cache.load_prices(
            universe=universe,
            start_date=start_date,
            end_date=end_date,
        )
        if cached_df is not None:
            logger.info(
                "cache_hit",
                universe=universe,
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat(),
                symbols_count=len(symbols),
            )
            return cached_df
        # Cache miss - log and proceed to fetch
        logger.info(
            "cache_miss",
            universe=universe,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            symbols_count=len(symbols),
        )
    else:
        # Force refresh - log and proceed to fetch
        logger.info(
            "cache_refresh",
            universe=universe,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            symbols_count=len(symbols),
            reason="force_refresh",
        )

    # Step 2: Fetch from bridge
    # Log start of fetch operation
    start_time = perf_counter()
    logger.info(
        "fetching_universe",
        symbols_count=len(symbols),
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat(),
        universe=universe,
    )

    # Step 3: Fetch data for each symbol sequentially
    # Note: Batch optimization deferred to future story
    symbol_dfs: list[pd.DataFrame] = []
    failed_symbols: list[tuple[str, Exception]] = []

    for i, symbol in enumerate(symbols, start=1):
        logger.info(
            "fetching_symbol",
            symbol=symbol,
            index=i,
            total=len(symbols),
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
        )

        try:
            symbol_df = bridge.fetch_price_data(
                symbol=symbol,
                start_date=start_date,
                end_date=end_date,
                adjustment="TOTALRETURN",
                timeout=30,
            )
            symbol_dfs.append(symbol_df)
        except (
            NDUNotRunningError,
            WindowsPythonNotFoundError,
            NorgateBridgeError,
        ) as e:
            logger.error(
                "symbol_fetch_failed",
                symbol=symbol,
                error=str(e),
                error_type=type(e).__name__,
            )
            failed_symbols.append((symbol, e))
            continue  # Continue fetching remaining symbols

    # Log partial failure if some symbols failed
    if failed_symbols:
        logger.warning(
            "partial_fetch_failure",
            failed_count=len(failed_symbols),
            successful_count=len(symbol_dfs),
            failed_symbols=[sym for sym, _ in failed_symbols],
            total_requested=len(symbols),
        )

    # Step 4: Combine all symbol DataFrames
    if not symbol_dfs:
        # All symbols failed - raise error with details
        if failed_symbols:
            raise ValueError(
                f"All {len(symbols)} symbols failed to fetch. "
                f"Failed symbols: {[sym for sym, _ in failed_symbols]}"
            )
        # No symbols provided (edge case)
        raise ValueError("No symbols provided to load_universe")

    # Concatenate all symbol DataFrames
    # Bridge returns DataFrames with date index and symbol column (not in index)
    combined_df = pd.concat(symbol_dfs, axis=0)

    # Create MultiIndex (date, symbol)
    # The date is currently the index, symbol is a column
    # We need to move both to the index to create MultiIndex
    if "symbol" in combined_df.columns:
        combined_df = combined_df.set_index("symbol", append=True)
        # After set_index with append=True, index is (date, symbol) which is correct
        # No need to swap levels
    else:
        # If symbol not in columns (shouldn't happen), it might already be in index
        # In that case, do nothing - the MultiIndex is already correct
        pass

    # Step 5: Save to cache
    cache.save_prices(
        df=combined_df,
        universe=universe,
        start_date=start_date,
        end_date=end_date,
    )

    # Log completion with duration
    elapsed = perf_counter() - start_time
    logger.info(
        "universe_fetched",
        universe=universe,
        symbols_count=len(symbols),
        rows=len(combined_df),
        duration=elapsed,
    )

    return combined_df
