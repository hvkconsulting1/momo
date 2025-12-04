"""
Test ID: 1.2-INT-002
Story: 1.2 - Integrate Norgate Data API via Windows Python Bridge
Priority: P1
Test Level: Integration
Risk Coverage: TECH-002 (Windows Python not in PATH)

Description:
Verify that installed norgatedata version matches required version (1.0.74).

Acceptance Criteria: AC1
Test Design Reference: docs/qa/assessments/1.2-test-design-20251204.md:432
"""

import pytest
import structlog

from momo.data.bridge import execute_norgate_code
from momo.utils.exceptions import NorgateBridgeError, WindowsPythonNotFoundError

logger = structlog.get_logger()


def test_1_2_int_002() -> None:
    """
    1.2-INT-002: Verify norgatedata version matches requirements

    Justification: Version compatibility prevents API breaking changes.
    Ensures the installed norgatedata package is exactly version 1.0.74
    as specified in the tech stack requirements.

    Expected: Version validation passes (version == "1.0.74")
    Failure mode: If version mismatch, test provides clear upgrade instructions
    """
    # Arrange
    required_version = "1.0.74"
    code = "norgatedata.__version__"

    # Act
    try:
        actual_version = execute_norgate_code(code)
        logger.info("norgatedata_version_check", version=actual_version)

        # Assert
        assert actual_version == required_version, (
            f"norgatedata version mismatch. Expected {required_version}, got {actual_version}.\n"
            f"To upgrade: python.exe -m pip install norgatedata=={required_version}"
        )

        logger.info("version_validation_passed", required=required_version, actual=actual_version)

    except WindowsPythonNotFoundError:
        pytest.skip(
            "Windows Python (python.exe) not found in PATH - cannot verify norgatedata version"
        )
    except NorgateBridgeError as e:
        if "module named 'norgatedata'" in str(e).lower():
            pytest.skip("norgatedata not installed in Windows Python - cannot verify version")
        raise
