"""Test ID: 1.3-UNIT-015

Test force_refresh=True bypasses cache.

Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac5-force-refresh-option-bypasses-cache

Steps:
1. Mock cache.load_prices to return cached DataFrame (cache exists)
2. Call load_universe() with force_refresh=True
3. Verify cache.load_prices is NOT called (cache bypassed)
4. Verify bridge.fetch_price_data IS called (fresh data fetched)
5. Verify cache.save_prices IS called (cache overwritten)

Expected: force_refresh=True bypasses cache and fetches fresh data from bridge
"""

from datetime import date
from unittest.mock import patch

import pandas as pd
import pytest

from momo.data import loader


@pytest.mark.p0
@pytest.mark.unit
def test_force_refresh_bypasses_cache(sample_price_df: pd.DataFrame) -> None:
    """Test ID: 1.3-UNIT-015

    Verify load_universe(force_refresh=True) bypasses cache and fetches fresh data.

    Story: 1.3 - Implement Data Loading and Parquet Caching
    Priority: P0
    Test Level: Unit
    Risk Coverage: DATA-003
    """
    # Setup
    symbols = ["AAPL"]
    start = date(2020, 1, 1)
    end = date(2020, 1, 31)
    universe = "test_universe"

    # Mock cached data
    cached_df = sample_price_df.copy()
    cached_df["close"] = 100.0  # Different from fresh data

    # Mock fresh data from bridge
    fresh_df = sample_price_df.copy()
    fresh_df["close"] = 200.0  # Different from cached data

    # Step 1-5: Mock and verify behavior
    with (
        patch("momo.data.loader.cache.load_prices", return_value=cached_df) as mock_load,
        patch("momo.data.loader.bridge.fetch_price_data", return_value=fresh_df) as mock_bridge,
        patch("momo.data.loader.cache.save_prices") as mock_save,
    ):
        # Call with force_refresh=True
        result_df = loader.load_universe(
            symbols=symbols,
            start_date=start,
            end_date=end,
            universe=universe,
            force_refresh=True,
        )

        # Step 3: Verify cache.load_prices was NOT called
        mock_load.assert_not_called()

        # Step 4: Verify bridge.fetch_price_data WAS called
        mock_bridge.assert_called_once_with(
            symbol="AAPL",
            start_date=start,
            end_date=end,
            adjustment="TOTALRETURN",
            timeout=30,
        )

        # Step 5: Verify cache.save_prices WAS called
        mock_save.assert_called_once()

        # Verify result is fresh data, not cached data
        assert result_df["close"].iloc[0] == 200.0  # Fresh data value
