"""Test ID: 1.4-UNIT-015

Test get_index_constituents_at_date() handles bridge timeout gracefully.

Story: 1.4 - Build Data Quality Validation Pipeline
Priority: P0
Test Level: Unit
Risk Coverage: TECH-001
"""

from datetime import date
from unittest.mock import patch

import pytest

from momo.data.validation import get_index_constituents_at_date
from momo.utils.exceptions import NorgateBridgeError


@pytest.mark.p0
@pytest.mark.unit
def test_1_4_unit_015() -> None:
    """Test ID: 1.4-UNIT-015

    Test get_index_constituents_at_date() handles bridge timeout gracefully.

    Ref: docs/qa/assessments/1.4-test-design-20251205.md#1.4-unit-015

    Steps:
    1. Mock fetch_index_constituent_timeseries to raise NorgateBridgeError (timeout)
    2. Call get_index_constituents_at_date with symbols list
    3. Verify NorgateBridgeError is raised with descriptive message
    4. Verify error message contains "timeout" or similar context

    Expected: NorgateBridgeError raised with descriptive error message
    """
    # Step 1: Mock the bridge call to raise timeout error
    with patch("momo.data.validation.fetch_index_constituent_timeseries") as mock_bridge:
        mock_bridge.side_effect = NorgateBridgeError(
            "Bridge operation timed out after 30 seconds. Check if NDU is responding."
        )

        # Step 2: Call get_index_constituents_at_date and expect exception
        with pytest.raises(NorgateBridgeError) as exc_info:
            get_index_constituents_at_date(
                index_name="Russell 1000 Current & Past",
                target_date=date(2010, 1, 5),
                symbols=["AAPL", "MSFT"],
            )

        # Step 3: Verify NorgateBridgeError was raised
        # Step 4: Verify error message contains timeout information
        error_message = str(exc_info.value).lower()
        assert "timeout" in error_message or "timed out" in error_message
        assert "bridge" in error_message
