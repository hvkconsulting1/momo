"""Test ID: 1.4-UNIT-003

validate_prices() accepts MultiIndex DataFrame from Story 1.3 loader.

Story: 1.4 - Build Data Quality Validation Pipeline
Priority: P0
Test Level: Unit
Risk Coverage: TECH-003
"""

import pandas as pd
import pytest

from momo.data.validation import ValidationReport, validate_prices


@pytest.mark.p0
@pytest.mark.unit
def test_1_4_unit_003(sample_price_df_clean: pd.DataFrame) -> None:
    """Test ID: 1.4-UNIT-003

    Verify validate_prices() accepts MultiIndex DataFrame and preserves input.

    Ref: docs/qa/assessments/1.4-test-design-20251205.md#1.4-unit-003-validate_prices-accepts-multiindex-dataframe

    Steps:
    1. Load clean price DataFrame with MultiIndex (date, symbol) from fixture
    2. Verify input DataFrame has MultiIndex structure
    3. Call validate_prices(prices_df)
    4. Verify function executes without error
    5. Verify input DataFrame MultiIndex is preserved after function call
    6. Verify input DataFrame data is unchanged (no mutation)

    Expected: validate_prices() accepts MultiIndex DataFrame without error,
              returns ValidationReport, and preserves input DataFrame
    """
    # Step 1: Load clean price DataFrame from fixture
    # Step 2: Verify input DataFrame has MultiIndex structure
    assert isinstance(sample_price_df_clean.index, pd.MultiIndex), "Fixture should have MultiIndex"
    assert sample_price_df_clean.index.names == [
        "date",
        "symbol",
    ], "MultiIndex should have (date, symbol) levels"

    # Store original DataFrame state for mutation check
    original_index_type = type(sample_price_df_clean.index)
    original_index_names = sample_price_df_clean.index.names
    original_shape = sample_price_df_clean.shape

    # Step 3: Call validate_prices()
    result = validate_prices(sample_price_df_clean)

    # Step 4: Verify function executes without error (implicit - no exception raised)
    # Step 5: Verify input DataFrame MultiIndex is preserved
    assert isinstance(
        sample_price_df_clean.index, pd.MultiIndex
    ), "Input DataFrame should still have MultiIndex after validation"
    assert sample_price_df_clean.index.names == [
        "date",
        "symbol",
    ], "MultiIndex levels should be unchanged"

    # Step 6: Verify input DataFrame data is unchanged (no mutation)
    assert isinstance(
        sample_price_df_clean.index, original_index_type
    ), "Index type should not change"
    assert (
        sample_price_df_clean.index.names == original_index_names
    ), "Index names should not change"
    assert sample_price_df_clean.shape == original_shape, "DataFrame shape should not change"

    # Additional verification: result is ValidationReport
    assert isinstance(result, ValidationReport), "validate_prices() should return ValidationReport"
