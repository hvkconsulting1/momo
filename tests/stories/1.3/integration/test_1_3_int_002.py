"""Test ID: 1.3-INT-002

Test that save_prices() writes Parquet to correct path in data/cache/prices/ directory.

Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac3-cache-to-parquet-with-organized-naming
"""

from datetime import date
from pathlib import Path

import pandas as pd
import pytest

from momo.data.cache import save_prices


@pytest.mark.p0
@pytest.mark.integration
def test_1_3_int_002_save_prices_writes_to_correct_path(
    temp_cache_dir: str,
    sample_price_df: pd.DataFrame,
) -> None:
    """Test ID: 1.3-INT-002

    Story: 1.3 - Implement Data Loading and Parquet Caching
    Priority: P0
    Test Level: Integration
    Risk Coverage: N/A

    Verifies save_prices() writes Parquet to correct directory path.

    Steps:
    1. Define cache parameters (universe, start_date, end_date)
    2. Call save_prices() with sample_price_df
    3. Verify returned path matches expected pattern
    4. Verify file actually exists at returned path
    5. Verify file is in data/cache/prices/ directory structure

    Expected: Parquet file written to data/cache/prices/{universe}_{start}_{end}.parquet
    """
    # Step 1: Define cache parameters
    universe = "test_universe"
    start_date = date(2020, 1, 1)
    end_date = date(2020, 1, 10)

    # Step 2: Call save_prices()
    returned_path = save_prices(sample_price_df, universe, start_date, end_date)

    # Step 3: Verify returned path matches expected pattern
    expected_filename = f"{universe}_{start_date.isoformat()}_{end_date.isoformat()}.parquet"
    assert (
        returned_path.name == expected_filename
    ), f"Expected filename {expected_filename}, got {returned_path.name}"

    # Verify path structure
    expected_path = Path("data") / "cache" / "prices" / expected_filename
    assert returned_path == expected_path, f"Expected path {expected_path}, got {returned_path}"

    # Step 4: Verify file actually exists at returned path
    assert returned_path.exists(), f"Cache file should exist at {returned_path}"
    assert returned_path.is_file(), f"Path should be a file, not directory: {returned_path}"

    # Step 5: Verify file is in data/cache/prices/ directory structure
    assert (
        returned_path.parent == Path("data") / "cache" / "prices"
    ), f"Cache file should be in data/cache/prices/, got {returned_path.parent}"
