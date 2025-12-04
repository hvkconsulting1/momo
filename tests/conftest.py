"""
Global pytest fixtures for all story tests.
"""

from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def project_root() -> Path:
    """
    Return the absolute path to the project root directory.

    Assumes tests are located in tests/ subdirectory.
    """
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def src_dir(project_root: Path) -> Path:
    """
    Return the absolute path to the src/ directory.
    """
    return project_root / "src"


@pytest.fixture(scope="session")
def data_dir(project_root: Path) -> Path:
    """
    Return the absolute path to the data/ directory.
    """
    return project_root / "data"
