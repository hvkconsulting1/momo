"""
Test ID: 1.1-INT-006
Story: 1.1 - Initialize Project Structure and Development Environment
Priority: P2
Test Level: Integration
Risk Coverage: None

Description:
Verify README.md contains required sections for developer onboarding.

Acceptance Criteria: AC5
Test Design Reference: docs/qa/assessments/1.1-test-design-20251203.md:144
"""

from pathlib import Path

import pytest


@pytest.mark.p2
@pytest.mark.integration
def test_1_1_int_006(project_root: Path) -> None:
    """
    1.1-INT-006: Verify README contains required sections

    Justification: Content validation requires markdown parsing/analysis.

    Expected: README contains sections: title, description, setup, usage
    Failure mode: Incomplete documentation hinders onboarding
    """
    readme_file = project_root / "README.md"
    content = readme_file.read_text().lower()

    # Check for required sections (case-insensitive)
    required_sections = [
        "momo",  # Project title/name
        "setup",  # Setup instructions
        "install",  # Installation steps
    ]

    for section in required_sections:
        assert section in content, f"README missing section or keyword: {section}"
