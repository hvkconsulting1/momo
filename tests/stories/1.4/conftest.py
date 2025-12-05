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


@pytest.fixture
def sample_price_df_with_negative_price(sample_price_df_clean: pd.DataFrame) -> pd.DataFrame:
    """Prices DataFrame with negative close price for ticker FAIL.

    Args:
        sample_price_df_clean: Clean price DataFrame fixture dependency

    Returns:
        pd.DataFrame: Price data with FAIL ticker having negative close price.

    Schema:
        Same as sample_price_df_clean, but with FAIL ticker added with negative close value.
    """
    df = sample_price_df_clean.copy()

    # Add FAIL ticker with negative close price
    fail_dates = df.index.get_level_values("date").unique()
    fail_data = []

    for dt in fail_dates:
        fail_data.append(
            {
                "date": dt,
                "symbol": "FAIL",
                "open": 100.0,
                "high": 105.0,
                "low": 95.0,
                "close": -50.0,  # Negative close price (invalid)
                "volume": 1000000,
                "unadjusted_close": -50.0,
                "dividend": 0.0,
            }
        )

    # Create FAIL DataFrame and concatenate with clean data
    fail_df = pd.DataFrame(fail_data)
    fail_df = fail_df.set_index(["date", "symbol"])
    fail_df["volume"] = fail_df["volume"].astype("int64")

    # Combine with clean data
    result_df = pd.concat([df, fail_df])
    result_df = result_df.sort_index()

    return result_df


@pytest.fixture
def sample_price_df_with_50pct_jump_no_div(sample_price_df_clean: pd.DataFrame) -> pd.DataFrame:
    """Prices DataFrame with 50% price jump without dividend for ticker XYZ.

    Args:
        sample_price_df_clean: Clean price DataFrame fixture dependency

    Returns:
        pd.DataFrame: Price data with XYZ ticker showing 50% price jump with dividend=0.

    Schema:
        Same as sample_price_df_clean, but with XYZ ticker added with 50% price jump.
        Day 1: close = 100
        Day 2: close = 150 (50% jump)
        dividend column = 0.0 for all days (no dividend to justify jump)
    """
    df = sample_price_df_clean.copy()

    # Get dates for XYZ ticker
    xyz_dates = df.index.get_level_values("date").unique()
    xyz_data = []

    for i, dt in enumerate(xyz_dates):
        if i == 0:
            # First day: close = 100
            close_price = 100.0
        else:
            # Second day onwards: close = 150 (50% jump from day 1)
            close_price = 150.0

        xyz_data.append(
            {
                "date": dt,
                "symbol": "XYZ",
                "open": close_price,
                "high": close_price + 5.0,
                "low": close_price - 5.0,
                "close": close_price,
                "volume": 1000000,
                "unadjusted_close": close_price,
                "dividend": 0.0,  # No dividend to justify the jump
            }
        )

    # Create XYZ DataFrame and concatenate with clean data
    xyz_df = pd.DataFrame(xyz_data)
    xyz_df = xyz_df.set_index(["date", "symbol"])
    xyz_df["volume"] = xyz_df["volume"].astype("int64")

    # Combine with clean data
    result_df = pd.concat([df, xyz_df])
    result_df = result_df.sort_index()

    return result_df


@pytest.fixture
def sample_price_df_with_aapl_split() -> pd.DataFrame:
    """Historical Apple data with 7:1 stock split on June 9, 2014.

    Returns:
        pd.DataFrame: Price data simulating Apple's 7:1 split with proper adjustment.

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
        - Before split (June 6, 2014): close ~ 645.57 (unadjusted)
        - After split (June 9, 2014): close ~ 92.22 (unadjusted, 645.57 / 7)
        - close column shows adjusted prices (no jump after split)
        - unadjusted_close shows the actual raw prices (with 7x jump)
        - This simulates a properly adjusted split that should NOT be flagged
    """
    # Dates around Apple's 7:1 stock split (June 9, 2014)
    dates_before_split = pd.to_datetime(["2014-06-05", "2014-06-06"])  # Thu, Fri before split
    dates_after_split = pd.to_datetime(
        ["2014-06-09", "2014-06-10", "2014-06-11"]
    )  # Mon-Wed after split

    aapl_data = []

    # Pre-split prices (unadjusted ~ 645.57)
    for dt in dates_before_split:
        aapl_data.append(
            {
                "date": dt,
                "symbol": "AAPL",
                "open": 640.0,
                "high": 650.0,
                "low": 635.0,
                "close": 645.57,  # Adjusted price (remains consistent)
                "volume": 10000000,
                "unadjusted_close": 645.57,  # Raw price before split
                "dividend": 0.0,
            }
        )

    # Post-split prices (unadjusted ~ 92.22 = 645.57 / 7)
    for dt in dates_after_split:
        aapl_data.append(
            {
                "date": dt,
                "symbol": "AAPL",
                "open": 91.0,
                "high": 93.5,
                "low": 90.5,
                "close": 645.57,  # Adjusted price (remains consistent after split adjustment)
                "volume": 70000000,  # Volume increases 7x post-split
                "unadjusted_close": 92.22,  # Raw price after split (645.57 / 7)
                "dividend": 0.0,
            }
        )

    # Create DataFrame
    df = pd.DataFrame(aapl_data)
    df = df.set_index(["date", "symbol"])
    df["volume"] = df["volume"].astype("int64")

    return df
