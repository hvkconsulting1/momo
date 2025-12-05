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

import pandas as pd
import structlog

from momo.data import bridge, cache

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
    4. Save fetched data to cache
    5. Return the complete DataFrame

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
        NDUNotRunningError: If Norgate Data Updater is not running
        WindowsPythonNotFoundError: If Windows Python not found in PATH
        NorgateBridgeError: If bridge communication fails
        CacheError: If cache save operation fails

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

    # Step 2: Cache miss - fetch from bridge
    logger.info(
        "cache_miss",
        universe=universe,
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat(),
        symbols_count=len(symbols),
    )

    # Step 3: Fetch data for each symbol sequentially
    # Note: Batch optimization deferred to future story
    symbol_dfs: list[pd.DataFrame] = []

    for symbol in symbols:
        logger.info(
            "fetching_symbol",
            symbol=symbol,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
        )

        symbol_df = bridge.fetch_price_data(
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            adjustment="TOTALRETURN",
        )
        symbol_dfs.append(symbol_df)

    # Step 4: Combine all symbol DataFrames
    if not symbol_dfs:
        # Handle empty list (no symbols)
        raise ValueError("No symbols provided to load_universe")

    combined_df = pd.concat(symbol_dfs, axis=0)

    # Step 5: Save to cache
    cache.save_prices(
        df=combined_df,
        universe=universe,
        start_date=start_date,
        end_date=end_date,
    )

    logger.info(
        "universe_loaded",
        universe=universe,
        symbols_count=len(symbols),
        rows=len(combined_df),
    )

    return combined_df
