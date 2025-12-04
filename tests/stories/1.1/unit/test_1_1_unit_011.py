"""
Test ID: 1.1-UNIT-011
Story: 1.1 - Initialize Project Structure and Development Environment
Priority: P1
Test Level: Unit
Risk Coverage: None

Description:
Verify docs/research-log.md template exists.

Acceptance Criteria: AC6
Test Design Reference: docs/qa/assessments/1.1-test-design-20251203.md:158
"""

from pathlib import Path


def test_1_1_unit_011(project_root: Path) -> None:
    """
    1.1-UNIT-011: Verify docs/research-log.md exists

    Justification: Research documentation is core workflow artifact for data
    science project; essential for experiment tracking.

    Expected: docs/research-log.md exists
    Failure mode: No structured place to document experiments
    """
    research_log = project_root / "docs" / "research-log.md"

    assert research_log.exists(), "docs/research-log.md missing"
    assert research_log.is_file(), "docs/research-log.md is not a file"

    # Basic content check - must not be empty
    content = research_log.read_text().strip()
    assert len(content) > 0, "docs/research-log.md is empty"
