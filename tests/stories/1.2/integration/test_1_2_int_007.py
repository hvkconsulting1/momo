"""
Test ID: 1.2-INT-007
Story: 1.2 - Integrate Norgate Data API via Windows Python Bridge
Priority: P2
Test Level: Integration
Risk Coverage: N/A

Description:
Verify that bridge correctly fetches data with different adjustment types (CAPITAL, TOTALRETURN).

Acceptance Criteria: AC3
Test Design Reference: docs/qa/assessments/1.2-test-design-20251204.md:570
"""

from datetime import date

import pytest
import structlog

from momo.data.bridge import check_ndu_status, fetch_price_data
from momo.utils.exceptions import NDUNotRunningError, NorgateBridgeError, WindowsPythonNotFoundError

logger = structlog.get_logger()


@pytest.mark.p2
@pytest.mark.integration
def test_1_2_int_007() -> None:
    """
    1.2-INT-007: Verify fetch_price_data() handles different adjustment types

    Justification: Feature coverage for adjustment types. Validates that both
    CAPITAL (split-adjusted only) and TOTALRETURN (split + dividend adjusted)
    work correctly through the bridge with documented differences.

    Expected: Both adjustment types work correctly, TOTALRETURN prices account for dividends
    Failure mode: One adjustment type fails, or prices are identical (no dividend adjustment)
    """
    # Arrange
    symbol = "AAPL"
    start_date = date(2023, 1, 1)
    end_date = date(2023, 12, 31)

    # Skip test if NDU not available
    try:
        ndu_running = check_ndu_status()
        if not ndu_running:
            pytest.skip("NDU is not running - cannot test adjustment types")
    except (WindowsPythonNotFoundError, NorgateBridgeError):
        pytest.skip("Cannot check NDU status - Windows Python or bridge not available")

    # Act - Fetch data with CAPITAL adjustment
    try:
        capital_df = fetch_price_data(
            symbol=symbol, start_date=start_date, end_date=end_date, adjustment="CAPITAL"
        )
        logger.info("fetched_capital_data", symbol=symbol, rows=len(capital_df))
    except NDUNotRunningError:
        pytest.skip("NDU is not running - cannot test CAPITAL adjustment")
    except Exception as e:
        pytest.fail(f"Failed to fetch CAPITAL data: {e}")

    # Act - Fetch data with TOTALRETURN adjustment
    try:
        totalreturn_df = fetch_price_data(
            symbol=symbol, start_date=start_date, end_date=end_date, adjustment="TOTALRETURN"
        )
        logger.info("fetched_totalreturn_data", symbol=symbol, rows=len(totalreturn_df))
    except NDUNotRunningError:
        pytest.skip("NDU is not running - cannot test TOTALRETURN adjustment")
    except Exception as e:
        pytest.fail(f"Failed to fetch TOTALRETURN data: {e}")

    # Assert - Both fetches succeeded
    assert capital_df is not None, "CAPITAL adjustment returned None"
    assert totalreturn_df is not None, "TOTALRETURN adjustment returned None"
    assert not capital_df.empty, "CAPITAL adjustment returned empty DataFrame"
    assert not totalreturn_df.empty, "TOTALRETURN adjustment returned empty DataFrame"

    # Assert - Both have same date range
    assert len(capital_df) == len(
        totalreturn_df
    ), f"Different row counts: CAPITAL={len(capital_df)}, TOTALRETURN={len(totalreturn_df)}"

    # Assert - TOTALRETURN prices differ from CAPITAL (dividend adjustments)
    # For a dividend-paying stock like AAPL, TOTALRETURN close prices should be
    # higher than CAPITAL close prices in most cases due to dividend reinvestment
    capital_close = capital_df["close"]
    totalreturn_close = totalreturn_df["close"]

    # Check that prices are different (at least for some dates)
    price_differences = totalreturn_close - capital_close
    num_different = (price_differences.abs() > 0.01).sum()

    assert num_different > 0, (
        "TOTALRETURN and CAPITAL prices are identical. "
        "Expected differences due to dividend adjustments for AAPL."
    )

    logger.info(
        "adjustment_type_comparison",
        symbol=symbol,
        dates_with_differences=num_different,
        total_dates=len(capital_df),
        capital_avg_close=capital_close.mean(),
        totalreturn_avg_close=totalreturn_close.mean(),
    )

    # Assert - Both have expected schema columns
    expected_columns = ["open", "high", "low", "close", "volume"]
    for col in expected_columns:
        assert col in capital_df.columns, f"CAPITAL missing column: {col}"
        assert col in totalreturn_df.columns, f"TOTALRETURN missing column: {col}"

    logger.info("adjustment_type_test_passed", symbol=symbol)
