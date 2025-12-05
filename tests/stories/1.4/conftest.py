"""
Shared test fixtures for Story 1.4: Data Quality Validation Pipeline.

Provides synthetic price data for validation testing with various data quality scenarios.
"""

import pandas as pd
import pytest


@pytest.fixture
def sample_price_df_clean() -> pd.DataFrame:
    """Clean prices DataFrame with 5 tickers, 10 days, no data quality issues.

    Returns:
        pd.DataFrame: Price data with MultiIndex (date, symbol) and complete OHLC data.

    Schema:
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
    """
    dates = pd.date_range("2020-01-01", periods=10, freq="D")
    symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

    # Create MultiIndex
    index = pd.MultiIndex.from_product([dates, symbols], names=["date", "symbol"])

    # Create clean data with consistent values
    data = {
        "open": 100.0,
        "high": 105.0,
        "low": 95.0,
        "close": 102.0,
        "volume": 1000000,
        "unadjusted_close": 102.0,
        "dividend": 0.0,
    }

    # Create DataFrame with repeated values for all rows
    df = pd.DataFrame(index=index, data=[data] * len(index))

    # Convert volume to int64
    df["volume"] = df["volume"].astype("int64")

    return df


@pytest.fixture
def sample_price_df_with_nans_close(sample_price_df_clean: pd.DataFrame) -> pd.DataFrame:
    """Prices DataFrame with 3 NaN values in close column for AAPL.

    Args:
        sample_price_df_clean: Clean price DataFrame fixture dependency

    Returns:
        pd.DataFrame: Price data with AAPL having 3 NaN in close column.

    Schema:
        Same as sample_price_df_clean, but AAPL close column has 3 NaN values.
    """
    df = sample_price_df_clean.copy()

    # Get AAPL data indices (first 10 rows in MultiIndex)
    aapl_mask = df.index.get_level_values("symbol") == "AAPL"
    aapl_indices = df[aapl_mask].index

    # Inject 3 NaN values into AAPL close column (rows 2, 5, 8)
    df.loc[aapl_indices[2], "close"] = float("nan")
    df.loc[aapl_indices[5], "close"] = float("nan")
    df.loc[aapl_indices[8], "close"] = float("nan")

    return df


@pytest.fixture
def sample_price_df_with_nans_ohlc(sample_price_df_clean: pd.DataFrame) -> pd.DataFrame:
    """Prices DataFrame with NaN values across OHLC columns for MSFT.

    Args:
        sample_price_df_clean: Clean price DataFrame fixture dependency

    Returns:
        pd.DataFrame: Price data with MSFT having NaN in open, high, low columns.

    Schema:
        Same as sample_price_df_clean, but MSFT has 2 NaN in open, 1 NaN in high.
    """
    df = sample_price_df_clean.copy()

    # Get MSFT data indices
    msft_mask = df.index.get_level_values("symbol") == "MSFT"
    msft_indices = df[msft_mask].index

    # Inject NaN values across OHLC columns
    # 2 NaN in open column (rows 1, 4)
    df.loc[msft_indices[1], "open"] = float("nan")
    df.loc[msft_indices[4], "open"] = float("nan")

    # 1 NaN in high column (row 3)
    df.loc[msft_indices[3], "high"] = float("nan")

    return df


@pytest.fixture
def sample_price_df_with_10day_gap() -> pd.DataFrame:
    """Prices DataFrame with 10-business-day gap for TSLA.

    Returns:
        pd.DataFrame: Price data with TSLA missing data from 2020-06-01 to 2020-06-15.

    Schema:
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

    Data characteristics:
        - TSLA has a gap from 2020-05-29 (Fri) to 2020-06-15 (Mon) = 11 business days
        - Other tickers (AAPL, MSFT, GOOGL, AMZN) have complete data with no gaps
    """
    # Create date range WITH gap for TSLA only
    dates_before_gap = pd.date_range("2020-05-25", "2020-05-29", freq="B")  # Week before gap
    dates_after_gap = pd.date_range("2020-06-15", "2020-06-19", freq="B")  # Week after gap

    # Create CONTINUOUS date range for other tickers (no gap)
    all_dates_continuous = pd.date_range("2020-05-25", "2020-06-19", freq="B")

    # Create list to hold all rows
    rows = []

    # Create data for all tickers except TSLA with CONTINUOUS date range (no gaps)
    for symbol in ["AAPL", "MSFT", "GOOGL", "AMZN"]:
        for dt in all_dates_continuous:
            rows.append(
                {
                    "date": dt,
                    "symbol": symbol,
                    "open": 100.0,
                    "high": 105.0,
                    "low": 95.0,
                    "close": 102.0,
                    "volume": 1000000,
                    "unadjusted_close": 102.0,
                    "dividend": 0.0,
                }
            )

    # Create data for TSLA - only dates BEFORE and AFTER the gap (missing middle dates)
    # dates_before_gap: 2020-05-25 to 2020-05-29 (5 business days)
    # dates_after_gap: 2020-06-15 to 2020-06-19 (5 business days)
    # Gap: 2020-05-29 to 2020-06-15 = 11 business days
    for dt in dates_before_gap:
        rows.append(
            {
                "date": dt,
                "symbol": "TSLA",
                "open": 100.0,
                "high": 105.0,
                "low": 95.0,
                "close": 102.0,
                "volume": 1000000,
                "unadjusted_close": 102.0,
                "dividend": 0.0,
            }
        )

    for dt in dates_after_gap:
        rows.append(
            {
                "date": dt,
                "symbol": "TSLA",
                "open": 100.0,
                "high": 105.0,
                "low": 95.0,
                "close": 102.0,
                "volume": 1000000,
                "unadjusted_close": 102.0,
                "dividend": 0.0,
            }
        )

    # Create DataFrame from rows
    df = pd.DataFrame(rows)
    df = df.set_index(["date", "symbol"])
    df["volume"] = df["volume"].astype("int64")

    return df


@pytest.fixture
def sample_price_df_with_weekends_missing() -> pd.DataFrame:
    """Typical trading data with weekday-only prices (no weekend data).

    Returns:
        pd.DataFrame: Price data for 10 business days (Mon-Fri only).

    Schema:
        Index:
            - MultiIndex with levels: (date: datetime64[ns], symbol: str)
            - Names: ['date', 'symbol']
            - Dates: Business days only (freq='B')
        Columns:
            - open: float64
            - high: float64
            - low: float64
            - close: float64
            - volume: int64
            - unadjusted_close: float64
            - dividend: float64
    """
    # Use business day frequency to create typical trading data (no weekends)
    dates = pd.date_range("2020-01-06", periods=10, freq="B")  # Starts Monday
    symbols = ["AAPL", "MSFT", "GOOGL"]

    # Create MultiIndex
    index = pd.MultiIndex.from_product([dates, symbols], names=["date", "symbol"])

    # Create data
    data = {
        "open": 100.0,
        "high": 105.0,
        "low": 95.0,
        "close": 102.0,
        "volume": 1000000,
        "unadjusted_close": 102.0,
        "dividend": 0.0,
    }
    df = pd.DataFrame(index=index, data=[data] * len(index))
    df["volume"] = df["volume"].astype("int64")

    return df


@pytest.fixture
def sample_price_df_with_july4_missing() -> pd.DataFrame:
    """Trading data missing July 3, 2020 (Independence Day observed, Friday).

    Returns:
        pd.DataFrame: Price data with expected market holiday gap.

    Schema:
        Index:
            - MultiIndex with levels: (date: datetime64[ns], symbol: str)
            - Names: ['date', 'symbol']
            - Dates: 2020-07-01, 2020-07-02, 2020-07-06 (missing 2020-07-03 holiday)
        Columns:
            - open: float64
            - high: float64
            - low: float64
            - close: float64
            - volume: int64
            - unadjusted_close: float64
            - dividend: float64
    """
    # Create dates around July 4, 2020
    # July 3, 2020 was Friday (market closed for Independence Day observed)
    # Include: Wed 7/1, Thu 7/2, Mon 7/6 (skip Fri 7/3)
    dates = pd.to_datetime(["2020-07-01", "2020-07-02", "2020-07-06"])
    symbols = ["AAPL", "MSFT", "GOOGL"]

    # Create MultiIndex
    index = pd.MultiIndex.from_product([dates, symbols], names=["date", "symbol"])

    # Create data
    data = {
        "open": 100.0,
        "high": 105.0,
        "low": 95.0,
        "close": 102.0,
        "volume": 1000000,
        "unadjusted_close": 102.0,
        "dividend": 0.0,
    }
    df = pd.DataFrame(index=index, data=[data] * len(index))
    df["volume"] = df["volume"].astype("int64")

    return df
