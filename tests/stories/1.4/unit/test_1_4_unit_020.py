"""Test ID: 1.4-UNIT-020

Verify ValidationReport __str__ method formats cleanly with section headers.

Ref: docs/qa/assessments/1.4-test-design-20251205.md#1.4-unit-020

Steps:
1. Create ValidationReport instance with various issues
2. Call str(report) to get formatted output
3. Verify output contains section headers: "Total Tickers:", "Date Range:", "Validation Status:"
4. Verify nested structures (dicts, lists) are formatted readably
5. Verify summary appears prominently in output

Expected: Formatted output has clear section headers, readable structure, and visible summary
"""

from __future__ import annotations

import pytest


@pytest.mark.p1
@pytest.mark.unit
def test_1_4_unit_020(mock_validation_report) -> None:  # type: ignore[no-untyped-def]
    """Test ValidationReport __str__ method formats cleanly.

    Verifies that the string representation has clear section headers,
    readable nested structure display, and a prominent summary.
    """
    # Step 1: Create ValidationReport instance (provided by fixture)
    report = mock_validation_report

    # Step 2: Call str(report) to get formatted output
    output = str(report)

    # Step 3: Verify output contains section headers
    required_headers = [
        "Total Tickers:",
        "Date Range:",
        "Missing Data:",
        "Date Gaps:",
        "Adjustment Issues:",
        "Delisting Events:",
        "Status:",
        "Summary:",
    ]

    for header in required_headers:
        assert header in output, f"Output should contain section header '{header}'"

    # Step 4: Verify nested structures are formatted readably
    # Should NOT be overwhelming - should show summary counts, not full nested dicts
    assert "10 ticker(s)" in output, "Should show delisting count in Delisting Events section"
    assert "5 ticker(s)" in output, "Should show missing data count in Missing Data section"
    assert "2 ticker(s)" in output, "Should show date gaps count in Date Gaps section"

    # Step 5: Verify summary appears prominently in output
    # Summary should be clearly labeled and visible
    assert "Summary: Validation found issues:" in output, "Summary should be clearly labeled"

    # Verify output has section delimiter (e.g., "===== Validation Report =====")
    assert "=====" in output, "Output should have visual section delimiters"

    # Verify output contains validation status (VALID or INVALID)
    assert "Status: INVALID" in output, "Output should show validation status as INVALID"

    # Verify output is multi-line (not a single long line)
    lines = output.split("\n")
    assert len(lines) >= 8, "Output should be multi-line with at least 8 lines for all sections"

    # Verify each line is reasonably short (not overwhelming)
    for line in lines:
        assert len(line) < 300, f"Each line should be < 300 chars for readability, got: {len(line)}"
