"""Test ID: 1.3-INT-003

Test Parquet compression and engine configuration.
"""

from datetime import date
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq  # type: ignore[import-untyped]
import pytest

from momo.data.cache import save_prices


@pytest.mark.p1
@pytest.mark.integration
def test_1_3_int_003(sample_price_df: pd.DataFrame, tmp_path: Path) -> None:
    """Test ID: 1.3-INT-003

    Verify Parquet files use snappy compression and pyarrow engine.

    Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac3-cache-to-parquet-with-organized-naming

    Steps:
    1. Save sample DataFrame to Parquet using save_prices()
    2. Read Parquet file metadata using pyarrow
    3. Verify file uses snappy compression
    4. Verify file was created by pyarrow (engine validation)
    5. Verify file can be read back successfully

    Expected: Parquet file uses snappy compression and pyarrow engine
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
        # Step 1: Save DataFrame to Parquet
        cache_path = save_prices(sample_price_df, universe, start_date, end_date)

        # Step 2: Read Parquet file metadata
        parquet_file = pq.ParquetFile(cache_path)

        # Step 3: Verify snappy compression
        # Check compression codec for first row group
        metadata = parquet_file.metadata
        assert metadata.num_row_groups > 0, "Parquet file should have at least one row group"

        # Get compression codec from first column chunk of first row group
        row_group = metadata.row_group(0)
        column_chunk = row_group.column(0)
        compression = column_chunk.compression

        assert compression == "SNAPPY", f"Expected SNAPPY compression, got {compression}"

        # Step 4: Verify pyarrow was used (check metadata for pyarrow creator)
        # PyArrow writes creator metadata to Parquet files
        creator = metadata.created_by
        assert creator is not None, "Parquet file should have creator metadata"
        assert (
            "parquet-cpp" in creator.lower() or "pyarrow" in creator.lower()
        ), f"Expected pyarrow engine creator, got: {creator}"

        # Step 5: Verify file can be read back successfully
        loaded_df = pd.read_parquet(cache_path, engine="pyarrow")
        assert len(loaded_df) == len(sample_price_df), "Loaded DataFrame should have same length"
        assert list(loaded_df.columns) == list(
            sample_price_df.columns
        ), "Loaded DataFrame should have same columns"

    finally:
        # Restore original function
        cache_module.get_cache_path = original_get_cache_path
