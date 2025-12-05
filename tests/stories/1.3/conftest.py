"""Shared fixtures for Story 1.3 test suite.

This module provides common test fixtures for data loading and Parquet caching tests.
"""

from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture
def sample_price_df() -> pd.DataFrame:
    """Standard valid DataFrame for cache tests.

    Returns:
        DataFrame with MultiIndex (date, symbol) and all required price columns.

    Schema:
        - Index: MultiIndex (date: datetime64[ns], symbol: str)
        - Columns: open, high, low, close, volume, unadjusted_close, dividend
        - Data: 10 dates x 3 symbols = 30 rows
    """
    dates = pd.date_range("2020-01-01", "2020-01-10", freq="D")
    symbols = ["AAPL", "MSFT", "GOOGL"]

    data = {
        "open": [100.0] * 30,
        "high": [105.0] * 30,
        "low": [95.0] * 30,
        "close": [102.0] * 30,
        "volume": [1000000] * 30,
        "unadjusted_close": [102.0] * 30,
        "dividend": [0.0] * 30,
    }

    index = pd.MultiIndex.from_product([dates, symbols], names=["date", "symbol"])
    return pd.DataFrame(data, index=index)


@pytest.fixture
def invalid_schema_dfs(sample_price_df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Collection of schema-violating DataFrames for validation tests.

    Args:
        sample_price_df: Valid sample DataFrame to derive invalid versions from

    Returns:
        Dictionary mapping error type to invalid DataFrame:
        - 'missing_column': Missing 'dividend' column
        - 'wrong_dtype': 'volume' as float64 instead of int64
        - 'wrong_index': Single index instead of MultiIndex
        - 'empty': Empty DataFrame (0 rows)
    """
    # Missing column
    missing_column_df = sample_price_df.drop(columns=["dividend"])

    # Wrong dtype
    wrong_dtype_df = sample_price_df.copy()
    wrong_dtype_df["volume"] = wrong_dtype_df["volume"].astype("float64")

    # Wrong index (single index instead of MultiIndex)
    wrong_index_df = sample_price_df.reset_index(drop=True)

    # Empty DataFrame (0 rows but correct schema)
    empty_df = sample_price_df.iloc[0:0].copy()

    return {
        "missing_column": missing_column_df,
        "wrong_dtype": wrong_dtype_df,
        "wrong_index": wrong_index_df,
        "empty": empty_df,
    }


@pytest.fixture
def temp_cache_dir(tmp_path: Path) -> Path:
    """Temporary cache directory using pytest tmp_path fixture.

    Args:
        tmp_path: Pytest built-in temporary directory fixture

    Returns:
        Path to isolated cache directory for testing (data/cache/prices/)
    """
    cache_dir = tmp_path / "data" / "cache" / "prices"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir
