"""
Test ID: 1.1-INT-001
Story: 1.1 - Initialize Project Structure and Development Environment
Priority: P0
Test Level: Integration
Risk Coverage: TECH-001 (Python 3.13 Compatibility), TECH-003 (uv Maturity)

Description:
Verify uv sync resolves all dependencies successfully.

Acceptance Criteria: AC2, AC4
Test Design Reference: docs/qa/assessments/1.1-test-design-20251203.md:786
"""

import subprocess


def test_1_1_int_001(project_root):
    """
    1.1-INT-001: Verify uv sync resolves dependencies

    Justification: Critical validation of dependency manager and Python 3.13
    compatibility. Detects missing wheels or version conflicts early.

    Expected: uv sync exits with code 0, creates uv.lock
    Failure mode: Missing Python 3.13 wheels, version conflicts
    """
    result = subprocess.run(
        ["uv", "sync"],
        cwd=project_root,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, (
        f"uv sync failed with exit code {result.returncode}\n"
        f"stdout: {result.stdout}\n"
        f"stderr: {result.stderr}"
    )

    # Verify uv.lock was created
    lockfile = project_root / "uv.lock"
    assert lockfile.exists(), "uv.lock not created after successful sync"
