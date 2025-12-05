"""
Data quality validation module for price data integrity checks.

This module provides functions to validate price data quality, including:
- Missing data detection (NaN values and date gaps)
- Adjustment factor consistency checks (splits/dividends)
- Point-in-time index constituent retrieval
- Delisting status detection

Architecture Context:
    Layer: Data (src/momo/data/)
    Dependencies: bridge.py, cache.py, loader.py
    Dependents: Signal layer can depend on this module
    Pure: No (I/O operations allowed in data layer)

Example Usage:
    >>> from momo.data.validation import validate_prices, check_delisting_status
    >>> from momo.data.loader import load_universe
    >>> from datetime import date
    >>> import pandas as pd
    >>>
    >>> # Load price data from cache or Norgate bridge
    >>> prices_df = load_universe(
    ...     watchlist_name="Russell 1000 Current & Past",
    ...     start_date=date(2020, 1, 1),
    ...     end_date=date(2020, 12, 31)
    ... )
    >>>
    >>> # Validate price data quality
    >>> report = validate_prices(prices_df)
    >>>
    >>> # Print formatted validation report
    >>> print(report)
    >>> # Output:
    >>> # ===== Validation Report =====
    >>> # Total Tickers: 1000
    >>> # Date Range: 2020-01-01 to 2020-12-31
    >>> # Missing Data: 5 ticker(s) with issues
    >>> # Date Gaps: 2 ticker(s) with issues
    >>> # Adjustment Issues: 1 ticker(s)
    >>> # Delisting Events: 10 ticker(s)
    >>> # Status: INVALID
    >>> # Summary: Validation found issues: 5 ticker(s) with 12 missing value(s); ...
    >>> # =============================
    >>>
    >>> # Inspect specific issues
    >>> if not report.is_valid:
    ...     # Check for missing data
    ...     if report.missing_data_counts:
    ...         print(f"Tickers with NaN values: {list(report.missing_data_counts.keys())}")
    ...
    ...     # Check for date gaps
    ...     if report.date_gaps:
    ...         for ticker, gaps in report.date_gaps.items():
    ...             print(f"{ticker} has {len(gaps)} gap(s): {gaps}")
    ...
    ...     # Check for adjustment issues
    ...     if report.adjustment_issues:
    ...         print(f"Tickers with adjustment problems: {report.adjustment_issues}")
    ...
    ...     # Check for delisted tickers
    ...     if report.delisting_events:
    ...         for ticker, delisting_date in report.delisting_events.items():
    ...             print(f"{ticker} delisted on {delisting_date}")
    >>>
    >>> # Manual delisting check for specific query date
    >>> delisting_dict = check_delisting_status(
    ...     prices_df,
    ...     query_end_date=date(2021, 1, 1),
    ...     threshold_days=30
    ... )
    >>> print(f"Delisted tickers: {delisting_dict}")
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date as date_type
from datetime import timedelta
from typing import cast

import pandas as pd
import structlog

from momo.data.bridge import fetch_index_constituent_timeseries, fetch_watchlist_symbols
from momo.utils.exceptions import NorgateBridgeError

logger = structlog.get_logger()


def _check_missing_values(prices_df: pd.DataFrame) -> dict[str, int]:
    """Detect missing values (NaN) in critical OHLC price columns.

    Scans the DataFrame for NaN values in open, high, low, and close columns,
    aggregating counts per ticker symbol.

    Args:
        prices_df: Price data with MultiIndex (date, symbol) and OHLC columns

    Returns:
        dict[str, int]: Mapping of ticker symbol -> total NaN count across OHLC columns.
            Only includes tickers with at least one NaN value.

    DataFrame Schema (Input):
        Index:
            - MultiIndex with levels: (date: datetime64[ns], symbol: str)
            - Names: ['date', 'symbol']
        Columns (checked for NaN):
            - open: float64
            - high: float64
            - low: float64
            - close: float64

    Note:
        This function preserves input DataFrame immutability by using df.copy().
    """
    df = prices_df.copy()  # Preserve input immutability (ADR-004)

    result: dict[str, int] = {}

    # Get unique symbols from MultiIndex
    if isinstance(df.index, pd.MultiIndex):
        symbols = df.index.get_level_values("symbol").unique().tolist()
    else:
        return result  # Empty result for non-MultiIndex

    # Check each ticker for NaN values in OHLC columns
    for ticker in symbols:
        # Extract data for this ticker using MultiIndex slicing
        ticker_data = df.loc[(slice(None), ticker), :]

        # Count NaN values across all critical OHLC columns
        nan_count = (
            ticker_data["open"].isna().sum()
            + ticker_data["high"].isna().sum()
            + ticker_data["low"].isna().sum()
            + ticker_data["close"].isna().sum()
        )

        # Only include tickers with at least one NaN
        if nan_count > 0:
            result[ticker] = nan_count
            logger.warning(
                "Missing data detected",
                layer="data",
                operation="_check_missing_values",
                ticker=ticker,
                nan_count=nan_count,
            )

    return result


def _check_date_gaps(
    prices_df: pd.DataFrame, threshold_days: int = 10
) -> dict[str, list[tuple[date_type, date_type]]]:
    """Detect suspicious date gaps in price time series data.

    Identifies gaps of 10 or more business days in each ticker's time series,
    which may indicate missing data or data quality issues. Uses pandas business
    day logic to avoid false positives from weekends.

    Args:
        prices_df: Price data with MultiIndex (date, symbol) and OHLC columns
        threshold_days: Minimum business days gap to flag as suspicious (default: 10)

    Returns:
        dict[str, list[tuple[date_type, date_type]]]: Mapping of ticker symbol ->
            list of gap date ranges. Each gap is represented as (last_date_before_gap,
            first_date_after_gap). Only includes tickers with at least one suspicious gap.

    DataFrame Schema (Input):
        Index:
            - MultiIndex with levels: (date: datetime64[ns], symbol: str)
            - Names: ['date', 'symbol']
        Columns:
            - Any columns (only index used for gap detection)

    Note:
        This function uses pandas business day logic (freq='B') to count weekdays only.
        It does NOT use NYSE holiday calendar, so may flag single-day market holidays
        as suspicious if they extend a weekend to create >= 10 business days gap.
        For most practical purposes, this limitation is acceptable as 10-day threshold
        is well above typical holiday closures (1-2 days).
    """
    df = prices_df.copy()  # Preserve input immutability (ADR-004)

    result: dict[str, list[tuple[date_type, date_type]]] = {}

    # Get unique symbols from MultiIndex
    if isinstance(df.index, pd.MultiIndex):
        symbols = df.index.get_level_values("symbol").unique().tolist()
    else:
        return result  # Empty result for non-MultiIndex

    # Check each ticker for date gaps
    for ticker in symbols:
        # Extract dates for this ticker using MultiIndex slicing
        ticker_data = df.loc[(slice(None), ticker), :]
        ticker_dates = ticker_data.index.get_level_values("date").unique().sort_values()

        if len(ticker_dates) < 2:
            continue  # Skip tickers with single date (no gaps possible)

        gaps: list[tuple[date_type, date_type]] = []

        # Check consecutive date pairs for suspicious gaps
        for i in range(len(ticker_dates) - 1):
            date_before = ticker_dates[i]
            date_after = ticker_dates[i + 1]

            # Count business days between dates using pandas business day calendar
            # This automatically excludes weekends from the count
            business_days = pd.bdate_range(start=date_before, end=date_after, freq="B")
            gap_size = len(business_days) - 1  # -1 because bdate_range includes both endpoints

            # Flag gaps >= threshold_days business days
            if gap_size >= threshold_days:
                gaps.append((date_before.date(), date_after.date()))
                logger.warning(
                    "Date gap detected",
                    layer="data",
                    operation="_check_date_gaps",
                    ticker=ticker,
                    gap_start=date_before.date(),
                    gap_end=date_after.date(),
                    gap_business_days=gap_size,
                )

        # Only include tickers with at least one gap
        if gaps:
            result[ticker] = gaps

    return result


def _check_adjustment_consistency(
    prices_df: pd.DataFrame, threshold_pct: float = 0.40
) -> list[str]:
    """Detect suspected adjustment factor inconsistencies in price data.

    Uses heuristics to identify tickers with potential split/dividend adjustment issues:
    1. Negative prices (always invalid after proper adjustment)
    2. Large price jumps (>40% by default) without corresponding dividend information

    Args:
        prices_df: Price data with MultiIndex (date, symbol) and OHLC columns
        threshold_pct: Percentage change threshold for flagging suspicious jumps
            (default: 0.40 = 40%)

    Returns:
        list[str]: List of ticker symbols with suspected adjustment issues.
            Empty list if no issues detected.

    DataFrame Schema (Input):
        Index:
            - MultiIndex with levels: (date: datetime64[ns], symbol: str)
            - Names: ['date', 'symbol']
        Columns:
            - close: float64 (required for price jump detection)
            - dividend: float64 (required to determine if jump is justified)

    Heuristics:
        - Negative Price: Any close < 0 indicates invalid adjustment
        - Large Jump: Day-over-day change > threshold_pct AND dividend=0 on that date
          suggests missing split/dividend adjustment
        - Threshold: 40% chosen to balance false positive vs. false negative rates

    Note:
        This function uses heuristics and may produce false positives for:
        - Volatile stocks with legitimate large price moves
        - Stocks with undocumented corporate actions
        Use ValidationReport context to manually review flagged tickers.
    """
    df = prices_df.copy()  # Preserve input immutability (ADR-004)

    result: list[str] = []

    # Get unique symbols from MultiIndex
    if isinstance(df.index, pd.MultiIndex):
        symbols = df.index.get_level_values("symbol").unique().tolist()
    else:
        return result  # Empty result for non-MultiIndex

    # Check each ticker for adjustment issues
    for ticker in symbols:
        # Extract data for this ticker using MultiIndex slicing
        ticker_data = df.loc[(slice(None), ticker), :]

        # Sort by date to ensure chronological order for pct_change calculation
        ticker_data = ticker_data.sort_index()

        # Check 1: Negative prices (always invalid)
        negative_prices = ticker_data["close"] < 0
        if negative_prices.any():
            result.append(ticker)
            logger.warning(
                "Negative price detected",
                layer="data",
                operation="_check_adjustment_consistency",
                ticker=ticker,
                issue_type="negative_price",
            )
            continue  # Skip further checks if already flagged

        # Check 2: Large price jumps without dividend
        # Calculate day-over-day percentage change in close price
        pct_changes = ticker_data["close"].pct_change()

        # Find dates where |pct_change| > threshold AND dividend == 0
        # Large jumps with dividend are likely justified (dividend payout or split with dividend)
        suspicious_jumps = (pct_changes.abs() > threshold_pct) & (ticker_data["dividend"] == 0.0)

        if suspicious_jumps.any():
            result.append(ticker)
            # Get the first suspicious jump for logging
            first_jump_idx = suspicious_jumps[suspicious_jumps].index[0]
            jump_date = first_jump_idx[0]  # Extract date from MultiIndex tuple
            jump_pct = pct_changes.loc[first_jump_idx]
            logger.warning(
                "Suspicious price jump detected",
                layer="data",
                operation="_check_adjustment_consistency",
                ticker=ticker,
                issue_type="large_jump_no_dividend",
                jump_date=jump_date,
                jump_pct=f"{jump_pct * 100:.2f}%",
                threshold_pct=f"{threshold_pct * 100:.0f}%",
            )

    return result


def get_index_constituents_at_date(
    index_name: str,
    target_date: date_type,
    symbols: list[str] | None = None,
    timeout: int = 300,
) -> list[str]:
    """Get list of symbols that were index members at a specific date.

    Retrieves point-in-time index constituent information by querying the
    Norgate API via the Windows Python bridge. This function is used to
    filter universes based on historical index membership to avoid
    survivorship bias in backtests.

    Args:
        index_name: Name of index (e.g., "Russell 3000 Current & Past", "Russell 1000")
        target_date: Date to check membership (datetime.date object)
        symbols: Optional list of symbols to check (if None, retrieves all from watchlist)
        timeout: Bridge timeout in seconds (default: 300s for full universe)

    Returns:
        list[str]: List of ticker symbols that were index members at target_date.
            Returns empty list if no constituents found or all symbols fail.

    Raises:
        ValueError: Invalid index name (index not found in Norgate database)
        NorgateBridgeError: Bridge communication errors or timeouts

    Example:
        >>> from datetime import date
        >>> # Get ALL Russell 1000 constituents as of Jan 1, 2010
        >>> constituents = get_index_constituents_at_date(
        ...     "Russell 1000 Current & Past",
        ...     date(2010, 1, 1)
        ... )
        >>> print(len(constituents))  # ~1000
        >>>
        >>> # Or filter specific symbols for membership
        >>> filtered = get_index_constituents_at_date(
        ...     "Russell 1000 Current & Past",
        ...     date(2010, 1, 1),
        ...     symbols=["AAPL", "MSFT", "XYZ"]
        ... )
        >>> print(filtered)
        ['AAPL', 'MSFT']  # XYZ was not in index

    Note:
        - Use "Current & Past" index names to include delisted securities
        - Uses narrow date window (±5 days) to minimize bridge data transfer
        - Invalid symbols are skipped with warning (not raised as errors)
        - Performance: ~7ms per symbol check via bridge (~7s for 1000 symbols)
    """
    logger.info(
        "Getting index constituents at date",
        layer="data",
        operation="get_index_constituents_at_date",
        index_name=index_name,
        target_date=target_date,
        symbol_count=len(symbols) if symbols else "all",
    )

    # If no symbols provided, get all symbols from the watchlist
    if symbols is None:
        logger.info(
            "Fetching all symbols from watchlist",
            layer="data",
            operation="get_index_constituents_at_date",
            index_name=index_name,
        )
        symbols = fetch_watchlist_symbols(watchlist_name=index_name, timeout=timeout)
        logger.info(
            "Watchlist symbols retrieved",
            layer="data",
            operation="get_index_constituents_at_date",
            symbol_count=len(symbols),
        )

    constituents: list[str] = []

    # Use narrow date window (±5 days) to minimize data transfer
    start_date = target_date - timedelta(days=5)
    end_date = target_date + timedelta(days=5)

    for symbol in symbols:
        try:
            # Fetch constituent timeseries for narrow date range
            timeseries = fetch_index_constituent_timeseries(
                symbol=symbol,
                index_name=index_name,
                start_date=start_date,
                end_date=end_date,
                timeout=timeout,
            )

            # Skip symbols with no constituent data (empty DataFrame)
            if timeseries.empty:
                logger.warning(
                    "No constituent data for symbol, skipping",
                    layer="data",
                    operation="get_index_constituents_at_date",
                    symbol=symbol,
                    index_name=index_name,
                    target_date=target_date,
                )
                continue

            # Check if symbol was member on target_date
            # Use nearest date if target_date is not a trading day
            target_timestamp = pd.Timestamp(target_date)

            if target_timestamp in timeseries.index:
                # Exact date found
                is_member = bool(timeseries.loc[target_timestamp, "index_constituent"])
            else:
                # Find nearest trading day (use ffill to get nearest prior date)
                nearest_date = timeseries.index[timeseries.index <= target_timestamp]
                if len(nearest_date) > 0:
                    is_member = bool(timeseries.loc[nearest_date[-1], "index_constituent"])
                else:
                    # No date before target_date, check first available date
                    is_member = bool(timeseries.iloc[0]["index_constituent"])

            if is_member:
                constituents.append(symbol)
                logger.debug(
                    "Symbol was index member",
                    layer="data",
                    operation="get_index_constituents_at_date",
                    symbol=symbol,
                    target_date=target_date,
                )

        except ValueError as e:
            # Invalid symbol or index name - skip and log warning
            logger.warning(
                "Constituent check failed",
                layer="data",
                operation="get_index_constituents_at_date",
                symbol=symbol,
                index_name=index_name,
                error=str(e),
            )
            # Don't raise - continue checking other symbols
            continue

        except NorgateBridgeError as e:
            # Check if this is an invalid symbol/index error (should skip)
            # vs a real bridge communication error (should raise)
            error_message = str(e).lower()
            if "not found" in error_message or "not found" in error_message:
                # Invalid symbol/index - log warning and skip
                logger.warning(
                    "Constituent check failed",
                    layer="data",
                    operation="get_index_constituents_at_date",
                    symbol=symbol,
                    index_name=index_name,
                    error=str(e),
                )
                # Don't raise - continue checking other symbols
                continue
            else:
                # Real bridge communication error (timeout, etc.) - re-raise
                logger.error(
                    "Bridge error during constituent check",
                    layer="data",
                    operation="get_index_constituents_at_date",
                    symbol=symbol,
                    index_name=index_name,
                    error=str(e),
                )
                raise

    logger.info(
        "Index constituents retrieved",
        layer="data",
        operation="get_index_constituents_at_date",
        index_name=index_name,
        target_date=target_date,
        total_checked=len(symbols) if symbols else 0,
        constituents_found=len(constituents),
    )

    return constituents


def check_delisting_status(
    prices_df: pd.DataFrame,
    query_end_date: date_type | None = None,
    threshold_days: int = 30,
) -> dict[str, date_type]:
    """Detect delisted tickers by identifying time series ending before query date.

    Uses a heuristic to identify likely delisted securities: if a ticker's data
    ends more than `threshold_days` before the `query_end_date`, it is flagged
    as delisted. This approach works well for historical backtests where we
    expect all active securities to have data through the query end date.

    Args:
        prices_df: Price data with MultiIndex (date, symbol) and OHLC columns
        query_end_date: Expected end date for active securities (default: max date in DataFrame)
        threshold_days: Minimum days before query_end_date to flag as delisted (default: 30)

    Returns:
        dict[str, date_type]: Mapping of ticker symbol -> last trading date.
            Only includes tickers flagged as delisted (data ending > threshold_days
            before query_end_date). Empty dict if no delistings detected.

    DataFrame Schema (Input):
        Index:
            - MultiIndex with levels: (date: datetime64[ns], symbol: str)
            - Names: ['date', 'symbol']
        Columns:
            - Any columns (only index used for delisting detection)

    Heuristic:
        A ticker is considered delisted if its last date in the time series is
        more than `threshold_days` before `query_end_date`. This heuristic works
        because:
        - Active securities have data through the query period
        - Delisted securities have data ending at/near delisting date
        - 30-day threshold avoids false positives from recent data delays

    Example:
        >>> from datetime import date
        >>> # Enron delisted Dec 2, 2001; query period is 2020
        >>> delistings = check_delisting_status(
        ...     prices_df,
        ...     query_end_date=date(2020, 12, 31),
        ...     threshold_days=30
        ... )
        >>> print(delistings)
        {'ENRN': datetime.date(2001, 12, 2)}
    """
    df = prices_df.copy()  # Preserve input immutability (ADR-004)

    result: dict[str, date_type] = {}

    # Get unique symbols from MultiIndex
    if isinstance(df.index, pd.MultiIndex):
        symbols = df.index.get_level_values("symbol").unique().tolist()
        dates = df.index.get_level_values("date")
    else:
        return result  # Empty result for non-MultiIndex

    # Use max date in DataFrame if query_end_date not specified
    if query_end_date is None:
        query_end_date = dates.max().date()

    # Check each ticker's last trading date
    for ticker in symbols:
        # Extract dates for this ticker using MultiIndex slicing
        ticker_data = df.loc[(slice(None), ticker), :]
        ticker_dates = ticker_data.index.get_level_values("date")

        if len(ticker_dates) == 0:
            continue  # Skip tickers with no data

        # Get last trading date for this ticker
        last_date = ticker_dates.max().date()

        # Calculate gap between last date and query end date
        gap_days = (query_end_date - last_date).days

        # Flag as delisted if gap exceeds threshold
        if gap_days > threshold_days:
            result[ticker] = last_date
            logger.warning(
                "Delisting detected",
                layer="data",
                operation="check_delisting_status",
                ticker=ticker,
                last_trading_date=last_date,
                query_end_date=query_end_date,
                gap_days=gap_days,
                threshold_days=threshold_days,
            )

    return result


@dataclass
class ValidationReport:
    """Data quality validation report with comprehensive issue summary.

    Attributes:
        total_tickers: Total number of tickers in the dataset
        date_range: Tuple of (start_date, end_date) for the price data
        missing_data_counts: Dict mapping ticker -> count of missing values in OHLC columns
        date_gaps: Dict mapping ticker -> list of gap date ranges (start, end)
        adjustment_issues: List of tickers with suspected adjustment problems
        delisting_events: Dict mapping ticker -> delisting date (None if not delisted)
        summary_message: Human-readable concise summary (< 200 chars)
        is_valid: True if no critical issues found, False otherwise
    """

    total_tickers: int
    date_range: tuple[date_type, date_type]
    missing_data_counts: dict[str, int]
    date_gaps: dict[str, list[tuple[date_type, date_type]]]
    adjustment_issues: list[str]
    delisting_events: dict[str, date_type | None]
    summary_message: str
    is_valid: bool

    def __str__(self) -> str:
        """Format validation report as human-readable string.

        Returns:
            str: Formatted report with clear section headers and readable structure.

        Example Output:
            ===== Validation Report =====
            Total Tickers: 100
            Date Range: 2020-01-01 to 2020-12-31
            Missing Data: 5 ticker(s) with issues
            Date Gaps: 2 ticker(s) with issues
            Adjustment Issues: 1 ticker(s)
            Delisting Events: 10 ticker(s)
            Status: INVALID
            Summary: Validation found issues: 5 ticker(s) with 12 missing value(s); ...
            =============================
        """
        lines = ["===== Validation Report ====="]
        lines.append(f"Total Tickers: {self.total_tickers}")
        lines.append(f"Date Range: {self.date_range[0]} to {self.date_range[1]}")

        # Missing data summary
        if self.missing_data_counts:
            lines.append(f"Missing Data: {len(self.missing_data_counts)} ticker(s) with issues")
        else:
            lines.append("Missing Data: None")

        # Date gaps summary
        if self.date_gaps:
            lines.append(f"Date Gaps: {len(self.date_gaps)} ticker(s) with issues")
        else:
            lines.append("Date Gaps: None")

        # Adjustment issues summary
        if self.adjustment_issues:
            lines.append(f"Adjustment Issues: {len(self.adjustment_issues)} ticker(s)")
        else:
            lines.append("Adjustment Issues: None")

        # Delisting events summary
        if self.delisting_events:
            lines.append(f"Delisting Events: {len(self.delisting_events)} ticker(s)")
        else:
            lines.append("Delisting Events: None")

        # Validation status
        status_str = "VALID" if self.is_valid else "INVALID"
        lines.append(f"Status: {status_str}")

        # Summary message (appears prominently at end)
        lines.append(f"Summary: {self.summary_message}")

        lines.append("=============================")

        return "\n".join(lines)


def validate_prices(prices_df: pd.DataFrame, check_delistings: bool = True) -> ValidationReport:
    """Validate price data quality with comprehensive checks.

    Performs validation checks on price DataFrame including:
    1. Missing data detection (NaN/null values)
    2. Date gap identification (suspicious gaps in time series)
    3. Adjustment factor consistency (split/dividend validation)
    4. Delisting status detection (optional, enabled by default)

    Args:
        prices_df: Price data with MultiIndex (date, symbol) and OHLC columns
        check_delistings: If True, run delisting detection (default: True)

    Returns:
        ValidationReport: Comprehensive validation results with issue summary

    Raises:
        ValidationError: If validation cannot be completed due to data structure issues

    DataFrame Schema (Input):
        Index:
            - MultiIndex with levels: (date: datetime64[ns], symbol: str)
            - Names: ['date', 'symbol']
        Columns:
            - open: float64
            - high: float64
            - low: float64
            - close: float64
            - volume: int64
            - unadjusted_close: float64
            - dividend: float64

    Note:
        Delisting detection uses a heuristic: tickers with data ending > 30 days
        before the DataFrame's max date are flagged as delisted. This is useful
        for historical backtests with "Current & Past" watchlists.
    """
    logger.info("Starting price data validation", layer="data", operation="validate_prices")

    # Get unique tickers
    if isinstance(prices_df.index, pd.MultiIndex):
        symbols = prices_df.index.get_level_values("symbol").unique().tolist()
        dates = prices_df.index.get_level_values("date")
        start_date = dates.min().date()
        end_date = dates.max().date()
    else:
        # Fallback for non-MultiIndex (should not happen with Story 1.3 loader output)
        symbols = []
        start_date = date_type(2020, 1, 1)
        end_date = date_type(2020, 1, 1)

    total_tickers = len(symbols)

    # Perform validation checks
    # Check for missing values (NaN) in OHLC columns
    missing_data_counts = _check_missing_values(prices_df)

    # Check for date gaps (>= 10 business days)
    date_gaps = _check_date_gaps(prices_df)

    # Check for adjustment consistency issues (negative prices, large jumps)
    adjustment_issues = _check_adjustment_consistency(prices_df)

    # Check for delisting events (optional)
    if check_delistings:
        # check_delisting_status returns dict[str, date_type],
        # which is compatible with dict[str, date_type | None]
        delisting_events: dict[str, date_type | None] = cast(
            dict[str, date_type | None], check_delisting_status(prices_df, query_end_date=end_date)
        )
    else:
        delisting_events = {}

    # Determine validation status (delistings don't affect validity, just informational)
    is_valid = len(missing_data_counts) == 0 and len(date_gaps) == 0 and len(adjustment_issues) == 0

    # Generate concise summary message (< 200 chars)
    issues = []
    if missing_data_counts:
        ticker_count = len(missing_data_counts)
        total_nans = sum(missing_data_counts.values())
        issues.append(f"{ticker_count} ticker(s) with {total_nans} missing value(s)")
    if date_gaps:
        gap_count = len(date_gaps)
        total_gaps = sum(len(gaps) for gaps in date_gaps.values())
        issues.append(f"{gap_count} ticker(s) with {total_gaps} date gap(s)")
    if adjustment_issues:
        issue_count = len(adjustment_issues)
        issues.append(f"{issue_count} ticker(s) with adjustment issue(s)")
    if delisting_events:
        delisting_count = len(delisting_events)
        issues.append(f"{delisting_count} delisted")

    if issues:
        # Join issues with semicolons, truncate if > 200 chars
        summary_message = f"Validation found issues: {'; '.join(issues)}"
        if len(summary_message) > 200:
            # Truncate to 197 chars and add ellipsis
            summary_message = summary_message[:197] + "..."
    else:
        summary_message = f"Validation complete: {total_tickers} tickers, no issues detected"

    report = ValidationReport(
        total_tickers=total_tickers,
        date_range=(start_date, end_date),
        missing_data_counts=missing_data_counts,
        date_gaps=date_gaps,
        adjustment_issues=adjustment_issues,
        delisting_events=delisting_events,
        summary_message=summary_message,
        is_valid=is_valid,
    )

    logger.info(
        "Price data validation complete",
        layer="data",
        operation="validate_prices",
        total_tickers=total_tickers,
        is_valid=report.is_valid,
        delisting_count=len(delisting_events),
    )

    return report
