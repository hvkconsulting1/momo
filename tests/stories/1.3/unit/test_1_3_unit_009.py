"""Test ID: 1.3-UNIT-009

Verify _validate_price_schema() rejects empty DataFrames with informative exception.

Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac3-cache-to-parquet-with-organized-naming
"""

import pandas as pd
import pytest

from momo.data.cache import _validate_price_schema
from momo.utils.exceptions import CacheError


@pytest.mark.p0
@pytest.mark.unit
def test_schema_validation_rejects_empty_dataframe(
    sample_price_df: pd.DataFrame, invalid_schema_dfs: dict[str, pd.DataFrame]
) -> None:
    """Test ID: 1.3-UNIT-009

    Verify _validate_price_schema() rejects empty DataFrames with informative exception.

    Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac3-cache-to-parquet-with-organized-naming

    Steps:
    1. Call _validate_price_schema() with valid DataFrame (should pass)
    2. Create empty DataFrame (0 rows but correct schema)
    3. Call _validate_price_schema() with empty DataFrame
    4. Verify CacheError is raised
    5. Verify error message mentions empty DataFrame

    Expected: Validation passes for non-empty DataFrame, raises CacheError with informative message for empty DataFrame
    """
    # Step 1: Valid DataFrame should pass validation
    try:
        _validate_price_schema(sample_price_df)
    except CacheError as e:
        pytest.fail(f"Valid DataFrame failed schema validation: {e}")

    # Step 2-3: Empty DataFrame should fail validation
    empty_df = invalid_schema_dfs["empty"]

    # Step 4: Verify CacheError is raised
    with pytest.raises(CacheError) as exc_info:
        _validate_price_schema(empty_df)

    # Step 5: Verify error message is informative
    error_msg = str(exc_info.value)
    assert (
        "empty" in error_msg.lower()
    ), f"Error message should mention empty DataFrame, got: {error_msg}"
    assert "0 rows" in error_msg, f"Error message should mention 0 rows, got: {error_msg}"
