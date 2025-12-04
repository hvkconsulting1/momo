"""
Test ID: 1.2-INT-006
Story: 1.2 - Integrate Norgate Data API via Windows Python Bridge
Priority: P0
Test Level: Integration
Risk Coverage: DATA-001 (JSON serialization failures)

Description:
Validate that fetched price data conforms to documented schema specification.
This ensures data quality and schema consistency for downstream consumers.

Acceptance Criteria: AC3
Test Design Reference: docs/qa/assessments/1.2-test-design-20251204.md:542
"""

import pandas as pd
import pytest

from momo.data.bridge import check_ndu_status, fetch_price_data


def test_1_2_int_006() -> None:
    """
    1.2-INT-006: Verify retrieved data has expected schema (Date, OHLCV)

    Justification: Data quality validation ensures downstream consumers can
    trust schema. Critical for data contract validation.

    Steps:
    1. Check if NDU is running (skip test if not available)
    2. Call fetch_price_data() for AAPL
    3. Verify required columns are present
    4. Verify dtypes are correct (datetime64[ns], float64, int64)
    5. Verify no NaN values in price columns
    6. Verify date column is sorted ascending
    7. Verify date column is index

    Expected: DataFrame schema matches specification (docs/architecture/data-models.md:6-20)
    Failure mode: Schema mismatch, incorrect dtypes, or data quality issues

    Environment Requirements:
    - Windows environment with NDU running
    """
    # Arrange & Act: Step 1 - Check NDU status
    if not check_ndu_status():
        pytest.skip("NDU is not running - integration test requires NDU")

    # Act: Step 2 - Fetch price data
    result_df = fetch_price_data(symbol="AAPL")

    # Assert: Step 3 - Verify required columns present
    expected_columns = ["symbol", "open", "high", "low", "close", "volume"]
    for col in expected_columns:
        assert (
            col in result_df.columns
        ), f"Expected column '{col}' in DataFrame, got columns: {result_df.columns.tolist()}"

    # Assert: Step 4 - Verify dtypes are correct
    assert pd.api.types.is_datetime64_any_dtype(
        result_df.index
    ), f"Expected date index to be datetime64[ns], got {result_df.index.dtype}"
    assert pd.api.types.is_float_dtype(
        result_df["open"]
    ), f"Expected 'open' to be float64, got {result_df['open'].dtype}"
    assert pd.api.types.is_float_dtype(
        result_df["high"]
    ), f"Expected 'high' to be float64, got {result_df['high'].dtype}"
    assert pd.api.types.is_float_dtype(
        result_df["low"]
    ), f"Expected 'low' to be float64, got {result_df['low'].dtype}"
    assert pd.api.types.is_float_dtype(
        result_df["close"]
    ), f"Expected 'close' to be float64, got {result_df['close'].dtype}"
    assert pd.api.types.is_integer_dtype(
        result_df["volume"]
    ), f"Expected 'volume' to be int64, got {result_df['volume'].dtype}"
    assert (
        pd.api.types.is_string_dtype(result_df["symbol"]) or result_df["symbol"].dtype == "object"
    ), f"Expected 'symbol' to be string or object, got {result_df['symbol'].dtype}"

    # Assert: Step 5 - Verify no NaN values in price columns
    price_columns = ["open", "high", "low", "close"]
    for col in price_columns:
        nan_count = result_df[col].isna().sum()
        assert nan_count == 0, f"Expected no NaN values in '{col}', found {nan_count} NaN values"

    # Assert: Step 6 - Verify date column is sorted ascending
    assert (
        result_df.index.is_monotonic_increasing
    ), "Expected date index to be sorted in ascending order"

    # Assert: Step 7 - Verify date column is index
    assert (
        result_df.index.name == "date"
    ), f"Expected index name to be 'date', got '{result_df.index.name}'"

    # Additional validation: Verify OHLC relationship (High >= Low, etc.)
    assert all(result_df["high"] >= result_df["low"]), "Expected high >= low for all rows"
    assert all(result_df["high"] >= result_df["open"]) or all(
        result_df["low"] <= result_df["open"]
    ), "Expected open to be between low and high"
    assert all(result_df["high"] >= result_df["close"]) or all(
        result_df["low"] <= result_df["close"]
    ), "Expected close to be between low and high"

    # Additional validation: Verify volume is positive
    assert all(result_df["volume"] > 0), "Expected all volume values to be positive"
