"""Test ID: 1.3-UNIT-016

Test cache invalidation functionality.
"""

from datetime import date
from pathlib import Path

import pandas as pd
import pytest

from momo.data.cache import invalidate, save_prices


@pytest.mark.p1
@pytest.mark.unit
def test_1_3_unit_016(sample_price_df: pd.DataFrame, tmp_path: Path) -> None:
    """Test ID: 1.3-UNIT-016

    Verify invalidate() removes cache files for given universe.

    Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac5-force-refresh-option-bypasses-cache

    Steps:
    1. Save sample DataFrame to cache
    2. Verify cache file exists
    3. Call invalidate() with same parameters
    4. Verify cache file no longer exists
    5. Call invalidate() again (should not raise error for missing file)

    Expected: Cache file is removed by invalidate(), idempotent behavior
    """
    universe = "test_universe"
    start_date = date(2020, 1, 1)
    end_date = date(2020, 1, 10)

    # Monkey-patch get_cache_path to use tmp_path
    import momo.data.cache as cache_module

    original_get_cache_path = cache_module.get_cache_path

    def patched_get_cache_path(universe: str, start_date: date, end_date: date) -> Path:
        filename = f"{universe}_{start_date.isoformat()}_{end_date.isoformat()}.parquet"
        return tmp_path / "data" / "cache" / "prices" / filename

    cache_module.get_cache_path = patched_get_cache_path

    try:
        # Step 1: Save DataFrame to cache
        cache_path = save_prices(sample_price_df, universe, start_date, end_date)

        # Step 2: Verify cache file exists
        assert cache_path.exists(), f"Cache file should exist at {cache_path}"

        # Step 3: Call invalidate()
        invalidate(universe, start_date, end_date)

        # Step 4: Verify cache file no longer exists
        assert not cache_path.exists(), f"Cache file should be removed at {cache_path}"

        # Step 5: Call invalidate() again (idempotent - should not raise error)
        invalidate(universe, start_date, end_date)  # Should not raise exception

    finally:
        # Restore original function
        cache_module.get_cache_path = original_get_cache_path
