"""
Test ID: 1.1-INT-003
Story: 1.1 - Initialize Project Structure and Development Environment
Priority: P1
Test Level: Integration
Risk Coverage: OPS-001 (Git Data Directory Exclusion) - HIGH RISK

Description:
Functional test that data/ files are not tracked by git after creating test file.

Acceptance Criteria: AC3
Test Design Reference: docs/qa/assessments/1.1-test-design-20251203.md:894
"""

import subprocess
from pathlib import Path

import pytest


def test_1_1_int_003(project_root: Path, data_dir: Path) -> None:
    """
    1.1-INT-003: Verify data/ files are not tracked by git

    Justification: Functional test of gitignore configuration. Ensures data/
    exclusion actually works, not just that .gitignore has the right text.

    Expected: Test file in data/ is not shown by git status
    Failure mode: .gitignore pattern not working as expected
    """
    # Create test file in data/
    test_file = data_dir / "test-file.txt"
    test_file.write_text("This file should not be tracked by git")

    try:
        # Run git status --porcelain to check untracked files
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=project_root,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, "git status failed"

        # Check that test file is NOT in output
        assert "data/test-file.txt" not in result.stdout, (
            "data/test-file.txt appears in git status - .gitignore not working"
        )

    finally:
        # Clean up test file
        if test_file.exists():
            test_file.unlink()
