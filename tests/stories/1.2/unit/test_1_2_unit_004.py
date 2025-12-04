"""Test ID: 1.2-UNIT-004

Story: 1.2 - Integrate Norgate Data API via Windows Python Bridge
Priority: P0
Test Level: Unit
Risk Coverage: DATA-002 (Norgatedata INFO messages)

Description:
Verify that execute_norgate_code() correctly parses JSON when norgatedata INFO
messages are present in stdout. Known issue from Story 1.0 - must parse only last line.

Acceptance Criteria: AC2
Test Design Reference: docs/qa/assessments/1.2-test-design-20251204.md#12-unit-004-execute_norgate_code-handles-norgatedata-info-messages  # noqa: E501
"""

from unittest.mock import MagicMock, patch

from momo.data.bridge import execute_norgate_code


def test_1_2_unit_004() -> None:
    """Test ID: 1.2-UNIT-004

    Verify execute_norgate_code() handles norgatedata INFO messages correctly.

    Ref: docs/qa/assessments/1.2-test-design-20251204.md#12-unit-004-execute_norgate_code-handles-norgatedata-info-messages  # noqa: E501

    Steps:
    1. Mock subprocess.run to return stdout with INFO messages and JSON on last line
    2. Call execute_norgate_code()
    3. Assert only last line parsed (JSON result)
    4. Assert INFO messages do not interfere with parsing

    Expected: JSON correctly extracted from last line, INFO messages ignored
    """
    # Arrange: Mock subprocess with INFO messages before JSON
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = """INFO: Norgate Data Updater connection established
INFO: Retrieving data for AAPL
INFO: Processing request
{"symbol": "AAPL", "rows": 252}"""
    mock_result.stderr = ""

    with patch("momo.data.bridge.subprocess.run", return_value=mock_result):
        # Act: Parse output with INFO messages
        result = execute_norgate_code("test_code")

        # Assert: Verify only last line (JSON) was parsed
        assert result == {"symbol": "AAPL", "rows": 252}
        assert "INFO" not in str(result)

    # Test case 2: Single line of JSON (no INFO messages)
    mock_result.stdout = '{"version": "1.0.74"}'

    with patch("momo.data.bridge.subprocess.run", return_value=mock_result):
        result = execute_norgate_code("test_code")
        assert result == {"version": "1.0.74"}

    # Test case 3: Multiple INFO messages with array result
    mock_result.stdout = """INFO: Starting operation
INFO: Processing
INFO: Complete
[1, 2, 3, 4, 5]"""

    with patch("momo.data.bridge.subprocess.run", return_value=mock_result):
        result = execute_norgate_code("test_code")
        assert result == [1, 2, 3, 4, 5]
