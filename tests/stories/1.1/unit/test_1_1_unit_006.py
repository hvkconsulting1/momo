"""
Test ID: 1.1-UNIT-006
Story: 1.1 - Initialize Project Structure and Development Environment
Priority: P0
Test Level: Unit
Risk Coverage: TECH-001 (Python 3.13 Compatibility)

Description:
Verify .python-version file exists and specifies Python 3.13.

Acceptance Criteria: AC2
Test Design Reference: docs/qa/assessments/1.1-test-design-20251203.md:64
"""

from pathlib import Path


def test_1_1_unit_006(project_root: Path) -> None:
    """
    1.1-UNIT-006: Verify .python-version file contains '3.13'

    Justification: Ensures tools (uv, pyenv) detect correct Python version.

    Expected: .python-version exists and contains exactly '3.13'
    Failure mode: Tools may use wrong Python version, causing compatibility issues
    """
    python_version_file = project_root / ".python-version"

    assert python_version_file.exists(), ".python-version file missing"
    assert python_version_file.is_file(), ".python-version is not a file"

    content = python_version_file.read_text().strip()
    assert content == "3.13", f"Expected Python version '3.13', found '{content}'"
