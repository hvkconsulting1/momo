"""Test ID: 1.2-UNIT-003

Story: 1.2 - Integrate Norgate Data API via Windows Python Bridge
Priority: P0
Test Level: Unit
Risk Coverage: DATA-001 (JSON serialization failures)

Description:
Verify that execute_norgate_code() correctly parses JSON from subprocess stdout,
handling various data types (strings, numbers, dicts, lists).

Acceptance Criteria: AC2
Test Design Reference: docs/qa/assessments/1.2-test-design-20251204.md#12-unit-003-execute_norgate_code-parses-json-from-subprocess-stdout  # noqa: E501
"""

from unittest.mock import MagicMock, patch

import pytest

from momo.data.bridge import execute_norgate_code


@pytest.mark.p0
@pytest.mark.unit
def test_1_2_unit_003() -> None:
    """Test ID: 1.2-UNIT-003

    Verify execute_norgate_code() parses JSON from subprocess stdout correctly.

    Ref: docs/qa/assessments/1.2-test-design-20251204.md#12-unit-003-execute_norgate_code-parses-json-from-subprocess-stdout  # noqa: E501

    Steps:
    1. Mock subprocess.run to return various JSON types in stdout
    2. Call execute_norgate_code()
    3. Assert result matches expected parsed value for each type
    4. Test string, number, dict, array, nested objects

    Expected: JSON correctly parsed into Python objects with type preservation
    """
    test_cases = [
        # (stdout, expected_result, description)
        ('"1.0.74"', "1.0.74", "string"),
        ("42", 42, "integer"),
        ("3.14", 3.14, "float"),
        ('{"key": "value"}', {"key": "value"}, "dict"),
        ("[1, 2, 3]", [1, 2, 3], "array"),
        (
            '{"version": "1.0.74", "date": "2023-12-04", "count": 12225}',
            {"version": "1.0.74", "date": "2023-12-04", "count": 12225},
            "nested dict",
        ),
        (
            '{"data": [1, 2, 3], "meta": {"count": 3}}',
            {"data": [1, 2, 3], "meta": {"count": 3}},
            "nested structures",
        ),
    ]

    for stdout, expected, description in test_cases:
        # Arrange: Mock subprocess with specific JSON output
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = stdout
        mock_result.stderr = ""

        with patch("momo.data.bridge.subprocess.run", return_value=mock_result):
            # Act: Parse JSON
            result = execute_norgate_code("test_code")

            # Assert: Verify correct parsing and type preservation
            assert (
                result == expected
            ), f"Failed for {description}: expected {expected}, got {result}"
