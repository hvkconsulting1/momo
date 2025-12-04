"""
Test ID: 1.1-UNIT-004
Story: 1.1 - Initialize Project Structure and Development Environment
Priority: P1
Test Level: Unit
Risk Coverage: None

Description:
Verify all package directories contain __init__.py files for Python discoverability.

Acceptance Criteria: AC1
Test Design Reference: docs/qa/assessments/1.1-test-design-20251203.md:402
"""



def test_1_1_unit_004(src_dir):
    """
    1.1-UNIT-004: Verify all __init__.py files exist

    Justification: Ensures package discoverability by Python interpreter.

    Expected: __init__.py exists in momo/ and all subdirectories
    Failure mode: Missing __init__.py prevents package imports
    """
    momo_dir = src_dir / "momo"

    # Package directories requiring __init__.py
    package_dirs = [
        momo_dir,
        momo_dir / "data",
        momo_dir / "signals",
        momo_dir / "portfolio",
        momo_dir / "backtest",
        momo_dir / "utils",
    ]

    for pkg_dir in package_dirs:
        init_file = pkg_dir / "__init__.py"
        assert init_file.exists(), f"Missing __init__.py in {pkg_dir.relative_to(src_dir)}"
        assert init_file.is_file(), f"__init__.py is not a file in {pkg_dir.relative_to(src_dir)}"
