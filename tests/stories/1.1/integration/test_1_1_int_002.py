"""
Test ID: 1.1-INT-002
Story: 1.1 - Initialize Project Structure and Development Environment
Priority: P0
Test Level: Integration
Risk Coverage: TECH-001 (Python 3.13 Compatibility)

Description:
Verify Python 3.13 is installed and executable.

Acceptance Criteria: AC2
Test Design Reference: docs/qa/assessments/1.1-test-design-20251203.md:843
"""

import subprocess
import sys


def test_1_1_int_002():
    """
    1.1-INT-002: Verify Python 3.13 is available and executable

    Justification: Ensures correct Python version installed in environment.

    Expected: Python version is 3.13.x
    Failure mode: Wrong Python version installed
    """
    # Check current interpreter version
    assert sys.version_info.major == 3, f"Expected Python 3.x, got {sys.version_info.major}"
    assert sys.version_info.minor == 13, f"Expected Python 3.13, got 3.{sys.version_info.minor}"

    # Also verify via python --version command
    result = subprocess.run(
        ["python", "--version"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, "Python version check failed"
    assert "Python 3.13" in result.stdout, f"Expected Python 3.13, got: {result.stdout}"
