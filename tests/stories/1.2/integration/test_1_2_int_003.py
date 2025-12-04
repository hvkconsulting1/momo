"""
Test ID: 1.2-INT-003
Story: 1.2 - Integrate Norgate Data API via Windows Python Bridge
Priority: P0
Test Level: Integration
Risk Coverage: TECH-001 (Subprocess communication failure)

Description:
Verify end-to-end subprocess communication with simple Python code execution.
This test validates the core bridge mechanism without requiring NDU, enabling
fast feedback on basic bridge functionality.

Acceptance Criteria: AC2
Test Design Reference: docs/qa/assessments/1.2-test-design-20251204.md:458
"""

from momo.data.bridge import execute_norgate_code


def test_1_2_int_003() -> None:
    """
    1.2-INT-003: Verify bridge successfully executes simple Python code via Windows

    Justification: Validates core bridge mechanism without NDU dependency.
    Faster feedback than full Norgate tests.

    Steps:
    1. Execute simple arithmetic expression via bridge
    2. Verify result is correct
    3. Execute dictionary expression via bridge
    4. Verify JSON serialization/deserialization round-trip

    Expected: Simple Python expressions execute correctly through bridge
    Failure mode: Subprocess communication broken or JSON serialization failed
    """
    # Arrange & Act: Step 1-2 - Execute simple arithmetic
    result_arithmetic = execute_norgate_code("2 + 2")

    # Assert: Step 2 - Verify arithmetic result
    assert result_arithmetic == 4, f"Expected 4, got {result_arithmetic}"

    # Arrange & Act: Step 3 - Execute dictionary expression
    result_dict = execute_norgate_code("{'key': 'value', 'number': 42}")

    # Assert: Step 4 - Verify JSON serialization round-trip
    assert isinstance(result_dict, dict), f"Expected dict, got {type(result_dict)}"
    assert result_dict == {
        "key": "value",
        "number": 42,
    }, f"Expected {{'key': 'value', 'number': 42}}, got {result_dict}"

    # Additional validation: Test with list
    result_list = execute_norgate_code("[1, 2, 3, 'test']")
    assert result_list == [1, 2, 3, "test"], f"Expected [1, 2, 3, 'test'], got {result_list}"
