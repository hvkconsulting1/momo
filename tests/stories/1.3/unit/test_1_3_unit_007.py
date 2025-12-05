"""Test ID: 1.3-UNIT-007

Verify _validate_price_schema() validates DataFrame dtypes match expected schema.

Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac3-cache-to-parquet-with-organized-naming
"""

import pandas as pd
import pytest

from momo.data.cache import _validate_price_schema
from momo.utils.exceptions import CacheError


@pytest.mark.p0
@pytest.mark.unit
def test_schema_validation_correct_dtypes(
    sample_price_df: pd.DataFrame, invalid_schema_dfs: dict[str, pd.DataFrame]
) -> None:
    """Test ID: 1.3-UNIT-007

    Verify _validate_price_schema() validates DataFrame dtypes match expected schema.

    Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac3-cache-to-parquet-with-organized-naming

    Steps:
    1. Call _validate_price_schema() with valid DataFrame (should pass)
    2. Create DataFrame with 'volume' as float64 instead of int64
    3. Call _validate_price_schema() with wrong dtype DataFrame
    4. Verify CacheError is raised
    5. Verify error message lists dtype mismatches with expected vs actual

    Expected: Validation passes for correct dtypes, raises CacheError with detailed dtype mismatch information
    """
    # Step 1: Valid DataFrame should pass validation
    try:
        _validate_price_schema(sample_price_df)
    except CacheError as e:
        pytest.fail(f"Valid DataFrame failed schema validation: {e}")

    # Step 2-3: DataFrame with wrong dtype should fail validation
    wrong_dtype_df = invalid_schema_dfs["wrong_dtype"]

    # Step 4: Verify CacheError is raised
    with pytest.raises(CacheError) as exc_info:
        _validate_price_schema(wrong_dtype_df)

    # Step 5: Verify error message is informative and lists dtype mismatches
    error_msg = str(exc_info.value)
    assert (
        "dtype mismatch" in error_msg.lower()
    ), f"Error message should mention dtype mismatch, got: {error_msg}"
    assert "volume" in error_msg, f"Error message should mention 'volume' column, got: {error_msg}"
    assert (
        "int64" in error_msg
    ), f"Error message should mention expected dtype 'int64', got: {error_msg}"
    assert (
        "float64" in error_msg
    ), f"Error message should mention actual dtype 'float64', got: {error_msg}"
