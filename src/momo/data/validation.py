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

Usage:
    >>> from momo.data.validation import validate_prices
    >>> import pandas as pd
    >>> # Assume prices_df is MultiIndex DataFrame from loader.load_universe()
    >>> report = validate_prices(prices_df)
    >>> print(report.summary_message)
    >>> if not report.is_valid:
    >>>     print(f"Missing data: {report.missing_data_counts}")
    >>>     print(f"Date gaps: {report.date_gaps}")
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date as date_type

import pandas as pd
import structlog

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


def validate_prices(prices_df: pd.DataFrame) -> ValidationReport:
    """Validate price data quality with comprehensive checks.

    Performs validation checks on price DataFrame including:
    1. Missing data detection (NaN/null values)
    2. Date gap identification (suspicious gaps in time series)
    3. Adjustment factor consistency (split/dividend validation)
    4. Delisting status detection

    Args:
        prices_df: Price data with MultiIndex (date, symbol) and OHLC columns

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
        This is a skeleton implementation. Validation logic will be added in subsequent commits.
        Currently returns minimal ValidationReport with no validation performed.
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

    # Future commits will implement:
    # - check_delisting_status() for delisting detection

    # Determine validation status
    is_valid = len(missing_data_counts) == 0 and len(date_gaps) == 0 and len(adjustment_issues) == 0

    # Generate summary message
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

    if issues:
        summary_message = f"Validation found issues: {'; '.join(issues)}"
    else:
        summary_message = f"Validation complete: {total_tickers} tickers, no issues detected"

    report = ValidationReport(
        total_tickers=total_tickers,
        date_range=(start_date, end_date),
        missing_data_counts=missing_data_counts,
        date_gaps=date_gaps,
        adjustment_issues=adjustment_issues,
        delisting_events={},  # Future commits
        summary_message=summary_message,
        is_valid=is_valid,
    )

    logger.info(
        "Price data validation complete",
        layer="data",
        operation="validate_prices",
        total_tickers=total_tickers,
        is_valid=report.is_valid,
    )

    return report
