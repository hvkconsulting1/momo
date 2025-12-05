"""Test ID: 1.4-UNIT-019

Verify ValidationReport has concise summary_message (< 200 chars).

Ref: docs/qa/assessments/1.4-test-design-20251205.md#1.4-unit-019

Steps:
1. Access mock ValidationReport with multiple issues (5 missing data, 2 gaps, 2 adjustment, 10 delisting)
2. Verify summary_message length < 200 characters
3. Verify summary_message contains key numbers for each issue type
4. Verify summary_message is grammatically correct and readable

Expected: Summary message is concise (< 200 chars), contains issue counts, and is human-readable
"""

from __future__ import annotations

import pytest


@pytest.mark.p1
@pytest.mark.unit
def test_1_4_unit_019(mock_validation_report) -> None:  # type: ignore[no-untyped-def]
    """Test ValidationReport has concise summary_message.

    Uses mock ValidationReport with various issues to verify summary stays under 200 chars
    while still conveying all important information.
    """
    # Step 1: Access mock ValidationReport (provided by fixture)
    report = mock_validation_report

    # Step 2: Verify summary_message length < 200 characters
    summary = report.summary_message
    assert len(summary) < 200, f"Summary message too long: {len(summary)} chars (max 200)"

    # Step 3: Verify summary_message contains key numbers for each issue type
    # Expected format: "Validation found issues: 5 ticker(s) with 15 missing value(s); ..."
    assert (
        "5 ticker(s) with 15 missing value(s)" in summary
    ), "Summary should mention missing data count"
    assert "2 ticker(s) with 2 date gap(s)" in summary, "Summary should mention date gap count"
    assert (
        "2 ticker(s) with adjustment issue(s)" in summary
    ), "Summary should mention adjustment issues"
    assert "10 delisted" in summary, "Summary should mention delisting count"

    # Step 4: Verify summary_message is grammatically correct and readable
    # Should start with "Validation found issues:"
    assert summary.startswith(
        "Validation found issues:"
    ), "Summary should start with 'Validation found issues:'"

    # Should use semicolons to separate issue types for readability
    assert ";" in summary, "Summary should use semicolons to separate issue types"

    # Should contain expected keywords
    keywords = ["ticker", "missing", "gap", "adjustment", "delisted"]
    for keyword in keywords:
        assert keyword in summary.lower(), f"Summary should contain keyword '{keyword}'"
