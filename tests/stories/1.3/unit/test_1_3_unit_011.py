"""Test ID: 1.3-UNIT-011

Test that load_prices() returns None when cache file does not exist.

Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac4-cache-loading-checks-local-parquet-before-api-query
"""

from datetime import date

import pytest

from momo.data.cache import load_prices


@pytest.mark.p0
@pytest.mark.unit
def test_1_3_unit_011_load_prices_returns_none_on_cache_miss(
    temp_cache_dir: str,
) -> None:
    """Test ID: 1.3-UNIT-011

    Story: 1.3 - Implement Data Loading and Parquet Caching
    Priority: P0
    Test Level: Unit
    Risk Coverage: N/A

    Verifies load_prices() returns None when cache file does not exist.

    Steps:
    1. Define cache parameters (universe, start_date, end_date)
    2. Ensure cache file does not exist (using temp_cache_dir fixture)
    3. Call load_prices() with these parameters
    4. Verify it returns None

    Expected: load_prices() returns None for cache miss scenario
    """
    # Step 1: Define cache parameters
    universe = "test_universe"
    start_date = date(2020, 1, 1)
    end_date = date(2020, 1, 31)

    # Step 2: Cache file doesn't exist (temp_cache_dir is empty)
    # Step 3: Call load_prices()
    result = load_prices(universe, start_date, end_date)

    # Step 4: Verify returns None
    assert result is None, "load_prices() should return None when cache file doesn't exist"
