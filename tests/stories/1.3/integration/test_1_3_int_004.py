"""Test ID: 1.3-INT-004

Test force-refresh fetches and overwrites cache.

Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac5-force-refresh-option-bypasses-cache

Steps:
1. Create initial cached DataFrame with known values
2. Save initial cache to disk
3. Call load_universe() with force_refresh=True and mock fresh data with different values
4. Verify cache file is overwritten with fresh data
5. Load cache again and verify it contains fresh data values

Expected: force_refresh=True fetches fresh data and overwrites existing cache
"""

from datetime import date
from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest

from momo.data import cache, loader


@pytest.mark.p1
@pytest.mark.integration
def test_force_refresh_overwrites_cache(
    sample_price_df: pd.DataFrame, temp_cache_dir: Path
) -> None:
    """Test ID: 1.3-INT-004

    Verify force_refresh=True fetches fresh data and overwrites existing cache.

    Story: 1.3 - Implement Data Loading and Parquet Caching
    Priority: P1
    Test Level: Integration
    Risk Coverage: DATA-003
    """
    # Setup
    symbols = ["AAPL"]
    start = date(2020, 1, 1)
    end = date(2020, 1, 10)
    universe = "test_universe"

    # Step 1: Create initial cached DataFrame with known values
    initial_df = sample_price_df.copy()
    initial_df["close"] = 100.0

    # Step 2: Save initial cache to disk
    # Patch get_cache_path to use temp directory
    def mock_get_cache_path(universe_param: str, start_date: date, end_date: date) -> Path:
        filename = f"{universe_param}_{start_date.isoformat()}_{end_date.isoformat()}.parquet"
        return temp_cache_dir / filename

    with (
        patch("momo.data.cache.get_cache_path", side_effect=mock_get_cache_path),
        patch("momo.data.loader.cache.get_cache_path", side_effect=mock_get_cache_path),
    ):
        # Save initial cache
        saved_path = cache.save_prices(
            df=initial_df,
            universe=universe,
            start_date=start,
            end_date=end,
        )

        # Verify initial cache exists
        assert saved_path.exists()
        loaded_initial = cache.load_prices(
            universe=universe,
            start_date=start,
            end_date=end,
        )
        assert loaded_initial is not None
        assert loaded_initial["close"].iloc[0] == 100.0

        # Step 3: Create fresh data with different values
        fresh_df = sample_price_df.copy()
        fresh_df["close"] = 200.0

        # Mock bridge to return fresh data
        with patch("momo.data.loader.bridge.fetch_price_data", return_value=fresh_df):
            # Call load_universe with force_refresh=True
            result_df = loader.load_universe(
                symbols=symbols,
                start_date=start,
                end_date=end,
                universe=universe,
                force_refresh=True,
            )

            # Step 4: Verify result contains fresh data
            assert result_df["close"].iloc[0] == 200.0

        # Step 5: Load cache again and verify it was overwritten with fresh data
        reloaded_df = cache.load_prices(
            universe=universe,
            start_date=start,
            end_date=end,
        )
        assert reloaded_df is not None
        assert reloaded_df["close"].iloc[0] == 200.0  # Fresh data, not initial (100.0)
