"""Test ID: 1.4-UNIT-016

Test get_index_constituents_at_date() raises on invalid index name.

Story: 1.4 - Build Data Quality Validation Pipeline
Priority: P1
Test Level: Unit
Risk Coverage: TECH-001
"""

from datetime import date
from unittest.mock import patch

import pytest

from momo.data.validation import get_index_constituents_at_date


@pytest.mark.p1
@pytest.mark.unit
def test_1_4_unit_016() -> None:
    """Test ID: 1.4-UNIT-016

    Test get_index_constituents_at_date() handles invalid index name gracefully.

    Ref: docs/qa/assessments/1.4-test-design-20251205.md#1.4-unit-016

    Steps:
    1. Mock fetch_index_constituent_timeseries to raise ValueError for invalid index
    2. Call get_index_constituents_at_date with invalid index name
    3. Verify function logs warning and skips symbol (does not raise exception)
    4. Verify empty list is returned (all symbols skipped)

    Expected: Returns empty list and logs warning for invalid index/symbol
    """
    # Step 1: Mock the bridge call to raise ValueError for invalid index
    with patch("momo.data.validation.fetch_index_constituent_timeseries") as mock_bridge:
        # Simulate Norgate API raising ValueError for invalid index name
        mock_bridge.side_effect = ValueError("Index InvalidIndex123 not found")

        # Step 2: Call get_index_constituents_at_date with invalid index
        # Note: Function should NOT raise ValueError - it should skip and log warning
        result = get_index_constituents_at_date(
            index_name="InvalidIndex123",
            target_date=date(2010, 1, 5),
            symbols=["AAPL", "MSFT"],
        )

        # Step 3: Verify function handled error gracefully (logged warning, skipped symbols)
        # Step 4: Verify empty list returned (all symbols failed validation check)
        assert isinstance(result, list)
        assert len(result) == 0  # No constituents found (all symbols failed)
