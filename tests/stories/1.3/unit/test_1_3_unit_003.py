"""Test progress logging for multi-symbol fetches.

Test ID: 1.3-UNIT-003
Story: 1.3 - Implement Data Loading and Parquet Caching
Priority: P1
Test Level: Unit
Risk Coverage: N/A

Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac1-fetch-ohlcv-data-using-norgatedata-api

Steps:
1. Mock cache.load_prices() to return None (cache miss)
2. Mock bridge.fetch_price_data() to return sample DataFrames
3. Mock cache.save_prices() to avoid file I/O
4. Call load_universe() with multiple symbols (e.g., 3 symbols)
5. Capture structlog output
6. Verify start log message with symbols_count
7. Verify per-symbol log messages with symbol, index, total
8. Verify completion log message with symbols_count and duration

Expected: Structlog outputs progress messages for fetching_universe (start),
fetching_symbol (per-symbol), and universe_fetched (completion).
"""

from datetime import date
from unittest.mock import patch

import pandas as pd
import pytest

from momo.data.loader import load_universe


@pytest.mark.p1
@pytest.mark.unit
def test_1_3_unit_003(sample_price_df: pd.DataFrame) -> None:
    """Verify load_universe() logs progress for multi-symbol fetches."""
    # Test data
    symbols = ["AAPL", "MSFT", "GOOGL"]
    start = date(2020, 1, 1)
    end = date(2020, 1, 10)
    universe = "test_universe"

    # Create individual symbol DataFrames
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
        ),
        patch("momo.data.loader.logger") as mock_logger,
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
        assert len(result_df) == 30  # 10 dates x 3 symbols

        # Step 6: Verify start log message (fetching_universe)
        fetching_universe_calls = [
            call for call in mock_logger.info.call_args_list if call[0][0] == "fetching_universe"
        ]
        assert len(fetching_universe_calls) == 1, "Should log fetching_universe once"
        fetching_universe_kwargs = fetching_universe_calls[0][1]
        assert fetching_universe_kwargs["symbols_count"] == 3

        # Step 7: Verify per-symbol log messages
        fetching_symbol_calls = [
            call for call in mock_logger.info.call_args_list if call[0][0] == "fetching_symbol"
        ]
        assert len(fetching_symbol_calls) == 3, "Should log fetching_symbol 3 times"

        # Verify each symbol was logged with index and total
        logged_symbols = [call[1]["symbol"] for call in fetching_symbol_calls]
        assert set(logged_symbols) == set(symbols), "All symbols should be logged"

        # Verify index and total are included
        for i, call_obj in enumerate(fetching_symbol_calls, start=1):
            kwargs = call_obj[1]
            assert "index" in kwargs, "Each fetching_symbol log should include index"
            assert "total" in kwargs, "Each fetching_symbol log should include total"
            assert kwargs["index"] == i, f"Expected index {i}, got {kwargs['index']}"
            assert kwargs["total"] == 3, f"Expected total 3, got {kwargs['total']}"

        # Step 8: Verify completion log message (universe_fetched)
        universe_fetched_calls = [
            call for call in mock_logger.info.call_args_list if call[0][0] == "universe_fetched"
        ]
        assert len(universe_fetched_calls) == 1, "Should log universe_fetched once"
        universe_fetched_kwargs = universe_fetched_calls[0][1]
        assert universe_fetched_kwargs["symbols_count"] == 3
        assert universe_fetched_kwargs["rows"] == 30
        assert "duration" in universe_fetched_kwargs, "Should include duration in completion log"
