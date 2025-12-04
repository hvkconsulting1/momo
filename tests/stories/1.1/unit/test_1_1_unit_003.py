"""
Test ID: 1.1-UNIT-003
Story: 1.1 - Initialize Project Structure and Development Environment
Priority: P0
Test Level: Unit
Risk Coverage: OPS-002 (Story-Based Test Organization)

Description:
Verify src/momo/ package structure exists with all required subdirectories.

Acceptance Criteria: AC1
Test Design Reference: docs/qa/assessments/1.1-test-design-20251203.md:345
"""



def test_1_1_unit_003(src_dir):
    """
    1.1-UNIT-003: Verify src/momo/ package structure exists

    Justification: Core package structure must be correct for Python imports
    and package discovery.

    Expected: All momo subdirectories exist
    Failure mode: Missing subdirectory prevents package imports
    """
    momo_dir = src_dir / "momo"

    # Verify momo package directory
    assert momo_dir.exists(), "src/momo/ directory missing"
    assert momo_dir.is_dir(), "src/momo/ is not a directory"

    # Verify subdirectories
    required_subdirs = [
        "data",
        "signals",
        "portfolio",
        "backtest",
        "utils",
    ]

    for subdir in required_subdirs:
        full_path = momo_dir / subdir
        assert full_path.exists(), f"Required momo subdirectory missing: {subdir}"
        assert full_path.is_dir(), f"Path exists but is not a directory: {subdir}"
