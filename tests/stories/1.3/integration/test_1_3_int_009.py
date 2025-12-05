"""Test ID: 1.3-INT-009

Test that MultiIndex is preserved after Parquet round-trip.

Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac7-cached-parquet-readable-with-correct-dtypes-and-index
"""

from datetime import date

import pandas as pd
import pytest

from momo.data.cache import load_prices, save_prices


@pytest.mark.p0
@pytest.mark.integration
def test_1_3_int_009_multiindex_preserved_after_parquet_io(
    temp_cache_dir: str,
    sample_price_df: pd.DataFrame,
) -> None:
    """Test ID: 1.3-INT-009

    Story: 1.3 - Implement Data Loading and Parquet Caching
    Priority: P0
    Test Level: Integration
    Risk Coverage: DATA-002

    Verifies MultiIndex (date, symbol) structure is preserved after Parquet I/O.

    Steps:
    1. Define cache parameters (universe, start_date, end_date)
    2. Verify sample_price_df has MultiIndex with (date, symbol) structure
    3. Save sample_price_df to cache using save_prices()
    4. Load data back using load_prices()
    5. Verify loaded DataFrame has MultiIndex (not flattened to single index)
    6. Verify MultiIndex has correct names: ['date', 'symbol']
    7. Verify MultiIndex values match original

    Expected: MultiIndex structure fully preserved after Parquet I/O
    """
    # Step 1: Define cache parameters
    universe = "test_universe"
    start_date = date(2020, 1, 1)
    end_date = date(2020, 1, 10)

    # Step 2: Verify original has MultiIndex
    assert isinstance(
        sample_price_df.index, pd.MultiIndex
    ), "sample_price_df should have MultiIndex"
    assert sample_price_df.index.names == [
        "date",
        "symbol",
    ], "Original should have ['date', 'symbol'] index names"

    # Step 3: Save to cache
    save_prices(sample_price_df, universe, start_date, end_date)

    # Step 4: Load from cache
    loaded_df = load_prices(universe, start_date, end_date)

    # Step 5: Verify loaded DataFrame has MultiIndex
    assert loaded_df is not None, "load_prices() should return DataFrame"
    assert isinstance(
        loaded_df.index, pd.MultiIndex
    ), "Loaded DataFrame should have MultiIndex (not flattened)"

    # Step 6: Verify MultiIndex names
    assert loaded_df.index.names == [
        "date",
        "symbol",
    ], f"Expected index names ['date', 'symbol'], got {loaded_df.index.names}"

    # Step 7: Verify MultiIndex values match original
    assert loaded_df.index.equals(
        sample_price_df.index
    ), "MultiIndex values should match original after round-trip"

    # Additional verification: Check number of levels
    assert (
        loaded_df.index.nlevels == 2
    ), f"MultiIndex should have 2 levels, got {loaded_df.index.nlevels}"
