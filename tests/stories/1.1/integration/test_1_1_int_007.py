"""
Test ID: 1.1-INT-007
Story: 1.1 - Initialize Project Structure and Development Environment
Priority: P0
Test Level: Integration
Risk Coverage: None

Description:
Verify 'import momo' succeeds from project root.

Acceptance Criteria: AC7
Test Design Reference: docs/qa/assessments/1.1-test-design-20251203.md:1161
"""

import sys

import pytest


def test_1_1_int_007(project_root):
    """
    1.1-INT-007: Verify 'import momo' succeeds from project root

    Justification: Critical validation of package structure. Tests that src/
    layout allows imports.

    Expected: import momo succeeds without error
    Failure mode: Package not discoverable, breaking all future development
    """
    # Ensure src/ is in sys.path
    src_path = project_root / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    try:
        import momo

        # Verify momo has __file__ attribute (is a real package)
        assert hasattr(momo, "__file__"), "momo package has no __file__ attribute"

    except ImportError as e:
        pytest.fail(f"Failed to import momo: {e}")
