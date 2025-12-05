"""Test ID: 1.3-UNIT-018

Test partial fetch failures are handled gracefully in load_universe().

This test verifies that when some symbols fail to fetch via the bridge,
load_universe() continues with remaining symbols, logs errors appropriately,
and caches partial results successfully.
"""

from datetime import date
from unittest.mock import patch

import pandas as pd
import pytest

from momo.data.loader import load_universe
from momo.utils.exceptions import NorgateBridgeError


@pytest.mark.p0
@pytest.mark.unit
def test_1_3_unit_018_partial_fetch_failures(
    sample_price_df: pd.DataFrame,
    temp_cache_dir: str,
) -> None:
    """Test ID: 1.3-UNIT-018

    Story: 1.3 - Implement Data Loading and Parquet Caching
    Priority: P0
    Test Level: Unit
    Risk Coverage: TECH-002

    Verifies load_universe() handles partial fetch failures gracefully.

    Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac8-unit-tests-verify-caching-logic

    Steps:
    1. Mock bridge.fetch_price_data() to fail for some symbols
    2. Mock cache.load_prices() to return None (cache miss)
    3. Call load_universe() with mix of valid and invalid symbols
    4. Verify function continues fetching after failures
    5. Verify successful symbols are in result DataFrame
    6. Verify failed symbols are logged with error details
    7. Verify partial results are saved to cache

    Expected:
    - Function returns DataFrame with successfully fetched symbols only
    - Failed symbols logged with error messages
    - Partial results saved to cache via cache.save_prices()
    - No exception raised (graceful degradation)
    """
    # Test configuration
    symbols = ["AAPL", "INVALID_SYMBOL", "MSFT", "ANOTHER_BAD", "GOOGL"]
    start_date = date(2020, 1, 1)
    end_date = date(2020, 1, 10)
    universe = "test_universe"

    # Create mock DataFrames for successful symbols
    # We'll use a subset of sample_price_df for each successful symbol
    aapl_df = sample_price_df[sample_price_df.index.get_level_values("symbol") == "AAPL"]
    msft_df = sample_price_df[sample_price_df.index.get_level_values("symbol") == "MSFT"]
    googl_df = sample_price_df[sample_price_df.index.get_level_values("symbol") == "GOOGL"]

    # Mock fetch_price_data to fail for specific symbols
    def mock_fetch(symbol: str, **kwargs):  # type: ignore[no-untyped-def]
        if symbol == "INVALID_SYMBOL":
            raise NorgateBridgeError("Symbol not found: INVALID_SYMBOL")
        elif symbol == "ANOTHER_BAD":
            raise NorgateBridgeError("API timeout for ANOTHER_BAD")
        elif symbol == "AAPL":
            return aapl_df
        elif symbol == "MSFT":
            return msft_df
        elif symbol == "GOOGL":
            return googl_df
        else:
            raise ValueError(f"Unexpected symbol: {symbol}")

    with (
        patch("momo.data.loader.cache.load_prices", return_value=None),
        patch("momo.data.loader.cache.save_prices") as mock_save,
        patch("momo.data.loader.bridge.fetch_price_data", side_effect=mock_fetch),
        patch("momo.data.loader.logger") as mock_logger,
    ):
        # Call load_universe
        result_df = load_universe(
            symbols=symbols,
            start_date=start_date,
            end_date=end_date,
            universe=universe,
            force_refresh=False,
        )

        # Verify result contains only successful symbols
        result_symbols = result_df.index.get_level_values("symbol").unique().tolist()
        assert set(result_symbols) == {"AAPL", "MSFT", "GOOGL"}, (
            f"Expected result to contain only successful symbols, " f"got {result_symbols}"
        )

        # Verify failed symbols are not in result
        assert "INVALID_SYMBOL" not in result_symbols
        assert "ANOTHER_BAD" not in result_symbols

        # Verify error logging for failed symbols
        # Check that logger.error was called for each failed symbol
        error_calls = [
            call for call in mock_logger.error.call_args_list if call[0][0] == "symbol_fetch_failed"
        ]
        assert (
            len(error_calls) == 2
        ), f"Expected 2 error log calls for failed symbols, got {len(error_calls)}"

        # Verify error log contains symbol information
        logged_symbols = [call.kwargs["symbol"] for call in error_calls]
        assert "INVALID_SYMBOL" in logged_symbols
        assert "ANOTHER_BAD" in logged_symbols

        # Verify partial failure warning was logged
        warning_calls = [
            call
            for call in mock_logger.warning.call_args_list
            if call[0][0] == "partial_fetch_failure"
        ]
        assert (
            len(warning_calls) == 1
        ), f"Expected 1 partial_fetch_failure warning, got {len(warning_calls)}"

        warning_kwargs = warning_calls[0].kwargs
        assert warning_kwargs["failed_count"] == 2
        assert warning_kwargs["successful_count"] == 3
        assert set(warning_kwargs["failed_symbols"]) == {
            "INVALID_SYMBOL",
            "ANOTHER_BAD",
        }

        # Verify partial results were saved to cache
        assert mock_save.called, "Expected cache.save_prices to be called"
        save_call_kwargs = mock_save.call_args.kwargs
        saved_df = save_call_kwargs["df"]

        # Verify saved DataFrame contains only successful symbols
        saved_symbols = saved_df.index.get_level_values("symbol").unique().tolist()
        assert set(saved_symbols) == {"AAPL", "MSFT", "GOOGL"}


@pytest.mark.p0
@pytest.mark.unit
def test_1_3_unit_018_all_symbols_fail() -> None:
    """Test ID: 1.3-UNIT-018 (edge case)

    Story: 1.3 - Implement Data Loading and Parquet Caching
    Priority: P0
    Test Level: Unit
    Risk Coverage: TECH-002

    Verifies load_universe() raises ValueError when ALL symbols fail.

    Steps:
    1. Mock bridge.fetch_price_data() to fail for all symbols
    2. Mock cache.load_prices() to return None (cache miss)
    3. Call load_universe() with symbols that all fail
    4. Verify ValueError is raised with informative message

    Expected:
    - ValueError raised with list of failed symbols
    - Error includes count of failed symbols
    """
    symbols = ["INVALID1", "INVALID2", "INVALID3"]
    start_date = date(2020, 1, 1)
    end_date = date(2020, 1, 10)
    universe = "test_universe"

    def mock_fetch_all_fail(symbol: str, **kwargs):  # type: ignore[no-untyped-def]
        raise NorgateBridgeError(f"Symbol not found: {symbol}")

    with (
        patch("momo.data.loader.cache.load_prices", return_value=None),
        patch(
            "momo.data.loader.bridge.fetch_price_data",
            side_effect=mock_fetch_all_fail,
        ),
    ):
        with pytest.raises(ValueError) as exc_info:
            load_universe(
                symbols=symbols,
                start_date=start_date,
                end_date=end_date,
                universe=universe,
            )

        # Verify error message includes all failed symbols
        error_msg = str(exc_info.value)
        assert "All 3 symbols failed to fetch" in error_msg
        assert "INVALID1" in error_msg
        assert "INVALID2" in error_msg
        assert "INVALID3" in error_msg
