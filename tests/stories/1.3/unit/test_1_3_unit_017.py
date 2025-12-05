"""Test ID: 1.3-UNIT-017

Test round-trip equality: save → load → DataFrame comparison (schema, values, index).

Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac7-cached-parquet-readable-with-correct-dtypes-and-index
"""

from datetime import date

import pandas as pd
import pytest

from momo.data.cache import load_prices, save_prices


@pytest.mark.p0
@pytest.mark.unit
def test_1_3_unit_017_round_trip_equality(
    temp_cache_dir: str,
    sample_price_df: pd.DataFrame,
) -> None:
    """Test ID: 1.3-UNIT-017

    Story: 1.3 - Implement Data Loading and Parquet Caching
    Priority: P0
    Test Level: Unit
    Risk Coverage: DATA-001, DATA-002

    Verifies round-trip equality: save → load → DataFrame comparison.

    Steps:
    1. Define cache parameters (universe, start_date, end_date)
    2. Save sample_price_df to cache using save_prices()
    3. Load data back using load_prices()
    4. Verify schema matches (columns, dtypes, index names)
    5. Verify values are identical (using pd.testing.assert_frame_equal)
    6. Verify MultiIndex structure preserved

    Expected: Loaded DataFrame is identical to original DataFrame
    """
    # Step 1: Define cache parameters
    universe = "test_universe"
    start_date = date(2020, 1, 1)
    end_date = date(2020, 1, 10)

    # Step 2: Save to cache
    save_prices(sample_price_df, universe, start_date, end_date)

    # Step 3: Load from cache
    loaded_df = load_prices(universe, start_date, end_date)

    # Step 4: Verify schema matches
    assert loaded_df is not None, "load_prices() should return DataFrame"
    assert list(loaded_df.columns) == list(sample_price_df.columns), "Column names should match"
    assert list(loaded_df.dtypes) == list(sample_price_df.dtypes), "Column dtypes should match"
    assert list(loaded_df.index.names) == list(
        sample_price_df.index.names
    ), "Index names should match"

    # Step 5: Verify values are identical
    pd.testing.assert_frame_equal(
        loaded_df,
        sample_price_df,
        check_exact=True,
        check_dtype=True,
        check_index_type=True,
    )

    # Step 6: Verify MultiIndex structure preserved
    assert isinstance(loaded_df.index, pd.MultiIndex), "Index should be MultiIndex after round-trip"
    assert loaded_df.index.names == [
        "date",
        "symbol",
    ], "MultiIndex names should be ['date', 'symbol']"
