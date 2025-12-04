"""
Test ID: 1.2-UNIT-011
Story: 1.2 - Integrate Norgate Data API via Windows Python Bridge
Priority: P0
Test Level: Unit
Risk Coverage: OPS-001 (NDU not running)

Description:
Verify that check_ndu_status() proactively detects when NDU is not running.

Acceptance Criteria: AC4
Test Design Reference: docs/qa/assessments/1.2-test-design-20251204.md#1.2-unit-011-check_ndu_status-detects-ndu-not-running
"""

from unittest.mock import patch

from momo.data.bridge import check_ndu_status
from momo.utils.exceptions import NDUNotRunningError


def test_1_2_unit_011() -> None:
    """Test ID: 1.2-UNIT-011

    Verify check_ndu_status() detects NDU not running.

    Ref: docs/qa/assessments/1.2-test-design-20251204.md#1.2-unit-011-check_ndu_status-detects-ndu-not-running

    Steps:
    1. Mock execute_norgate_code() to raise NDUNotRunningError
    2. Call check_ndu_status()
    3. Assert function returns False
    4. Mock execute_norgate_code() to succeed
    5. Call check_ndu_status()
    6. Assert function returns True

    Expected: Boolean result correctly indicates NDU availability
    """
    # Steps 1-3: NDU not running scenario
    with patch("momo.data.bridge.execute_norgate_code") as mock_execute:
        # Step 1: Mock to raise NDUNotRunningError
        mock_execute.side_effect = NDUNotRunningError(
            "Norgate Data Updater is not running. Please start NDU."
        )

        # Step 2: Call check_ndu_status
        result = check_ndu_status()

        # Step 3: Assert returns False
        assert (
            result is False
        ), f"check_ndu_status() should return False when NDU not running, got {result}"

        # Verify execute_norgate_code was called
        assert mock_execute.called, "execute_norgate_code should be called"

        # Verify correct code was executed (NDU databases check)
        call_args = mock_execute.call_args
        code_param = call_args[0][0]
        assert "norgatedata.databases()" in code_param, (
            f"Should call norgatedata.databases()\n" f"Actual code: {code_param}"
        )

    # Steps 4-6: NDU running scenario
    with patch("momo.data.bridge.execute_norgate_code") as mock_execute:
        # Step 4: Mock to succeed (return list of databases)
        mock_execute.return_value = ["US EOD"]

        # Step 5: Call check_ndu_status
        result = check_ndu_status()

        # Step 6: Assert returns True
        assert (
            result is True
        ), f"check_ndu_status() should return True when NDU running, got {result}"


def test_1_2_unit_011_timeout_custom() -> None:
    """Test ID: 1.2-UNIT-011 (variant: custom timeout)

    Verify check_ndu_status() passes custom timeout to execute_norgate_code.

    Expected: Timeout parameter passed correctly
    """
    # Arrange: Mock execute_norgate_code
    with patch("momo.data.bridge.execute_norgate_code") as mock_execute:
        mock_execute.return_value = ["US EOD"]

        # Act: Call with custom timeout
        result = check_ndu_status(timeout=5)

        # Assert: Verify timeout passed
        assert result is True
        call_args = mock_execute.call_args
        assert (
            call_args[1]["timeout"] == 5
        ), f"Timeout should be 5 seconds, got {call_args[1].get('timeout')}"


def test_1_2_unit_011_generic_exception() -> None:
    """Test ID: 1.2-UNIT-011 (variant: generic exception)

    Verify check_ndu_status() returns False for generic exceptions.

    Expected: Returns False and logs warning for unexpected errors
    """
    # Arrange: Mock to raise generic exception
    with patch("momo.data.bridge.execute_norgate_code") as mock_execute:
        mock_execute.side_effect = Exception("Unexpected error")

        # Act: Call check_ndu_status
        result = check_ndu_status()

        # Assert: Should return False for any exception
        assert (
            result is False
        ), f"check_ndu_status() should return False for generic exceptions, got {result}"


def test_1_2_unit_011_default_timeout() -> None:
    """Test ID: 1.2-UNIT-011 (variant: default timeout)

    Verify check_ndu_status() uses default timeout of 10 seconds.

    Expected: Default timeout of 10 seconds used when not specified
    """
    # Arrange: Mock execute_norgate_code
    with patch("momo.data.bridge.execute_norgate_code") as mock_execute:
        mock_execute.return_value = ["US EOD"]

        # Act: Call without timeout parameter
        result = check_ndu_status()

        # Assert: Verify default timeout
        assert result is True
        call_args = mock_execute.call_args
        assert (
            call_args[1]["timeout"] == 10
        ), f"Default timeout should be 10 seconds, got {call_args[1].get('timeout')}"
