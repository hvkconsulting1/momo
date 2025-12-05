"""Test ID: 1.4-INT-002

Story: 1.4 - Build Data Quality Validation Pipeline
Priority: P0
Test Level: Integration
Risk Coverage: DATA-001

Full validation pipeline with known-corrupt cached data.
"""

from datetime import date

import pandas as pd
import pytest

from momo.data.validation import ValidationReport, validate_prices


@pytest.mark.p0
@pytest.mark.integration
def test_1_4_int_002(cached_corrupt_test_data: pd.DataFrame) -> None:
    """Test ID: 1.4-INT-002

    Verify full validation pipeline correctly identifies all synthetic data quality issues.

    Ref: docs/qa/assessments/1.4-test-design-20251205.md#integration-tests

    Steps:
    1. Load cached corrupt test data with 4 known issue types
    2. Call validate_prices() on the DataFrame
    3. Verify ValidationReport.is_valid is False
    4. Verify AAPL missing data detected (5 NaN in close)
    5. Verify MSFT date gap detected (10-business-day gap)
    6. Verify TSLA adjustment issue detected (50% jump without dividend)
    7. Verify ENRN delisting detected (data ends 2001-12-02)
    8. Verify summary_message mentions all 4 issue types

    Expected: ValidationReport correctly identifies all 4 synthetic issues with is_valid=False
    """
    # Step 1: Data loaded via fixture (cached_corrupt_test_data)
    # Verify fixture has expected structure
    assert isinstance(cached_corrupt_test_data, pd.DataFrame)
    assert cached_corrupt_test_data.index.names == ["date", "symbol"]

    # Step 2: Call validate_prices() on corrupt data
    result = validate_prices(cached_corrupt_test_data, check_delistings=True)

    # Step 3: Verify is_valid is False (issues detected)
    assert isinstance(result, ValidationReport)
    assert result.is_valid is False, "ValidationReport should be invalid when issues detected"

    # Step 4: Verify AAPL missing data detected (5 NaN in close)
    assert "AAPL" in result.missing_data_counts, "AAPL should be flagged for missing data"
    assert (
        result.missing_data_counts["AAPL"] == 5
    ), f"Expected 5 NaN values for AAPL, got {result.missing_data_counts['AAPL']}"

    # Step 5: Verify MSFT date gap detected (10-business-day gap)
    assert "MSFT" in result.date_gaps, "MSFT should be flagged for date gaps"
    assert len(result.date_gaps["MSFT"]) > 0, "MSFT should have at least one date gap detected"
    # Gap should be from 2020-05-29 to 2020-06-15 (or similar range >= 10 business days)

    # Step 6: Verify TSLA adjustment issue detected (50% jump without dividend)
    assert "TSLA" in result.adjustment_issues, "TSLA should be flagged for adjustment issues"

    # Step 7: Verify ENRN delisting detected (data ends 2001-11-30, last business day)
    assert "ENRN" in result.delisting_events, "ENRN should be flagged as delisted"
    # Note: 2001-12-02 was a Sunday, so last business day is 2001-11-30 (Friday)
    assert result.delisting_events["ENRN"] == date(
        2001, 11, 30
    ), f"Expected ENRN delisting date 2001-11-30, got {result.delisting_events['ENRN']}"

    # Step 8: Verify summary_message mentions all issue types
    summary = result.summary_message.lower()
    assert "missing" in summary or "nan" in summary, "Summary should mention missing data issues"
    assert "gap" in summary, "Summary should mention date gap issues"
    assert "adjustment" in summary, "Summary should mention adjustment issues"
    assert "delist" in summary, "Summary should mention delisting events"
