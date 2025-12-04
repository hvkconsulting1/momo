"""Test ID: 1.2-UNIT-002

Story: 1.2 - Integrate Norgate Data API via Windows Python Bridge
Priority: P0
Test Level: Unit
Risk Coverage: TECH-001 (Subprocess communication failure)

Description:
Verify that execute_norgate_code() constructs the correct subprocess command with
proper Python code wrapper including JSON serialization.

Acceptance Criteria: AC2
Test Design Reference: docs/qa/assessments/1.2-test-design-20251204.md#12-unit-002-execute_norgate_code-constructs-subprocess-call-correctly  # noqa: E501
"""

from unittest.mock import MagicMock, patch

from momo.data.bridge import execute_norgate_code


def test_1_2_unit_002() -> None:
    """Test ID: 1.2-UNIT-002

    Verify execute_norgate_code() constructs subprocess call correctly.

    Ref: docs/qa/assessments/1.2-test-design-20251204.md#12-unit-002-execute_norgate_code-constructs-subprocess-call-correctly  # noqa: E501

    Steps:
    1. Mock subprocess.run to capture call arguments
    2. Call execute_norgate_code("norgatedata.version()")
    3. Assert subprocess.run called with ['python.exe', '-c', <wrapper_code>]
    4. Assert wrapper includes: import json, import norgatedata, print(json.dumps(result))

    Expected: Subprocess called with correctly formatted Python code including JSON wrapper
    """
    # Arrange: Mock subprocess to capture arguments
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = '"1.0.74"'
    mock_result.stderr = ""

    with patch("momo.data.bridge.subprocess.run", return_value=mock_result) as mock_run:
        # Act: Call execute_norgate_code
        execute_norgate_code("norgatedata.version()")

        # Assert: Verify subprocess.run was called with correct arguments
        assert mock_run.call_count == 1
        call_args = mock_run.call_args

        # Check command structure
        cmd = call_args[0][0]
        assert cmd[0] == "python.exe"
        assert cmd[1] == "-c"

        # Check wrapper code contains required elements
        wrapper_code = cmd[2]
        assert "import json" in wrapper_code
        assert "import norgatedata" in wrapper_code
        assert "norgatedata.version()" in wrapper_code
        assert "print(json.dumps(result" in wrapper_code

        # Check subprocess options
        kwargs = call_args[1]
        assert kwargs["capture_output"] is True
        assert kwargs["text"] is True
        assert kwargs["timeout"] == 30
