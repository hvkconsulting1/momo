"""Test ID: 1.3-UNIT-010

Test metadata tracking in Parquet cache files.
"""

from datetime import date, datetime
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq  # type: ignore[import-untyped]
import pytest

from momo.data.cache import save_prices


@pytest.mark.p1
@pytest.mark.unit
def test_1_3_unit_010(sample_price_df: pd.DataFrame, tmp_path: Path) -> None:
    """Test ID: 1.3-UNIT-010

    Verify save_prices() includes metadata in Parquet file.

    Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac3-cache-to-parquet-with-organized-naming

    Steps:
    1. Save sample DataFrame to Parquet using save_prices()
    2. Read Parquet file metadata using pyarrow
    3. Verify metadata includes universe, start_date, end_date
    4. Verify metadata includes created_at timestamp
    5. Verify metadata includes schema_version

    Expected: Metadata contains all required fields with correct values
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
        # Step 1: Save DataFrame with metadata
        cache_path = save_prices(sample_price_df, universe, start_date, end_date)

        # Step 2: Read Parquet metadata using pyarrow
        parquet_file = pq.ParquetFile(cache_path)
        metadata = parquet_file.schema_arrow.metadata

        # Convert metadata from bytes to dict
        metadata_dict = {
            k.decode(): v.decode() for k, v in metadata.items() if k.startswith(b"momo")
        }

        # Step 3: Verify universe, start_date, end_date
        assert "momo:universe" in metadata_dict, "Missing 'universe' in metadata"
        assert metadata_dict["momo:universe"] == universe

        assert "momo:start_date" in metadata_dict, "Missing 'start_date' in metadata"
        assert metadata_dict["momo:start_date"] == start_date.isoformat()

        assert "momo:end_date" in metadata_dict, "Missing 'end_date' in metadata"
        assert metadata_dict["momo:end_date"] == end_date.isoformat()

        # Step 4: Verify created_at timestamp
        assert "momo:created_at" in metadata_dict, "Missing 'created_at' in metadata"
        created_at_str = metadata_dict["momo:created_at"]
        # Verify it's a valid ISO format timestamp
        created_at = datetime.fromisoformat(created_at_str)
        assert created_at.tzinfo is not None, "created_at should include timezone"

        # Step 5: Verify schema_version
        assert "momo:schema_version" in metadata_dict, "Missing 'schema_version' in metadata"
        assert metadata_dict["momo:schema_version"] == "1.0"

    finally:
        # Restore original function
        cache_module.get_cache_path = original_get_cache_path
