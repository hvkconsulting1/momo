"""Test ID: 1.2-UNIT-007

Story: 1.2 - Integrate Norgate Data API via Windows Python Bridge
Priority: P0
Test Level: Unit
Risk Coverage: OPS-002 (Inadequate error messages)

Description:
Verify that execute_norgate_code() logs all bridge operations with structured
logging (structlog) for debugging and observability.

Acceptance Criteria: AC2
Test Design Reference: docs/qa/assessments/1.2-test-design-20251204.md#12-unit-007-execute_norgate_code-logs-all-bridge-operations  # noqa: E501
"""

from unittest.mock import MagicMock, patch

import pytest

from momo.data.bridge import execute_norgate_code
from momo.utils.exceptions import NorgateBridgeError


@pytest.mark.p0
@pytest.mark.unit
def test_1_2_unit_007() -> None:
    """Test ID: 1.2-UNIT-007

    Verify execute_norgate_code() logs all bridge operations.

    Ref: docs/qa/assessments/1.2-test-design-20251204.md#12-unit-007-execute_norgate_code-logs-all-bridge-operations  # noqa: E501

    Steps:
    1. Configure test log capture
    2. Mock subprocess.run to succeed
    3. Call execute_norgate_code("norgatedata.version()")
    4. Assert logs contain: event="executing_norgate_code", code_length=<n>
    5. Assert logs contain: event="norgate_code_executed", success=True
    6. Test failure path: Assert error logged with full context

    Expected: All bridge operations logged with structured context for debugging
    """
    # Test case 1: Success path logging
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = '"1.0.74"'
    mock_result.stderr = ""

    with patch("momo.data.bridge.subprocess.run", return_value=mock_result):
        with patch("momo.data.bridge.logger") as mock_logger:
            # Act: Execute code
            result = execute_norgate_code("norgatedata.version()")

            # Assert: Verify success logging
            assert result == "1.0.74"

            # Check "executing" log
            executing_calls = [
                call
                for call in mock_logger.info.call_args_list
                if call[0][0] == "executing_norgate_code"
            ]
            assert len(executing_calls) >= 1
            assert "code_length" in executing_calls[0][1]

            # Check "executed" log
            executed_calls = [
                call
                for call in mock_logger.info.call_args_list
                if call[0][0] == "norgate_code_executed"
            ]
            assert len(executed_calls) >= 1
            assert executed_calls[0][1].get("success") is True

    # Test case 2: Error path logging (NDU not running)
    mock_result.returncode = 1
    mock_result.stderr = "Error: NDU is not running"

    with patch("momo.data.bridge.subprocess.run", return_value=mock_result):
        with patch("momo.data.bridge.logger") as mock_logger:
            # Act & Assert: Execute should raise error
            try:
                execute_norgate_code("test_code")
            except Exception:
                pass  # Expected to raise

            # Assert: Verify error logging occurred
            error_calls = [
                call for call in mock_logger.error.call_args_list if call[0][0] == "ndu_not_running"
            ]
            assert len(error_calls) >= 1

    # Test case 3: Timeout error logging
    import subprocess

    timeout_exception = subprocess.TimeoutExpired(cmd=["python.exe"], timeout=30)

    with patch("momo.data.bridge.subprocess.run", side_effect=timeout_exception):
        with patch("momo.data.bridge.logger") as mock_logger:
            # Act & Assert: Execute should raise error
            try:
                execute_norgate_code("test_code", timeout=30)
            except NorgateBridgeError:
                pass  # Expected

            # Assert: Verify timeout error logged
            error_calls = [
                call for call in mock_logger.error.call_args_list if call[0][0] == "bridge_timeout"
            ]
            assert len(error_calls) >= 1
            assert error_calls[0][1].get("timeout") == 30
