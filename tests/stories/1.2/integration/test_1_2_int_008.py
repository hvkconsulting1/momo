"""Test ID: 1.2-INT-008

Story: 1.2 - Integrate Norgate Data API via Windows Python Bridge
Priority: P0
Test Level: Integration
Risk Coverage: OPS-002 (Inadequate error messages)

Description:
User experience validation - verify error messages guide user to resolution when NDU is stopped.

Acceptance Criteria: AC4
Test Design Reference: docs/qa/assessments/1.2-test-design-20251204.md#12-int-008-verify-bridge-error-messages-are-actionable-when-ndu-stopped
"""

import pytest

from momo.data.bridge import fetch_price_data
from momo.utils.exceptions import (
    NDUNotRunningError,
    NorgateBridgeError,
    WindowsPythonNotFoundError,
)


def test_1_2_int_008() -> None:
    """1.2-INT-008: Verify bridge error messages are actionable when NDU stopped

    Justification: Error message quality directly impacts developer experience. Integration test validates real error flow.

    Steps:
    1. Attempt to fetch price data (NDU must be stopped for this test)
    2. Verify appropriate error is raised
    3. Verify error message includes:
       - Clear problem statement
       - Resolution steps
       - Authentication reminder (for NDU errors)

    Expected: Error message enables user to self-resolve without documentation lookup
    Failure mode: Generic error or technical jargon that doesn't guide user to solution

    Environment Requirements:
    - Windows environment
    - Ability to start/stop NDU (or NDU not running)

    NOTE: This test is designed to validate error messages. It will:
    - Pass if NDU is not running and error message is clear
    - Skip if Windows Python is not available
    - Provide guidance if NDU is running (manual test required)
    """
    from datetime import date

    # Act - Attempt to fetch price data
    try:
        _result = fetch_price_data(
            symbol="AAPL", start_date=date(2023, 1, 1), end_date=date(2023, 1, 31)
        )

        # If we got here, NDU is running and the fetch succeeded
        # This means we can't test the error message in this run
        pytest.skip(
            "NDU is currently running - cannot test error message when NDU stopped. "
            "To test this scenario: 1) Stop NDU, 2) Run this test, 3) Verify error message quality, 4) Restart NDU"
        )

    except WindowsPythonNotFoundError:
        # Windows Python not available - skip test
        pytest.skip(
            "Windows Python environment not available - requires Windows environment with python.exe in PATH"
        )

    except NDUNotRunningError as e:
        # This is the expected error - verify message quality
        error_message = str(e)

        # Assert - Verify error message quality
        # 1. Clear problem statement
        assert (
            "NDU" in error_message or "Norgate Data Updater" in error_message
        ), f"Error should clearly mention NDU/Norgate Data Updater, got: {error_message}"
        assert (
            "not running" in error_message.lower() or "not accessible" in error_message.lower()
        ), f"Error should clearly state NDU is not running, got: {error_message}"

        # 2. Resolution steps
        assert (
            "start" in error_message.lower() or "run" in error_message.lower()
        ), f"Error should guide user to start NDU, got: {error_message}"

        # 3. Message is actionable (user can understand what to do)
        assert (
            len(error_message) > 20
        ), f"Error message too short to be helpful, got: {error_message}"
        assert not error_message.startswith(
            "Error:"
        ), f"Error message should be user-friendly, not technical stack trace format: {error_message}"

        # Test passes - error message is clear and actionable

    except NorgateBridgeError as e:
        # Generic bridge error - check if it's a timeout (NDU stopped causes timeout)
        error_message = str(e)
        if "timed out" in error_message.lower():
            # Timeout is expected when NDU is stopped (norgatedata hangs)
            # Verify the timeout error message is actionable
            assert (
                "NDU" in error_message or "responding" in error_message.lower()
            ), f"Timeout error should mention NDU or responding, got: {error_message}"
            assert (
                len(error_message) > 20
            ), f"Timeout error message too short to be helpful, got: {error_message}"
            # Test passes - timeout with actionable message is acceptable when NDU stopped
        elif "ndu is not running" in error_message.lower():
            # It's an NDU error but wrong exception type
            pytest.fail(
                f"NDU error should raise NDUNotRunningError, not NorgateBridgeError. "
                f"Error message: {error_message}"
            )
        else:
            # Some other bridge error - skip test
            pytest.skip(f"Different bridge error encountered (not NDU-related): {error_message}")

    except Exception as e:
        # Unexpected error type
        pytest.fail(
            f"Unexpected error type when NDU not running. Expected NDUNotRunningError, got {type(e).__name__}: {e}"
        )
