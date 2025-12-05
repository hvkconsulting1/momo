"""Test ID: 1.3-UNIT-001

Test that load_universe() fetches single symbol via bridge on cache miss.

Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac1-fetch-ohlcv-data-using-norgatedata-api
"""

from datetime import date
from unittest.mock import patch

import pandas as pd
import pytest

from momo.data.loader import load_universe


@pytest.mark.p0
@pytest.mark.unit
def test_load_universe_fetches_via_bridge_on_cache_miss(
    sample_price_df: pd.DataFrame,
) -> None:
    """Test ID: 1.3-UNIT-001

    Verify load_universe() fetches single symbol via bridge when cache misses.

    Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac1-fetch-ohlcv-data-using-norgatedata-api

    Steps:
    1. Mock cache.load_prices() to return None (cache miss)
    2. Mock bridge.fetch_price_data() to return sample DataFrame
    3. Call load_universe() with single symbol
    4. Verify bridge.fetch_price_data() was called once with correct parameters

    Expected: Bridge is called exactly once with symbol, date range, and TOTALRETURN adjustment
    """
    # Step 1: Mock cache miss
    with patch("momo.data.loader.cache.load_prices", return_value=None) as mock_load:
        # Step 2: Mock bridge to return sample data for single symbol
        with patch(
            "momo.data.loader.bridge.fetch_price_data",
            return_value=sample_price_df.xs("AAPL", level="symbol"),
        ) as mock_bridge:
            # Mock save_prices to prevent actual file I/O
            with patch("momo.data.loader.cache.save_prices") as mock_save:
                # Step 3: Call load_universe with single symbol
                start_date = date(2020, 1, 1)
                end_date = date(2020, 1, 10)
                result_df = load_universe(
                    symbols=["AAPL"],
                    start_date=start_date,
                    end_date=end_date,
                    universe="test_universe",
                )

                # Step 4: Verify bridge was called once with correct parameters
                mock_bridge.assert_called_once()
                call_args = mock_bridge.call_args
                assert call_args.kwargs["symbol"] == "AAPL"
                assert call_args.kwargs["start_date"] == start_date
                assert call_args.kwargs["end_date"] == end_date
                assert call_args.kwargs["adjustment"] == "TOTALRETURN"

                # Verify cache was checked
                mock_load.assert_called_once_with(
                    universe="test_universe",
                    start_date=start_date,
                    end_date=end_date,
                )

                # Verify result was saved to cache
                mock_save.assert_called_once()

                # Verify result is a DataFrame
                assert isinstance(result_df, pd.DataFrame)
