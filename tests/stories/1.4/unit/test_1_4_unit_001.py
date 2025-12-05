"""Test ID: 1.4-UNIT-001

ValidationReport dataclass has all required fields.

Story: 1.4 - Build Data Quality Validation Pipeline
Priority: P0
Test Level: Unit
Risk Coverage: DATA-001
"""

from datetime import date

import pytest

from momo.data.validation import ValidationReport


@pytest.mark.p0
@pytest.mark.unit
def test_1_4_unit_001() -> None:
    """Test ID: 1.4-UNIT-001

    Verify ValidationReport dataclass has all required fields and is instantiable.

    Ref: docs/qa/assessments/1.4-test-design-20251205.md#1.4-unit-001-validationreport-dataclass-has-all-required-fields

    Steps:
    1. Import ValidationReport dataclass from validation.py
    2. Instantiate ValidationReport with all required fields
    3. Verify all fields are accessible via dot notation
    4. Verify field types match expected types

    Expected: ValidationReport instance has all 8 required fields accessible
    """
    # Step 2: Instantiate ValidationReport with all required fields
    report = ValidationReport(
        total_tickers=10,
        date_range=(date(2020, 1, 1), date(2021, 1, 1)),
        missing_data_counts={"AAPL": 5},
        date_gaps={"MSFT": [(date(2020, 6, 1), date(2020, 6, 10))]},
        adjustment_issues=["TSLA"],
        delisting_events={"ENRN": date(2001, 12, 2)},
        summary_message="Validation complete: 1 issue found",
        is_valid=False,
    )

    # Step 3: Verify all fields are accessible via dot notation
    assert report.total_tickers == 10, "total_tickers field should be accessible"
    assert report.date_range == (
        date(2020, 1, 1),
        date(2021, 1, 1),
    ), "date_range field should be accessible"
    assert report.missing_data_counts == {
        "AAPL": 5
    }, "missing_data_counts field should be accessible"
    assert report.date_gaps == {
        "MSFT": [(date(2020, 6, 1), date(2020, 6, 10))]
    }, "date_gaps field should be accessible"
    assert report.adjustment_issues == ["TSLA"], "adjustment_issues field should be accessible"
    assert report.delisting_events == {
        "ENRN": date(2001, 12, 2)
    }, "delisting_events field should be accessible"
    assert (
        report.summary_message == "Validation complete: 1 issue found"
    ), "summary_message field should be accessible"
    assert report.is_valid is False, "is_valid field should be accessible"

    # Step 4: Verify field types match expected types (mypy will verify this at type checking time)
    # At runtime, verify basic type correctness
    assert isinstance(report.total_tickers, int), "total_tickers should be int"
    assert isinstance(report.date_range, tuple), "date_range should be tuple"
    assert isinstance(report.missing_data_counts, dict), "missing_data_counts should be dict"
    assert isinstance(report.date_gaps, dict), "date_gaps should be dict"
    assert isinstance(report.adjustment_issues, list), "adjustment_issues should be list"
    assert isinstance(report.delisting_events, dict), "delisting_events should be dict"
    assert isinstance(report.summary_message, str), "summary_message should be str"
    assert isinstance(report.is_valid, bool), "is_valid should be bool"
