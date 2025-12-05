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

    # Future commits will implement:
    # - _check_date_gaps() for gap identification
    # - _check_adjustment_consistency() for adjustment validation
    # - check_delisting_status() for delisting detection

    # Determine validation status
    is_valid = len(missing_data_counts) == 0

    # Generate summary message
    if missing_data_counts:
        ticker_count = len(missing_data_counts)
        total_nans = sum(missing_data_counts.values())
        summary_message = (
            f"Validation found issues: {ticker_count} ticker(s) with "
            f"{total_nans} missing value(s)"
        )
    else:
        summary_message = f"Validation complete: {total_tickers} tickers, no issues detected"

    report = ValidationReport(
        total_tickers=total_tickers,
        date_range=(start_date, end_date),
        missing_data_counts=missing_data_counts,
        date_gaps={},  # Future commits
        adjustment_issues=[],  # Future commits
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
