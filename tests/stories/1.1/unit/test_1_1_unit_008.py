"""
Test ID: 1.1-UNIT-008
Story: 1.1 - Initialize Project Structure and Development Environment
Priority: P0
Test Level: Unit
Risk Coverage: None

Description:
Verify .gitignore excludes common Python artifacts (__pycache__, *.pyc, cache directories).

Acceptance Criteria: AC3
Test Design Reference: docs/qa/assessments/1.1-test-design-20251203.md:81
"""

import re
from pathlib import Path

import pytest


@pytest.mark.p0
@pytest.mark.unit
def test_1_1_unit_008(project_root: Path) -> None:
    """
    1.1-UNIT-008: Verify .gitignore excludes Python artifacts

    Justification: Critical for repo cleanliness and CI performance. Prevents
    committing build artifacts that bloat repository.

    Expected: .gitignore contains patterns for __pycache__, *.pyc, cache dirs
    Failure mode: Repository polluted with build artifacts
    """
    gitignore_file = project_root / ".gitignore"
    content = gitignore_file.read_text()

    required_patterns = [
        r"__pycache__",  # Python cache directories
        r"(\*\.pyc|\*\.py\[cod\])",  # Compiled Python files (matches *.pyc or *.py[cod])
        r"\.pytest_cache",  # pytest cache
        r"\.mypy_cache",  # mypy cache
        r"\.ruff_cache",  # ruff cache
    ]

    for pattern in required_patterns:
        assert re.search(pattern, content), f".gitignore missing pattern: {pattern}"
