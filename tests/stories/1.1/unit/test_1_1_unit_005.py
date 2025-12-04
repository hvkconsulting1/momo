"""
Test ID: 1.1-UNIT-005
Story: 1.1 - Initialize Project Structure and Development Environment
Priority: P1
Test Level: Unit
Risk Coverage: None

Description:
Verify py.typed marker file exists to enable PEP 561 type hint support.

Acceptance Criteria: AC1
Test Design Reference: docs/qa/assessments/1.1-test-design-20251203.md:455
"""


def test_1_1_unit_005(src_dir):
    """
    1.1-UNIT-005: Verify py.typed marker file exists

    Justification: Enables PEP 561 type hint support for external type checkers
    like mypy, allowing them to use this package's type annotations.

    Expected: src/momo/py.typed exists
    Failure mode: External type checkers may not recognize package type hints
    """
    momo_dir = src_dir / "momo"
    py_typed = momo_dir / "py.typed"

    assert py_typed.exists(), "py.typed marker file missing in src/momo/"
    assert py_typed.is_file(), "py.typed exists but is not a file"
