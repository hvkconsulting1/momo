"""
Test ID: 1.1-INT-005
Story: 1.1 - Initialize Project Structure and Development Environment
Priority: P1
Test Level: Integration
Risk Coverage: TECH-001 (Python 3.13 Compatibility)

Description:
Verify core dependencies can be imported successfully.

Acceptance Criteria: AC4
Test Design Reference: docs/qa/assessments/1.1-test-design-20251203.md:1047
"""


def test_1_1_int_005() -> None:
    """
    1.1-INT-005: Verify core dependencies are importable

    Justification: Validates actual installation, not just manifest. Ensures
    Python 3.13 wheels are available and functional.

    Expected: All core dependencies import successfully
    Failure mode: Missing wheels, compilation errors, version conflicts
    """
    # Core data dependencies
    # Notebooks
    import jupyter  # type: ignore[import-untyped]  # noqa: F401
    import jupyterlab  # type: ignore[import-untyped]  # noqa: F401

    # Visualization
    import matplotlib  # noqa: F401

    # Project-specific
    import norgatedata  # noqa: F401
    import numpy
    import pandas  # type: ignore[import-untyped]
    import pyarrow  # type: ignore[import-untyped]  # noqa: F401

    # Testing
    import pytest as pytest_module  # noqa: F401
    import scipy  # type: ignore[import-untyped]  # noqa: F401
    import seaborn  # noqa: F401
    import statsmodels  # type: ignore[import-untyped]  # noqa: F401
    import structlog  # noqa: F401
    import tenacity  # noqa: F401

    # Verify versions are reasonable (basic sanity check)
    assert pandas.__version__.startswith("2.2"), f"Unexpected pandas version: {pandas.__version__}"
    assert numpy.__version__.startswith("2.1"), f"Unexpected numpy version: {numpy.__version__}"
