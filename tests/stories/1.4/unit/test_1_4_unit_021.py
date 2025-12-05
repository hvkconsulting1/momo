"""Test ID: 1.4-UNIT-021

Verify module docstring contains usage example with validate_prices().

Ref: docs/qa/assessments/1.4-test-design-20251205.md#1.4-unit-021

Steps:
1. Import validation module
2. Read module's __doc__ attribute
3. Verify docstring exists and is non-empty
4. Verify docstring contains "Example" or "Usage" section
5. Verify docstring contains "validate_prices" function reference
6. Verify docstring shows typical validation workflow

Expected: Module docstring contains comprehensive usage example demonstrating validate_prices()
"""

from __future__ import annotations

import pytest


@pytest.mark.p2
@pytest.mark.unit
def test_1_4_unit_021() -> None:
    """Test module docstring contains usage example.

    Verifies that validation.py module has comprehensive documentation with
    usage examples showing typical validation workflow.
    """
    # Step 1: Import validation module
    import momo.data.validation as validation_module

    # Step 2: Read module's __doc__ attribute
    docstring = validation_module.__doc__

    # Step 3: Verify docstring exists and is non-empty
    assert docstring is not None, "Module should have a docstring"
    assert len(docstring) > 0, "Module docstring should not be empty"

    # Step 4: Verify docstring contains "Example" or "Usage" section
    assert (
        "Example" in docstring or "Usage" in docstring
    ), "Module docstring should contain Example or Usage section"

    # Step 5: Verify docstring contains "validate_prices" function reference
    assert (
        "validate_prices" in docstring
    ), "Module docstring should reference validate_prices function"

    # Step 6: Verify docstring shows typical validation workflow
    # Should show imports, loading data, calling validate_prices, and inspecting report
    workflow_keywords = [
        "import",  # Shows import statements
        "load_universe" or "DataFrame",  # Shows data loading
        "validate_prices",  # Shows validation function call
        "report",  # Shows using the validation report
        "is_valid" or "summary_message",  # Shows accessing report fields
    ]

    for keyword in workflow_keywords:
        assert (
            keyword in docstring
        ), f"Module docstring should demonstrate workflow step with keyword '{keyword}'"

    # Verify docstring contains example of accessing ValidationReport fields
    report_fields = ["missing_data_counts", "date_gaps", "adjustment_issues", "delisting_events"]
    # At least 2 of the report fields should be mentioned in examples
    mentioned_fields = sum(1 for field in report_fields if field in docstring)
    assert (
        mentioned_fields >= 2
    ), f"Module docstring should show how to access report fields (found {mentioned_fields}/4)"

    # Verify docstring shows check_delisting_status function
    assert (
        "check_delisting_status" in docstring
    ), "Module docstring should reference check_delisting_status function"
