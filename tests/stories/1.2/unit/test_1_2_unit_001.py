"""Test ID: 1.2-UNIT-001

Story: 1.2 - Integrate Norgate Data API via Windows Python Bridge
Priority: P0
Test Level: Unit
Risk Coverage: OPS-001 (NDU not running)

Description:
Verify that execute_norgate_code() raises a clear error when norgatedata package
is not installed in Windows Python environment.

Acceptance Criteria: AC1
Test Design Reference: docs/qa/assessments/1.2-test-design-20251204.md#12-unit-001-bridge-handles-norgatedata-import-error  # noqa: E501
"""

from unittest.mock import MagicMock, patch

import pytest

from momo.data.bridge import execute_norgate_code
from momo.utils.exceptions import NorgateBridgeError


def test_1_2_unit_001() -> None:
    """Test ID: 1.2-UNIT-001

    Verify bridge handles norgatedata import error with clear message.

    Ref: docs/qa/assessments/1.2-test-design-20251204.md#12-unit-001-bridge-handles-norgatedata-import-error  # noqa: E501

    Steps:
    1. Mock subprocess.run to return stderr with ModuleNotFoundError for norgatedata
    2. Call execute_norgate_code()
    3. Verify NorgateBridgeError raised with message mentioning norgatedata installation

    Expected: Clear error message guiding user to install norgatedata==1.0.74
    """
    # Arrange: Mock subprocess to return norgatedata import error
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stderr = "ModuleNotFoundError: No module named 'norgatedata'"
    mock_result.stdout = ""

    with patch("momo.data.bridge.subprocess.run", return_value=mock_result):
        # Act & Assert: Verify correct exception with helpful message
        with pytest.raises(NorgateBridgeError) as exc_info:
            execute_norgate_code("norgatedata.version()")

        # Verify error message mentions norgatedata installation
        error_msg = str(exc_info.value)
        assert "norgatedata" in error_msg.lower()
        assert "1.0.74" in error_msg
        assert "pip install" in error_msg.lower()
