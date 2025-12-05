"""Test ID: 1.3-UNIT-014

Test that load_universe() returns cached data on cache hit.

Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac4-cache-loading-checks-local-parquet-before-api-query
"""

from datetime import date
from unittest.mock import patch

import pandas as pd
import pytest

from momo.data.loader import load_universe


@pytest.mark.p0
@pytest.mark.unit
def test_load_universe_returns_cached_data_on_cache_hit(
    sample_price_df: pd.DataFrame,
) -> None:
    """Test ID: 1.3-UNIT-014

    Verify load_universe() returns cached data directly when load_prices() succeeds (cache hit).

    Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac4-cache-loading-checks-local-parquet-before-api-query

    Steps:
    1. Mock cache.load_prices() to return sample DataFrame (cache hit)
    2. Mock bridge.fetch_price_data() (should NOT be called)
    3. Call load_universe() with symbols
    4. Verify bridge.fetch_price_data() was NOT called
    5. Verify returned DataFrame matches cached data

    Expected: Cached data is returned directly without calling bridge
    """
    # Step 1: Mock cache hit (return full sample DataFrame)
    with patch("momo.data.loader.cache.load_prices", return_value=sample_price_df) as mock_load:
        # Step 2: Mock bridge (should not be called)
        with patch("momo.data.loader.bridge.fetch_price_data") as mock_bridge:
            # Step 3: Call load_universe
            start_date = date(2020, 1, 1)
            end_date = date(2020, 1, 10)
            result_df = load_universe(
                symbols=["AAPL", "MSFT", "GOOGL"],
                start_date=start_date,
                end_date=end_date,
                universe="test_universe",
            )

            # Step 4: Verify bridge was NOT called (cache hit path)
            mock_bridge.assert_not_called()

            # Verify cache was checked
            mock_load.assert_called_once_with(
                universe="test_universe",
                start_date=start_date,
                end_date=end_date,
            )

            # Step 5: Verify returned DataFrame matches cached data
            pd.testing.assert_frame_equal(result_df, sample_price_df)
