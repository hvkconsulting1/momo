"""Test ID: 1.3-UNIT-013

Test that load_universe() calls bridge only when cache misses.

Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac4-cache-loading-checks-local-parquet-before-api-query
"""

from datetime import date
from unittest.mock import patch

import pandas as pd
import pytest

from momo.data.loader import load_universe


@pytest.mark.p0
@pytest.mark.unit
def test_load_universe_calls_bridge_only_on_cache_miss(
    sample_price_df: pd.DataFrame,
) -> None:
    """Test ID: 1.3-UNIT-013

    Verify load_universe() calls bridge only when load_prices() returns None (cache miss).

    Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac4-cache-loading-checks-local-parquet-before-api-query

    Steps:
    1. Mock cache.load_prices() to return None (cache miss)
    2. Mock bridge.fetch_price_data() to return sample DataFrame
    3. Call load_universe() with symbols
    4. Verify bridge.fetch_price_data() was called (since cache missed)

    Expected: Bridge is called when cache returns None
    """
    # Step 1: Mock cache miss
    with patch("momo.data.loader.cache.load_prices", return_value=None) as mock_load:
        # Step 2: Mock bridge to return sample data
        with patch(
            "momo.data.loader.bridge.fetch_price_data",
            return_value=sample_price_df.xs("AAPL", level="symbol"),
        ) as mock_bridge:
            # Mock save_prices
            with patch("momo.data.loader.cache.save_prices"):
                # Step 3: Call load_universe
                start_date = date(2020, 1, 1)
                end_date = date(2020, 1, 10)
                load_universe(
                    symbols=["AAPL"],
                    start_date=start_date,
                    end_date=end_date,
                    universe="test_universe",
                )

                # Step 4: Verify bridge was called (cache miss path)
                assert mock_bridge.call_count == 1, "Bridge should be called once when cache misses"

                # Verify cache was checked first
                mock_load.assert_called_once()
