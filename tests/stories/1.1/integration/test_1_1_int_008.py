"""
Test ID: 1.1-INT-008
Story: 1.1 - Initialize Project Structure and Development Environment
Priority: P1
Test Level: Integration
Risk Coverage: None

Description:
Verify all momo subpackages are importable.

Acceptance Criteria: AC7
Test Design Reference: docs/qa/assessments/1.1-test-design-20251203.md:1213
"""

import sys
from pathlib import Path

import pytest


@pytest.mark.p1
@pytest.mark.integration
def test_1_1_int_008(project_root: Path) -> None:
    """
    1.1-INT-008: Verify subpackages are importable

    Justification: Validates complete package hierarchy with __init__.py files.

    Expected: All subpackages can be imported
    Failure mode: Missing __init__.py prevents layer imports
    """
    # Ensure src/ is in sys.path
    src_path = project_root / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    subpackages = [
        "momo.data",
        "momo.signals",
        "momo.portfolio",
        "momo.backtest",
        "momo.utils",
    ]

    for subpkg in subpackages:
        try:
            __import__(subpkg)
        except ImportError as e:
            pytest.fail(f"Failed to import {subpkg}: {e}")
