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
