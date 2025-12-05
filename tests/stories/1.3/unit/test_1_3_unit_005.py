"""Test ID: 1.3-UNIT-005

Verify get_cache_path() generates consistent paths following pattern.

Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac3-cache-to-parquet-with-organized-naming
"""

from datetime import date
from pathlib import Path

import pytest

from momo.data.cache import get_cache_path


@pytest.mark.p0
@pytest.mark.unit
def test_cache_path_generation_consistency() -> None:
    """Test ID: 1.3-UNIT-005

    Verify get_cache_path() generates consistent paths following {universe}_{start_date}_{end_date}.parquet pattern.

    Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac3-cache-to-parquet-with-organized-naming

    Steps:
    1. Call get_cache_path() with known parameters (universe, start_date, end_date)
    2. Verify path follows pattern: data/cache/prices/{universe}_{start_date}_{end_date}.parquet
    3. Verify path uses ISO date format (YYYY-MM-DD)
    4. Call get_cache_path() again with same parameters
    5. Verify both calls produce identical paths (deterministic)

    Expected: Path matches pattern and is deterministic for collision prevention
    """
    # Step 1: Generate path with known parameters
    universe = "russell_1000_cp"
    start_date = date(2010, 1, 1)
    end_date = date(2020, 12, 31)

    path1 = get_cache_path(universe, start_date, end_date)

    # Step 2: Verify path follows expected pattern
    expected_filename = "russell_1000_cp_2010-01-01_2020-12-31.parquet"
    expected_path = Path("data") / "cache" / "prices" / expected_filename

    assert path1 == expected_path, f"Path mismatch: expected {expected_path}, got {path1}"

    # Step 3: Verify ISO date format in filename
    assert "2010-01-01" in str(path1), "Start date not in ISO format"
    assert "2020-12-31" in str(path1), "End date not in ISO format"

    # Step 4: Generate path again with same parameters
    path2 = get_cache_path(universe, start_date, end_date)

    # Step 5: Verify deterministic behavior (collision prevention)
    assert path1 == path2, f"Cache path generation is not deterministic: {path1} != {path2}"
