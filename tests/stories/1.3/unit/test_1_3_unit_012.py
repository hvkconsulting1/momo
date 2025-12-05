"""Test ID: 1.3-UNIT-012

Test that load_prices() returns DataFrame when cache file exists and is valid.

Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac4-cache-loading-checks-local-parquet-before-api-query
"""

from datetime import date

import pandas as pd
import pytest

from momo.data.cache import load_prices, save_prices


@pytest.mark.p0
@pytest.mark.unit
def test_1_3_unit_012_load_prices_returns_dataframe_on_cache_hit(
    temp_cache_dir: str,
    sample_price_df: pd.DataFrame,
) -> None:
    """Test ID: 1.3-UNIT-012

    Story: 1.3 - Implement Data Loading and Parquet Caching
    Priority: P0
    Test Level: Unit
    Risk Coverage: N/A

    Verifies load_prices() returns DataFrame when cache file exists and is valid.

    Steps:
    1. Define cache parameters (universe, start_date, end_date)
    2. Save sample_price_df to cache using save_prices()
    3. Call load_prices() with same parameters
    4. Verify it returns a DataFrame (not None)
    5. Verify returned DataFrame has expected shape

    Expected: load_prices() returns valid DataFrame matching cached data
    """
    # Step 1: Define cache parameters
    universe = "test_universe"
    start_date = date(2020, 1, 1)
    end_date = date(2020, 1, 10)

    # Step 2: Save sample data to cache
    save_prices(sample_price_df, universe, start_date, end_date)

    # Step 3: Call load_prices()
    result = load_prices(universe, start_date, end_date)

    # Step 4: Verify returns DataFrame (not None)
    assert result is not None, "load_prices() should return DataFrame when cache exists"
    assert isinstance(result, pd.DataFrame), f"Expected pd.DataFrame, got {type(result).__name__}"

    # Step 5: Verify DataFrame has expected shape
    assert (
        result.shape == sample_price_df.shape
    ), f"Expected shape {sample_price_df.shape}, got {result.shape}"
