"""
Test ID: 1.1-UNIT-002
Story: 1.1 - Initialize Project Structure and Development Environment
Priority: P0
Test Level: Unit
Risk Coverage: DATA-001 (WSL-Windows Path Accessibility)

Description:
Verify data/ subdirectories exist for caching prices, constituents, universes, and experiments.

Acceptance Criteria: AC1
Test Design Reference: docs/qa/assessments/1.1-test-design-20251203.md:296
"""


def test_1_1_unit_002(data_dir):
    """
    1.1-UNIT-002: Verify data/ subdirectories exist

    Justification: Critical for data caching workflow; prevents runtime errors
    when code attempts to write cached data.

    Expected: All data subdirectories exist
    Failure mode: Missing subdirectory raises AssertionError
    """
    required_subdirs = [
        "cache/prices",
        "cache/constituents",
        "cache/universes",
        "results/experiments",
    ]

    for subdir_path in required_subdirs:
        full_path = data_dir / subdir_path
        assert full_path.exists(), f"Required data subdirectory missing: {subdir_path}"
        assert full_path.is_dir(), f"Path exists but is not a directory: {subdir_path}"
