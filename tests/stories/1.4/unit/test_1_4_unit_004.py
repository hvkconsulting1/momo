"""Test ID: 1.4-UNIT-004

validate_prices() returns ValidationReport with correct structure.

Story: 1.4 - Build Data Quality Validation Pipeline
Priority: P0
Test Level: Unit
Risk Coverage: DATA-001
"""

import pandas as pd
import pytest

from momo.data.validation import ValidationReport, validate_prices


@pytest.mark.p0
@pytest.mark.unit
def test_1_4_unit_004(sample_price_df_clean: pd.DataFrame) -> None:
    """Test ID: 1.4-UNIT-004

    Verify validate_prices() returns ValidationReport instance with is_valid=True for clean data.

    Ref: docs/qa/assessments/1.4-test-design-20251205.md#1.4-unit-004-validate_prices-returns-validationreport

    Steps:
    1. Load clean price DataFrame from fixture (no data quality issues)
    2. Call validate_prices(prices_df)
    3. Verify return value is ValidationReport instance
    4. Verify is_valid=True for clean data (no issues)
    5. Verify summary_message contains positive indication (e.g., "no issues")

    Expected: validate_prices() returns ValidationReport with is_valid=True for clean data
    """
    # Step 1: Load clean price DataFrame from fixture
    # Step 2: Call validate_prices()
    result = validate_prices(sample_price_df_clean)

    # Step 3: Verify return value is ValidationReport instance
    assert isinstance(
        result, ValidationReport
    ), "validate_prices() should return ValidationReport instance"

    # Step 4: Verify is_valid=True for clean data
    assert result.is_valid is True, "Clean data should result in is_valid=True"

    # Step 5: Verify summary_message contains positive indication
    assert (
        "no issues" in result.summary_message.lower()
    ), f"Summary message should indicate no issues for clean data, got: {result.summary_message}"

    # Additional verification: ValidationReport has expected structure for clean data
    assert result.total_tickers > 0, "total_tickers should be > 0 for non-empty dataset"
    assert len(result.date_range) == 2, "date_range should be a tuple with (start, end)"
    assert isinstance(result.missing_data_counts, dict), "missing_data_counts should be a dict"
    assert isinstance(result.date_gaps, dict), "date_gaps should be a dict"
    assert isinstance(result.adjustment_issues, list), "adjustment_issues should be a list"
    assert isinstance(result.delisting_events, dict), "delisting_events should be a dict"
