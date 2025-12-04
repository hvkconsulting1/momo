"""Test ID: 1.2-UNIT-006

Story: 1.2 - Integrate Norgate Data API via Windows Python Bridge
Priority: P0
Test Level: Unit
Risk Coverage: PERF-001 (Subprocess timeout)

Description:
Verify that execute_norgate_code() raises error when subprocess exceeds timeout,
preventing hanging operations.

Acceptance Criteria: AC2
Test Design Reference: docs/qa/assessments/1.2-test-design-20251204.md#12-unit-006-execute_norgate_code-raises-norgatebridgeerror-on-timeout  # noqa: E501
"""

import subprocess
from unittest.mock import patch

import pytest

from momo.data.bridge import execute_norgate_code
from momo.utils.exceptions import NorgateBridgeError


@pytest.mark.p0
@pytest.mark.unit
def test_1_2_unit_006() -> None:
    """Test ID: 1.2-UNIT-006

    Verify execute_norgate_code() raises NorgateBridgeError on timeout.

    Ref: docs/qa/assessments/1.2-test-design-20251204.md#12-unit-006-execute_norgate_code-raises-norgatebridgeerror-on-timeout  # noqa: E501

    Steps:
    1. Mock subprocess.run to raise subprocess.TimeoutExpired
    2. Call execute_norgate_code(timeout=30)
    3. Assert NorgateBridgeError raised with message mentioning timeout
    4. Assert timeout value included in error message

    Expected: Error raised mentioning timeout duration and NDU responsiveness
    """
    # Arrange: Mock subprocess to raise TimeoutExpired
    timeout_exception = subprocess.TimeoutExpired(cmd=["python.exe", "-c", "test"], timeout=30)

    with patch("momo.data.bridge.subprocess.run", side_effect=timeout_exception):
        # Act & Assert: Verify correct exception with timeout info
        with pytest.raises(NorgateBridgeError) as exc_info:
            execute_norgate_code("test_code", timeout=30)

        # Verify error message mentions timeout and provides context
        error_msg = str(exc_info.value)
        assert "timeout" in error_msg.lower() or "timed out" in error_msg.lower()
        assert "30" in error_msg
        assert "ndu" in error_msg.lower() or "respond" in error_msg.lower()

    # Test case 2: Different timeout value
    timeout_exception = subprocess.TimeoutExpired(cmd=["python.exe", "-c", "test"], timeout=60)

    with patch("momo.data.bridge.subprocess.run", side_effect=timeout_exception):
        with pytest.raises(NorgateBridgeError) as exc_info:
            execute_norgate_code("test_code", timeout=60)

        error_msg = str(exc_info.value)
        assert "60" in error_msg
