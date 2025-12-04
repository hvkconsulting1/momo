"""
Test ID: 1.1-UNIT-010
Story: 1.1 - Initialize Project Structure and Development Environment
Priority: P2
Test Level: Unit
Risk Coverage: None

Description:
Verify README.md exists in project root.

Acceptance Criteria: AC5
Test Design Reference: docs/qa/assessments/1.1-test-design-20251203.md:143
"""

from pathlib import Path

import pytest


@pytest.mark.p2
@pytest.mark.unit
def test_1_1_unit_010(project_root: Path) -> None:
    """
    1.1-UNIT-010: Verify README.md exists in project root

    Justification: Documentation presence check for developer onboarding.

    Expected: README.md exists in project root
    Failure mode: Missing documentation hinders team onboarding
    """
    readme_file = project_root / "README.md"

    assert readme_file.exists(), "README.md missing in project root"
    assert readme_file.is_file(), "README.md is not a file"

    # Basic content check - must not be empty
    content = readme_file.read_text().strip()
    assert len(content) > 0, "README.md is empty"
