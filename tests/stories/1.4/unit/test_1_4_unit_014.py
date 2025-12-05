"""Test ID: 1.4-UNIT-014

Test get_index_constituents_at_date() with mocked bridge response.

Story: 1.4 - Build Data Quality Validation Pipeline
Priority: P0
Test Level: Unit
Risk Coverage: TECH-001
"""

from datetime import date
from typing import Any
from unittest.mock import patch

import pandas as pd
import pytest

from momo.data.validation import get_index_constituents_at_date


@pytest.mark.p0
@pytest.mark.unit
def test_1_4_unit_014(mock_bridge_response_russell1000: list[str]) -> None:
    """Test ID: 1.4-UNIT-014

    Test get_index_constituents_at_date() with mocked bridge to verify core functionality.

    Ref: docs/qa/assessments/1.4-test-design-20251205.md#1.4-unit-014

    Steps:
    1. Mock fetch_index_constituent_timeseries to return synthetic membership data
    2. Call get_index_constituents_at_date with symbols list
    3. Verify function returns list of ticker symbols that were members
    4. Verify bridge helper was called with correct parameters

    Expected: Returns list of symbols that were index members at target date
    """
    # Step 1: Mock the bridge call to return synthetic timeseries
    # Create mock DataFrame showing AAPL and MSFT as members (1), XYZ as not member (0)
    mock_timeseries_aapl = pd.DataFrame(
        {"index_constituent": [1, 1, 1]},
        index=pd.DatetimeIndex(["2010-01-04", "2010-01-05", "2010-01-06"], name="date"),
    )

    mock_timeseries_msft = pd.DataFrame(
        {"index_constituent": [1, 1, 1]},
        index=pd.DatetimeIndex(["2010-01-04", "2010-01-05", "2010-01-06"], name="date"),
    )

    mock_timeseries_xyz = pd.DataFrame(
        {"index_constituent": [0, 0, 0]},
        index=pd.DatetimeIndex(["2010-01-04", "2010-01-05", "2010-01-06"], name="date"),
    )

    # Mock the bridge function with side_effect to return different data per symbol
    def mock_fetch_side_effect(symbol: str, **kwargs: Any) -> pd.DataFrame:
        if symbol == "AAPL":
            return mock_timeseries_aapl
        elif symbol == "MSFT":
            return mock_timeseries_msft
        elif symbol == "XYZ":
            return mock_timeseries_xyz
        else:
            raise ValueError(f"Symbol {symbol} not found")

    with patch("momo.data.validation.fetch_index_constituent_timeseries") as mock_bridge:
        mock_bridge.side_effect = mock_fetch_side_effect

        # Step 2: Call get_index_constituents_at_date
        result = get_index_constituents_at_date(
            index_name="Russell 1000 Current & Past",
            target_date=date(2010, 1, 5),
            symbols=["AAPL", "MSFT", "XYZ"],
        )

        # Step 3: Verify result is list of members only (AAPL, MSFT)
        assert isinstance(result, list)
        assert len(result) == 2
        assert "AAPL" in result
        assert "MSFT" in result
        assert "XYZ" not in result  # XYZ was not a member

        # Step 4: Verify bridge was called exactly 3 times with correct parameters
        assert mock_bridge.call_count == 3

        # Verify calls included correct index name and date range (±5 days from target)
        for call in mock_bridge.call_args_list:
            call_kwargs = call.kwargs
            assert call_kwargs["index_name"] == "Russell 1000 Current & Past"
            assert call_kwargs["start_date"] == date(2009, 12, 31)  # 5 days before
            assert call_kwargs["end_date"] == date(2010, 1, 10)  # 5 days after
