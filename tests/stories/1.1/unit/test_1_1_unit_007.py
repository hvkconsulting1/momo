"""
Test ID: 1.1-UNIT-007
Story: 1.1 - Initialize Project Structure and Development Environment
Priority: P0
Test Level: Unit
Risk Coverage: OPS-001 (Git Data Directory Exclusion) - HIGH RISK

Description:
Verify .gitignore excludes data/ directory to prevent accidental commit of large data files.

Acceptance Criteria: AC3
Test Design Reference: docs/qa/assessments/1.1-test-design-20251203.md:80
"""

from pathlib import Path

import pytest


@pytest.mark.p0
@pytest.mark.unit
def test_1_1_unit_007(project_root: Path) -> None:
    """
    1.1-UNIT-007: Verify .gitignore excludes data/ directory

    Justification: HIGH RISK - Prevents accidental commit of gigabytes of cached
    market data which would bloat repository and slow git operations.

    Expected: .gitignore contains pattern matching data/ or /data/
    Failure mode: data/ files could be committed, breaking repository
    """
    gitignore_file = project_root / ".gitignore"

    assert gitignore_file.exists(), ".gitignore file missing"
    assert gitignore_file.is_file(), ".gitignore is not a file"

    content = gitignore_file.read_text()
    lines = [line.strip() for line in content.split("\n")]

    # Check for data/ pattern (with or without leading slash)
    data_patterns = ["/data/", "data/", "/data", "data"]
    has_data_exclusion = any(pattern in lines for pattern in data_patterns)

    assert has_data_exclusion, ".gitignore does not exclude data/ directory"
