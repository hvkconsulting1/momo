"""Test ID: 1.3-INT-011

Integration test to verify failed symbols are logged with detailed error
messages and symbol list.

This test validates observability for debugging fetch failures in production.
"""

from datetime import date
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from momo.data.loader import load_universe
from momo.utils.exceptions import NDUNotRunningError, NorgateBridgeError


@pytest.mark.p1
@pytest.mark.integration
def test_1_3_int_011_failed_symbols_logged(
    sample_price_df: pd.DataFrame,
    temp_cache_dir: str,
) -> None:
    """Test ID: 1.3-INT-011

    Story: 1.3 - Implement Data Loading and Parquet Caching
    Priority: P1
    Test Level: Integration
    Risk Coverage: TECH-002

    Verifies failed symbols are logged with detailed error messages and symbol list.

    Ref: docs/qa/assessments/1.3-test-design-20251204.md#tech-002-bridge-integration-error-handling

    Steps:
    1. Mock bridge to fail for specific symbols with different error types
    2. Mock structlog logger to capture log calls
    3. Call load_universe() with mix of valid and invalid symbols
    4. Verify each failed symbol has individual error log entry
    5. Verify error logs include symbol name, error message, and error type
    6. Verify partial_fetch_failure warning includes failed symbol list
    7. Verify logs distinguish between different error types (NDU vs generic)

    Expected:
    - Each failed symbol logged individually with detailed error info
    - Partial failure warning logged with aggregate failed symbol list
    - Error types are distinguishable in logs (NDU, timeout, etc.)
    - Logs include sufficient context for debugging (symbol, error_type, error message)
    """
    # Test configuration
    symbols = ["AAPL", "NDU_DOWN_SYM", "TIMEOUT_SYM", "MSFT", "NOT_FOUND_SYM"]
    start_date = date(2020, 1, 1)
    end_date = date(2020, 1, 10)
    universe = "test_error_logging"

    # Create mock DataFrames for successful symbols
    aapl_df = sample_price_df[sample_price_df.index.get_level_values("symbol") == "AAPL"]
    msft_df = sample_price_df[sample_price_df.index.get_level_values("symbol") == "MSFT"]

    # Mock fetch_price_data with different error types
    def mock_fetch_varied_errors(symbol: str, **kwargs):  # type: ignore[no-untyped-def]
        if symbol == "NDU_DOWN_SYM":
            raise NDUNotRunningError("Norgate Data Updater is not running")
        elif symbol == "TIMEOUT_SYM":
            raise NorgateBridgeError("Bridge timeout after 30 seconds")
        elif symbol == "NOT_FOUND_SYM":
            raise NorgateBridgeError("Symbol NOT_FOUND_SYM does not exist in database")
        elif symbol == "AAPL":
            return aapl_df
        elif symbol == "MSFT":
            return msft_df
        else:
            raise ValueError(f"Unexpected symbol: {symbol}")

    # Create a mock logger that captures all calls
    mock_logger = MagicMock()

    with (
        patch(
            "momo.data.loader.bridge.fetch_price_data",
            side_effect=mock_fetch_varied_errors,
        ),
        patch("momo.data.loader.logger", mock_logger),
    ):
        # Call load_universe
        result_df = load_universe(
            symbols=symbols,
            start_date=start_date,
            end_date=end_date,
            universe=universe,
            force_refresh=True,
        )

        # Verify result contains only successful symbols
        result_symbols = result_df.index.get_level_values("symbol").unique().tolist()
        assert set(result_symbols) == {"AAPL", "MSFT"}

        # Step 4-5: Verify individual error logs for each failed symbol
        error_calls = [
            call for call in mock_logger.error.call_args_list if call[0][0] == "symbol_fetch_failed"
        ]

        # Should have 3 error log calls (one for each failed symbol)
        assert (
            len(error_calls) == 3
        ), f"Expected 3 error log calls for failed symbols, got {len(error_calls)}"

        # Extract error log details
        error_logs = []
        for call in error_calls:
            log_entry = {
                "symbol": call.kwargs["symbol"],
                "error": call.kwargs["error"],
                "error_type": call.kwargs["error_type"],
            }
            error_logs.append(log_entry)

        # Verify each failed symbol has a log entry
        logged_symbols = {log["symbol"] for log in error_logs}
        assert logged_symbols == {
            "NDU_DOWN_SYM",
            "TIMEOUT_SYM",
            "NOT_FOUND_SYM",
        }, f"Expected all failed symbols logged, got {logged_symbols}"

        # Step 6: Verify error types are distinguishable
        error_types = {log["error_type"] for log in error_logs}
        assert "NDUNotRunningError" in error_types, "Expected NDUNotRunningError in logs"
        assert "NorgateBridgeError" in error_types, "Expected NorgateBridgeError in logs"

        # Step 7: Verify error messages contain useful debugging info
        ndu_log = next(log for log in error_logs if log["symbol"] == "NDU_DOWN_SYM")
        assert (
            "not running" in ndu_log["error"].lower()
        ), f"Expected NDU error message to mention 'not running', got: {ndu_log['error']}"

        timeout_log = next(log for log in error_logs if log["symbol"] == "TIMEOUT_SYM")
        assert (
            "timeout" in timeout_log["error"].lower()
        ), f"Expected timeout error message to mention 'timeout', got: {timeout_log['error']}"

        not_found_log = next(log for log in error_logs if log["symbol"] == "NOT_FOUND_SYM")
        assert (
            "not exist" in not_found_log["error"].lower()
            or "NOT_FOUND_SYM" in not_found_log["error"]
        ), f"Expected not found error to mention symbol, got: {not_found_log['error']}"

        # Step 8: Verify partial_fetch_failure warning
        warning_calls = [
            call
            for call in mock_logger.warning.call_args_list
            if call[0][0] == "partial_fetch_failure"
        ]

        assert (
            len(warning_calls) == 1
        ), f"Expected 1 partial_fetch_failure warning, got {len(warning_calls)}"

        warning_kwargs = warning_calls[0].kwargs
        assert warning_kwargs["failed_count"] == 3, "Expected failed_count=3"
        assert warning_kwargs["successful_count"] == 2, "Expected successful_count=2"
        assert warning_kwargs["total_requested"] == 5, "Expected total_requested=5"

        # Verify failed_symbols list in warning
        assert set(warning_kwargs["failed_symbols"]) == {
            "NDU_DOWN_SYM",
            "TIMEOUT_SYM",
            "NOT_FOUND_SYM",
        }, f"Expected all failed symbols in warning, got {warning_kwargs['failed_symbols']}"

    print("✓ Failed symbol logging verified")
    print("✓ Individual error logs: 3 entries with detailed error info")
    print("✓ Error types distinguishable: NDUNotRunningError, NorgateBridgeError")
    print("✓ Partial failure warning includes aggregate failed symbol list")
