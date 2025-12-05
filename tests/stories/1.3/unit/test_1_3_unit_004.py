"""Test TOTALRETURN adjustment passed to bridge.

Test ID: 1.3-UNIT-004
Story: 1.3 - Implement Data Loading and Parquet Caching
Priority: P0
Test Level: Unit
Risk Coverage: DATA-001

Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac2-fetched-data-includes-adjustment-factors-totalreturn

Steps:
1. Mock cache.load_prices() to return None (cache miss)
2. Mock bridge.fetch_price_data() to capture call arguments
3. Mock cache.save_prices() to avoid file I/O
4. Call load_universe() with test symbols
5. Verify bridge.fetch_price_data() was called with adjustment="TOTALRETURN"
6. Verify adjustment parameter is passed for all symbol fetches

Expected: All bridge calls include adjustment="TOTALRETURN" parameter for
dividend-adjusted prices required in backtesting.
"""

from datetime import date
from unittest.mock import call, patch

import pandas as pd
import pytest

from momo.data.loader import load_universe


@pytest.mark.p0
@pytest.mark.unit
def test_1_3_unit_004(sample_price_df: pd.DataFrame) -> None:
    """Verify load_universe() passes adjustment='TOTALRETURN' to bridge calls."""
    # Test data
    symbols = ["AAPL", "MSFT"]
    start = date(2020, 1, 1)
    end = date(2020, 1, 10)
    universe = "test_universe"

    # Create mock DataFrame to return from bridge
    def create_symbol_df(symbol: str) -> pd.DataFrame:
        dates = pd.date_range("2020-01-01", "2020-01-10", freq="D")
        data = {
            "open": [100.0] * 10,
            "high": [105.0] * 10,
            "low": [95.0] * 10,
            "close": [102.0] * 10,
            "volume": [1000000] * 10,
            "unadjusted_close": [102.0] * 10,
            "dividend": [0.0] * 10,
        }
        index = pd.MultiIndex.from_product([dates, [symbol]], names=["date", "symbol"])
        return pd.DataFrame(data, index=index)

    # Mock dependencies
    with (
        patch("momo.data.loader.cache.load_prices", return_value=None),
        patch("momo.data.loader.cache.save_prices"),
        patch(
            "momo.data.loader.bridge.fetch_price_data",
            side_effect=lambda symbol, **kwargs: create_symbol_df(symbol),
        ) as mock_fetch,
    ):
        # Execute
        result_df = load_universe(
            symbols=symbols,
            start_date=start,
            end_date=end,
            universe=universe,
            force_refresh=False,
        )

        # Verify result is not None
        assert result_df is not None
        assert len(result_df) == 20  # 10 dates x 2 symbols

        # Step 5 & 6: Verify all bridge calls include adjustment="TOTALRETURN"
        assert mock_fetch.call_count == 2, "Should call bridge twice for 2 symbols"

        # Check each call for TOTALRETURN adjustment
        for symbol in symbols:
            expected_call = call(
                symbol=symbol,
                start_date=start,
                end_date=end,
                adjustment="TOTALRETURN",
                timeout=30,
            )
            assert (
                expected_call in mock_fetch.call_args_list
            ), f"Expected bridge call with TOTALRETURN for symbol {symbol}"

        # Verify all calls have TOTALRETURN (no other adjustment types)
        for call_obj in mock_fetch.call_args_list:
            _, kwargs = call_obj
            assert (
                kwargs["adjustment"] == "TOTALRETURN"
            ), "All bridge calls must use TOTALRETURN adjustment"
