"""Test ID: 1.2-UNIT-010

Story: 1.2 - Integrate Norgate Data API via Windows Python Bridge
Priority: P0
Test Level: Unit
Risk Coverage: OPS-001 (NDU not running)

Description:
Verify that execute_norgate_code() raises clear error when NDU is not running.

Acceptance Criteria: AC4
Test Design Reference: docs/qa/assessments/1.2-test-design-20251204.md#12-unit-010-execute_norgate_code-raises-ndunotrunningerror-with-message
"""

from unittest.mock import MagicMock, patch

import pytest

from momo.data.bridge import execute_norgate_code
from momo.utils.exceptions import NDUNotRunningError


@pytest.mark.p0
@pytest.mark.unit
def test_1_2_unit_010() -> None:
    """1.2-UNIT-010: Verify execute_norgate_code() raises NDUNotRunningError with clear message

    Justification: Clear error messages reduce support burden and improve developer experience.

    Steps:
    1. Mock subprocess.run to return error indicating NDU not running
    2. Call execute_norgate_code()
    3. Verify NDUNotRunningError is raised
    4. Verify error message is actionable

    Expected: NDUNotRunningError with message "Norgate Data Updater is not running. Please start NDU."
    Failure mode: Generic error or unclear message that doesn't guide user to resolution
    """
    # Arrange - Mock subprocess to return NDU not running error
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stderr = "Error: NDU is not running"
    mock_result.stdout = ""

    # Act & Assert
    with patch("momo.data.bridge.subprocess.run", return_value=mock_result):
        with pytest.raises(NDUNotRunningError) as exc_info:
            execute_norgate_code("norgatedata.version()")

        # Verify error message is clear and actionable
        error_message = str(exc_info.value)
        assert (
            "Norgate Data Updater is not running" in error_message
        ), f"Error message should clearly state NDU is not running, got: {error_message}"
        assert (
            "start NDU" in error_message.lower() or "please start" in error_message.lower()
        ), f"Error message should guide user to start NDU, got: {error_message}"
