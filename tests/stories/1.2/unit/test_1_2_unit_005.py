"""Test ID: 1.2-UNIT-005

Story: 1.2 - Integrate Norgate Data API via Windows Python Bridge
Priority: P0
Test Level: Unit
Risk Coverage: TECH-002 (Windows Python not in PATH)

Description:
Verify that execute_norgate_code() raises clear error when Windows Python (python.exe)
is not found in PATH.

Acceptance Criteria: AC2
Test Design Reference: docs/qa/assessments/1.2-test-design-20251204.md#12-unit-005-execute_norgate_code-raises-windowspythonnotfounderror  # noqa: E501
"""

from unittest.mock import patch

import pytest

from momo.data.bridge import execute_norgate_code
from momo.utils.exceptions import WindowsPythonNotFoundError


def test_1_2_unit_005() -> None:
    """Test ID: 1.2-UNIT-005

    Verify execute_norgate_code() raises WindowsPythonNotFoundError.

    Ref: docs/qa/assessments/1.2-test-design-20251204.md#12-unit-005-execute_norgate_code-raises-windowspythonnotfounderror  # noqa: E501

    Steps:
    1. Mock subprocess.run to raise FileNotFoundError
    2. Call execute_norgate_code()
    3. Assert WindowsPythonNotFoundError raised
    4. Assert error message includes troubleshooting steps (check PATH, install Python)

    Expected: Clear error with actionable resolution about Windows Python installation
    """
    # Arrange: Mock subprocess to raise FileNotFoundError
    with patch(
        "momo.data.bridge.subprocess.run", side_effect=FileNotFoundError("python.exe not found")
    ):
        # Act & Assert: Verify correct exception with helpful message
        with pytest.raises(WindowsPythonNotFoundError) as exc_info:
            execute_norgate_code("test_code")

        # Verify error message contains troubleshooting guidance
        error_msg = str(exc_info.value)
        assert "python.exe" in error_msg.lower()
        assert "path" in error_msg.lower() or "PATH" in error_msg
        assert "windows python" in error_msg.lower()
