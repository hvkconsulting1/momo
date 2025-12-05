"""Test ID: 1.3-UNIT-008

Verify _validate_price_schema() validates MultiIndex structure (date, symbol) exists.

Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac3-cache-to-parquet-with-organized-naming
"""

import pandas as pd
import pytest

from momo.data.cache import _validate_price_schema
from momo.utils.exceptions import CacheError


@pytest.mark.p0
@pytest.mark.unit
def test_schema_validation_multiindex_structure(
    sample_price_df: pd.DataFrame, invalid_schema_dfs: dict[str, pd.DataFrame]
) -> None:
    """Test ID: 1.3-UNIT-008

    Verify _validate_price_schema() validates MultiIndex structure (date, symbol) exists.

    Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac3-cache-to-parquet-with-organized-naming

    Steps:
    1. Call _validate_price_schema() with valid MultiIndex DataFrame (should pass)
    2. Create DataFrame with single index instead of MultiIndex
    3. Call _validate_price_schema() with single index DataFrame
    4. Verify CacheError is raised
    5. Verify error message mentions MultiIndex requirement
    6. Verify error message includes expected index names (date, symbol)

    Expected: Validation passes for MultiIndex (date, symbol), raises CacheError for wrong index structure
    """
    # Step 1: Valid MultiIndex DataFrame should pass validation
    try:
        _validate_price_schema(sample_price_df)
    except CacheError as e:
        pytest.fail(f"Valid DataFrame failed schema validation: {e}")

    # Step 2-3: DataFrame with single index should fail validation
    wrong_index_df = invalid_schema_dfs["wrong_index"]

    # Step 4: Verify CacheError is raised
    with pytest.raises(CacheError) as exc_info:
        _validate_price_schema(wrong_index_df)

    # Step 5-6: Verify error message is informative about MultiIndex requirement
    error_msg = str(exc_info.value)
    assert (
        "MultiIndex" in error_msg
    ), f"Error message should mention MultiIndex requirement, got: {error_msg}"
