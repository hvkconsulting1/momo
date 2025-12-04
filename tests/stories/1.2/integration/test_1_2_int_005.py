"""
Test ID: 1.2-INT-005
Story: 1.2 - Integrate Norgate Data API via Windows Python Bridge
Priority: P0
Test Level: Integration
Risk Coverage: TECH-001 (Subprocess communication failure)

Description:
End-to-end validation of full bridge + NDU + norgatedata stack with actual
price data retrieval. This is the critical path validation proving the entire
bridge stack works end-to-end.

Acceptance Criteria: AC3
Test Design Reference: docs/qa/assessments/1.2-test-design-20251204.md:511
"""

from datetime import date

import pandas as pd
import pytest

from momo.data.bridge import check_ndu_status, fetch_price_data


def test_1_2_int_005() -> None:
    """
    1.2-INT-005: Verify fetch_price_data() retrieves AAPL data with NDU running

    Justification: Critical path validation - proves entire bridge stack works
    end-to-end. Validates bridge + NDU + norgatedata integration.

    Steps:
    1. Check if NDU is running (skip test if not available)
    2. Call fetch_price_data() for AAPL with date range
    3. Verify DataFrame is returned (not None)
    4. Verify DataFrame is not empty (rows > 0)
    5. Verify symbol column contains "AAPL"

    Expected: AAPL price data retrieved successfully with reasonable performance
    Failure mode: Bridge communication failed, NDU not responding, or data not available

    Environment Requirements:
    - Windows environment
    - NDU running and authenticated
    - Windows Python with norgatedata 1.0.74
    - Russell 3000 C&P subscription active
    """
    # Arrange & Act: Step 1 - Check NDU status
    if not check_ndu_status():
        pytest.skip("NDU is not running - integration test requires NDU")

    # Arrange: Define test parameters
    symbol = "AAPL"
    start_date = date(2023, 1, 1)
    end_date = date(2023, 12, 31)

    # Act: Step 2 - Fetch price data
    result_df = fetch_price_data(
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
        adjustment="TOTALRETURN",
    )

    # Assert: Step 3 - Verify DataFrame returned
    assert result_df is not None, "fetch_price_data() should return DataFrame, got None"
    assert isinstance(result_df, pd.DataFrame), f"Expected pandas DataFrame, got {type(result_df)}"

    # Assert: Step 4 - Verify DataFrame not empty
    assert len(result_df) > 0, f"Expected non-empty DataFrame, got {len(result_df)} rows"

    # Additional validation: Expect approximately 252 trading days in a year
    expected_min_rows = 240  # Account for holidays/market closures
    assert (
        len(result_df) >= expected_min_rows
    ), f"Expected at least {expected_min_rows} trading days in 2023, got {len(result_df)}"

    # Assert: Step 5 - Verify symbol column contains AAPL
    assert (
        "symbol" in result_df.columns
    ), f"Expected 'symbol' column, got columns: {result_df.columns.tolist()}"
    assert all(result_df["symbol"] == symbol), (
        f"Expected all rows to have symbol '{symbol}', "
        f"got: {result_df['symbol'].unique().tolist()}"
    )
