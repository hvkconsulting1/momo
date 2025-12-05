"""Test ID: 1.4-INT-004

Story: 1.4 - Build Data Quality Validation Pipeline
Priority: P2
Test Level: Integration
Risk Coverage: OPS-002

Manual validation report review for readability and usability.
"""

import pandas as pd
import pytest

from momo.data.validation import validate_prices


@pytest.mark.p2
@pytest.mark.integration
def test_1_4_int_004(cached_corrupt_test_data: pd.DataFrame) -> None:
    """Test ID: 1.4-INT-004

    Manual review of ValidationReport output to confirm readability and actionability.

    Ref: docs/qa/assessments/1.4-test-design-20251205.md#integration-tests

    Steps:
    1. Run validation on cached corrupt test data
    2. Print ValidationReport using str() method
    3. Manual developer review (documented in test output):
       - [ ] Summary is visible at top or bottom
       - [ ] Sections are clearly delineated
       - [ ] Nested structures are not overwhelming
       - [ ] Key metrics are easy to find
       - [ ] Report provides actionable information

    Expected: Printed report is human-readable and provides actionable data quality information

    Note: This is a semi-automated test requiring human validation.
          Findings are documented in test output for manual review.
    """
    # Step 1: Run validation on corrupt data
    result = validate_prices(cached_corrupt_test_data, check_delistings=True)

    # Step 2: Print ValidationReport using __str__() method
    print("\n" + "=" * 80)
    print("VALIDATION REPORT OUTPUT (Manual Review)")
    print("=" * 80)
    print(str(result))
    print("=" * 80)

    # Step 3: Automated checks for basic formatting requirements
    report_str = str(result)

    # Verify report contains expected section headers
    assert "Total Tickers:" in report_str, "Report should have 'Total Tickers' section"
    assert "Date Range:" in report_str, "Report should have 'Date Range' section"
    assert (
        "Validation Status:" in report_str or "Status:" in report_str
    ), "Report should have validation status section"

    # Verify report is not empty and has reasonable length
    assert len(report_str) > 100, "Report should contain substantial content"
    assert len(report_str) < 5000, "Report should not be overwhelming (< 5000 chars)"

    # Verify summary message is present and concise
    assert result.summary_message in report_str, "Summary message should appear in report"
    assert (
        len(result.summary_message) < 200
    ), f"Summary should be concise (< 200 chars), got {len(result.summary_message)}"

    # Document findings for manual review
    print("\n" + "=" * 80)
    print("MANUAL REVIEW CHECKLIST:")
    print("=" * 80)
    print("Review the printed report above and verify:")
    print("  [ ] Summary is visible at top or bottom")
    print("  [ ] Sections are clearly delineated with headers")
    print("  [ ] Nested structures (dicts, lists) are formatted readably")
    print("  [ ] Key metrics (ticker counts, date range, issue counts) are easy to find")
    print("  [ ] Report provides actionable information for debugging data quality issues")
    print("=" * 80)

    # Automated assertions passed - manual review required for full validation
    print("\nAutomated checks PASSED. Manual review required for usability assessment.")
