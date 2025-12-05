"""Test ID: 1.4-UNIT-005

Test that validate_prices() with clean data reports no issues.

Ref: docs/qa/assessments/1.4-test-design-20251205.md#14-unit-005-validate_prices-with-clean-data-reports-no-issues

Steps:
1. Load clean price DataFrame with no data quality issues
2. Call validate_prices(prices_df)
3. Verify ValidationReport shows no missing data
4. Verify ValidationReport shows no date gaps
5. Verify ValidationReport shows no adjustment issues
6. Verify is_valid is True

Expected: ValidationReport indicates all validations passed with no issues detected.
"""

import pandas as pd
import pytest

from momo.data.validation import validate_prices


@pytest.mark.p0
@pytest.mark.unit
def test_1_4_unit_005(sample_price_df_clean: pd.DataFrame) -> None:
    """Test validate_prices() with clean data reports no issues."""
    # Step 1: Load clean price DataFrame (via fixture)
    prices_df = sample_price_df_clean

    # Step 2: Call validate_prices()
    result = validate_prices(prices_df)

    # Step 3: Verify no missing data detected
    assert (
        len(result.missing_data_counts) == 0
    ), f"Expected no missing data, but found: {result.missing_data_counts}"

    # Step 4: Verify no date gaps detected
    assert len(result.date_gaps) == 0, f"Expected no date gaps, but found: {result.date_gaps}"

    # Step 5: Verify no adjustment issues detected
    assert (
        len(result.adjustment_issues) == 0
    ), f"Expected no adjustment issues, but found: {result.adjustment_issues}"

    # Step 6: Verify is_valid is True
    assert result.is_valid is True, f"Expected is_valid=True for clean data, got: {result.is_valid}"

    # Additional check: summary message should indicate no issues
    assert (
        "no issues" in result.summary_message.lower()
    ), f"Expected 'no issues' in summary, got: {result.summary_message}"
