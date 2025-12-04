"""
Test ID: 1.1-UNIT-009
Story: 1.1 - Initialize Project Structure and Development Environment
Priority: P0
Test Level: Unit
Risk Coverage: SEC-001 (Environment Variable Security)

Description:
Verify .gitignore excludes .env files to prevent credential exposure.

Acceptance Criteria: AC3
Test Design Reference: docs/qa/assessments/1.1-test-design-20251203.md:82
"""

import re
from pathlib import Path


def test_1_1_unit_009(project_root: Path) -> None:
    """
    1.1-UNIT-009: Verify .gitignore excludes .env files

    Justification: Security - prevents accidental commit of API keys, database
    credentials, and other secrets.

    Expected: .gitignore contains pattern matching .env files
    Failure mode: Credentials exposed in git history
    """
    gitignore_file = project_root / ".gitignore"
    content = gitignore_file.read_text()

    # Check for .env patterns
    env_patterns = [
        r"\.env",  # .env file
        r"\.env\.local",  # .env.local
        r"\*\.env",  # *.env pattern
    ]

    has_env_exclusion = any(re.search(pattern, content) for pattern in env_patterns)

    assert has_env_exclusion, ".gitignore does not exclude .env files"
