"""Test ID: 1.2-INT-001

Story: 1.2 - Integrate Norgate Data API via Windows Python Bridge
Priority: P0
Test Level: Integration
Risk Coverage: TECH-001 (Subprocess communication failure)

Description:
Verify that norgatedata package can be imported through the Windows Python bridge in actual environment.

Acceptance Criteria: AC1
Test Design Reference: docs/qa/assessments/1.2-test-design-20251204.md#12-int-001-verify-norgatedata-package-is-importable-via-bridge
"""

import pytest

from momo.data.bridge import execute_norgate_code


@pytest.mark.p0
@pytest.mark.integration
def test_1_2_int_001() -> None:
    """1.2-INT-001: Verify norgatedata package is importable via bridge

    Justification: Package availability is prerequisite. Integration test validates actual environment setup.

    Steps:
    1. Call execute_norgate_code() with import norgatedata statement
    2. Verify result contains version string
    3. Verify no import errors

    Expected: norgatedata successfully imported and version retrieved
    Failure mode: ImportError, FileNotFoundError, or other subprocess communication failure

    Environment Requirements:
    - Windows Python with norgatedata 1.0.74 installed
    - python.exe in WSL PATH
    """
    # Act - Import norgatedata and get version via bridge
    try:
        result = execute_norgate_code("norgatedata.__version__")
    except FileNotFoundError:
        pytest.skip("Windows Python (python.exe) not found in PATH - requires Windows environment")
    except Exception as e:
        # If it's a known environment error, skip the test
        error_msg = str(e).lower()
        if "python.exe" in error_msg or "not found" in error_msg:
            pytest.skip(f"Windows Python environment not available: {e}")
        # Re-raise if it's an unexpected error
        raise

    # Assert - Verify version string returned
    assert result is not None, "Version result should not be None"
    assert isinstance(result, str), f"Version should be a string, got {type(result)}"
    assert len(result) > 0, "Version string should not be empty"

    # Version should look like "1.0.74" or similar
    # Don't enforce exact version to avoid test brittleness
    assert "." in result, f"Version string should contain dots (e.g., '1.0.74'), got: {result}"
