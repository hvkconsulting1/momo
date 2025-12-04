"""
Test ID: 1.1-UNIT-001
Story: 1.1 - Initialize Project Structure and Development Environment
Priority: P0
Test Level: Unit
Risk Coverage: OPS-002 (Story-Based Test Organization)

Description:
Verify all top-level directories exist according to source-tree.md specification.

Acceptance Criteria: AC1
Test Design Reference: docs/qa/assessments/1.1-test-design-20251203.md:245
"""

from pathlib import Path

import pytest


@pytest.mark.p0
@pytest.mark.unit
def test_1_1_unit_001(project_root: Path) -> None:
    """
    1.1-UNIT-001: Verify all top-level directories exist

    Justification: Critical infrastructure verification; ensures project structure
    matches architecture specification.

    Expected: All directories exist
    Failure mode: Missing directory raises AssertionError with clear message
    """
    required_dirs = [
        "data",
        "src/momo",
        "notebooks",
        "docs",
        "tests",
        "scripts",
        ".github/workflows",
    ]

    for dir_path in required_dirs:
        full_path = project_root / dir_path
        assert full_path.exists(), f"Required directory missing: {dir_path}"
        assert full_path.is_dir(), f"Path exists but is not a directory: {dir_path}"
