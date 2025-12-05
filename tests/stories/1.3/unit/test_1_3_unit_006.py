"""Test ID: 1.3-UNIT-006

Verify _validate_price_schema() validates DataFrame schema (required columns present).

Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac3-cache-to-parquet-with-organized-naming
"""

import pandas as pd
import pytest

from momo.data.cache import _validate_price_schema
from momo.utils.exceptions import CacheError


@pytest.mark.p0
@pytest.mark.unit
def test_schema_validation_required_columns(
    sample_price_df: pd.DataFrame, invalid_schema_dfs: dict[str, pd.DataFrame]
) -> None:
    """Test ID: 1.3-UNIT-006

    Verify _validate_price_schema() validates DataFrame has all required columns.

    Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac3-cache-to-parquet-with-organized-naming

    Steps:
    1. Call _validate_price_schema() with valid DataFrame (should pass)
    2. Create DataFrame missing 'dividend' column
    3. Call _validate_price_schema() with missing column DataFrame
    4. Verify CacheError is raised
    5. Verify error message lists missing columns

    Expected: Validation passes for valid schema, raises CacheError with informative message for missing columns
    """
    # Step 1: Valid DataFrame should pass validation
    try:
        _validate_price_schema(sample_price_df)
    except CacheError as e:
        pytest.fail(f"Valid DataFrame failed schema validation: {e}")

    # Step 2-3: DataFrame missing column should fail validation
    missing_column_df = invalid_schema_dfs["missing_column"]

    # Step 4: Verify CacheError is raised
    with pytest.raises(CacheError) as exc_info:
        _validate_price_schema(missing_column_df)

    # Step 5: Verify error message is informative
    error_msg = str(exc_info.value)
    assert (
        "Missing required columns" in error_msg
    ), f"Error message should mention missing columns, got: {error_msg}"
    assert (
        "dividend" in error_msg
    ), f"Error message should list 'dividend' as missing column, got: {error_msg}"
