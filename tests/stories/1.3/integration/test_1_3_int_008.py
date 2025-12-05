"""Test ID: 1.3-INT-008

Test that loaded DataFrame has correct dtypes after Parquet round-trip.

Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac7-cached-parquet-readable-with-correct-dtypes-and-index
"""

from datetime import date

import pandas as pd
import pytest

from momo.data.cache import load_prices, save_prices


@pytest.mark.p0
@pytest.mark.integration
def test_1_3_int_008_loaded_dataframe_has_correct_dtypes(
    temp_cache_dir: str,
    sample_price_df: pd.DataFrame,
) -> None:
    """Test ID: 1.3-INT-008

    Story: 1.3 - Implement Data Loading and Parquet Caching
    Priority: P0
    Test Level: Integration
    Risk Coverage: DATA-001

    Verifies loaded DataFrame has correct dtypes after Parquet I/O.

    Steps:
    1. Define cache parameters (universe, start_date, end_date)
    2. Save sample_price_df to cache using save_prices()
    3. Load data back using load_prices()
    4. Verify each column has correct dtype (float64 for prices, int64 for volume)
    5. Verify index has correct dtype (datetime64[ns] for date)

    Expected: All dtypes preserved after Parquet round-trip
    """
    # Step 1: Define cache parameters
    universe = "test_universe"
    start_date = date(2020, 1, 1)
    end_date = date(2020, 1, 10)

    # Step 2: Save to cache
    save_prices(sample_price_df, universe, start_date, end_date)

    # Step 3: Load from cache
    loaded_df = load_prices(universe, start_date, end_date)

    # Step 4: Verify column dtypes
    assert loaded_df is not None, "load_prices() should return DataFrame"

    expected_dtypes = {
        "open": "float64",
        "high": "float64",
        "low": "float64",
        "close": "float64",
        "volume": "int64",
        "unadjusted_close": "float64",
        "dividend": "float64",
    }

    for col, expected_dtype in expected_dtypes.items():
        actual_dtype = str(loaded_df[col].dtype)
        assert (
            actual_dtype == expected_dtype
        ), f"Column {col}: expected dtype {expected_dtype}, got {actual_dtype}"

    # Step 5: Verify index dtypes
    assert isinstance(loaded_df.index, pd.MultiIndex), "Index should be MultiIndex after loading"

    # Date level should be datetime64[ns]
    date_level_dtype = str(loaded_df.index.levels[0].dtype)
    assert (
        date_level_dtype == "datetime64[ns]"
    ), f"Date index level: expected datetime64[ns], got {date_level_dtype}"

    # Symbol level should be object (string)
    symbol_level_dtype = str(loaded_df.index.levels[1].dtype)
    assert (
        symbol_level_dtype == "object"
    ), f"Symbol index level: expected object, got {symbol_level_dtype}"
