"""Test ID: 1.4-UNIT-017

Test get_index_constituents_at_date() retrieves all constituents when symbols=None.

Story: 1.4 - Build Data Quality Validation Pipeline
Priority: P0
Test Level: Unit
Risk Coverage: TECH-001, AC-4
"""

from datetime import date
from unittest.mock import patch

import pandas as pd
import pytest

from momo.data.validation import get_index_constituents_at_date


@pytest.mark.p0
@pytest.mark.unit
def test_1_4_unit_017() -> None:
    """Test ID: 1.4-UNIT-017

    Test get_index_constituents_at_date() retrieves ALL constituents when symbols=None.

    This tests the new functionality that fetches all symbols from a watchlist
    and then checks membership for each symbol.

    Steps:
    1. Mock fetch_watchlist_symbols to return a list of 5 symbols
    2. Mock fetch_index_constituent_timeseries to return membership data
    3. Call get_index_constituents_at_date WITHOUT symbols parameter
    4. Verify watchlist fetch was called
    5. Verify constituent checks were performed for all symbols
    6. Verify only actual members are returned

    Expected: Function retrieves watchlist symbols and filters to members only
    """
    # Step 1: Mock fetch_watchlist_symbols to return test symbols
    mock_watchlist_symbols = ["AAPL", "MSFT", "GOOGL", "XYZ", "ABC"]

    # Step 2: Mock constituent timeseries - AAPL, MSFT, GOOGL are members; XYZ, ABC are not
    def mock_constituent_timeseries(symbol: str, **kwargs: object) -> pd.DataFrame:
        # Return membership based on symbol
        if symbol in ["AAPL", "MSFT", "GOOGL"]:
            is_member = 1
        else:
            is_member = 0

        return pd.DataFrame(
            {"index_constituent": [is_member, is_member, is_member]},
            index=pd.DatetimeIndex(["2010-01-04", "2010-01-05", "2010-01-06"], name="date"),
        )

    with (
        patch("momo.data.validation.fetch_watchlist_symbols") as mock_fetch_watchlist,
        patch("momo.data.validation.fetch_index_constituent_timeseries") as mock_fetch_constituent,
    ):
        # Set up mocks
        mock_fetch_watchlist.return_value = mock_watchlist_symbols
        mock_fetch_constituent.side_effect = mock_constituent_timeseries

        # Step 3: Call get_index_constituents_at_date WITHOUT symbols parameter
        result = get_index_constituents_at_date(
            index_name="Russell 1000 Current & Past",
            target_date=date(2010, 1, 5),
            # symbols=None (default) - should trigger watchlist fetch
        )

        # Step 4: Verify fetch_watchlist_symbols was called with correct index name
        mock_fetch_watchlist.assert_called_once()
        call_kwargs = mock_fetch_watchlist.call_args.kwargs
        assert call_kwargs["watchlist_name"] == "Russell 1000 Current & Past"

        # Step 5: Verify constituent checks were performed for all 5 symbols
        assert mock_fetch_constituent.call_count == 5

        # Step 6: Verify only members are returned (AAPL, MSFT, GOOGL)
        assert isinstance(result, list)
        assert len(result) == 3
        assert "AAPL" in result
        assert "MSFT" in result
        assert "GOOGL" in result
        assert "XYZ" not in result
        assert "ABC" not in result
