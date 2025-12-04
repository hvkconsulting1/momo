"""
Test ID: 1.1-INT-004
Story: 1.1 - Initialize Project Structure and Development Environment
Priority: P1
Test Level: Integration
Risk Coverage: TECH-001 (Python 3.13 Compatibility)

Description:
Verify pyproject.toml specifies all required dependencies per tech-stack.md.

Acceptance Criteria: AC4
Test Design Reference: docs/qa/assessments/1.1-test-design-20251203.md:959
"""

from pathlib import Path

import pytest
import tomli


@pytest.mark.p1
@pytest.mark.integration
def test_1_1_int_004(project_root: Path) -> None:
    """
    1.1-INT-004: Verify pyproject.toml specifies all required dependencies

    Justification: Ensures dependency manifest is complete per architecture spec.

    Expected: All required dependencies listed in pyproject.toml
    Failure mode: Missing dependencies cause runtime import errors
    """
    pyproject_file = project_root / "pyproject.toml"

    assert pyproject_file.exists(), "pyproject.toml missing"

    with open(pyproject_file, "rb") as f:
        pyproject = tomli.load(f)

    # Extract dependencies
    dependencies = pyproject.get("project", {}).get("dependencies", [])
    dep_names = [
        dep.split("[")[0].split(">=")[0].split("~=")[0].split("==")[0] for dep in dependencies
    ]

    # Required core dependencies from tech-stack.md
    required_deps = [
        "pandas",
        "numpy",
        "pyarrow",
        "scipy",
        "matplotlib",
        "seaborn",
        "jupyter",
        "jupyterlab",
        "norgatedata",
        "structlog",
        "statsmodels",
        "tenacity",
    ]

    # Check dev dependencies (try both dependency-groups and optional-dependencies)
    dev_deps = pyproject.get("dependency-groups", {}).get("dev", [])
    if not dev_deps:
        dev_deps = pyproject.get("project", {}).get("optional-dependencies", {}).get("dev", [])
    dev_dep_names = [
        dep.split("[")[0].split(">=")[0].split("~=")[0].split("==")[0] for dep in dev_deps
    ]

    required_dev_deps = [
        "pytest",
        "pytest-cov",
        "pytest-xdist",
        "ruff",
        "mypy",
    ]

    # Verify core dependencies
    for dep in required_deps:
        assert dep in dep_names, f"Required dependency missing: {dep}"

    # Verify dev dependencies
    for dep in required_dev_deps:
        assert dep in dev_dep_names, f"Required dev dependency missing: {dep}"
