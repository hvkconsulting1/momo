"""
Test ID: 1.2-UNIT-009
Story: 1.2 - Integrate Norgate Data API via Windows Python Bridge
Priority: P0
Test Level: Unit
Risk Coverage: DATA-001 (JSON serialization failures)

Description:
Verify that fetch_price_data() correctly deserializes bridge response into
pandas DataFrame with expected schema.

Acceptance Criteria: AC3
Test Design Reference: docs/qa/assessments/1.2-test-design-20251204.md#1.2-unit-009-fetch_price_data-parses-dataframe-schema-correctly
"""

from unittest.mock import patch

import pandas as pd
import pytest

from momo.data.bridge import fetch_price_data


@pytest.mark.p0
@pytest.mark.unit
def test_1_2_unit_009() -> None:
    """Test ID: 1.2-UNIT-009

    Verify fetch_price_data() parses DataFrame schema correctly.

    Ref: docs/qa/assessments/1.2-test-design-20251204.md#1.2-unit-009-fetch_price_data-parses-dataframe-schema-correctly

    Steps:
    1. Mock execute_norgate_code() to return JSON DataFrame representation
    2. Call fetch_price_data()
    3. Assert result is pandas DataFrame
    4. Assert columns: ['date', 'symbol', 'open', 'high', 'low', 'close', 'volume']
    5. Assert dtypes: date=datetime64[ns], close=float64, volume=int64
    6. Assert date column is index

    Expected: DataFrame with correct schema matching data models specification
    """
    # Arrange: Mock execute_norgate_code with JSON DataFrame data
    with patch("momo.data.bridge.execute_norgate_code") as mock_execute:
        # Return list of dicts (as returned by lambda expression)
        mock_execute.return_value = [
            {
                "date": "2023-01-03",
                "open": 125.07,
                "high": 125.27,
                "low": 124.17,
                "close": 125.07,
                "volume": 112117471,
            },
            {
                "date": "2023-01-04",
                "open": 126.89,
                "high": 128.66,
                "low": 125.08,
                "close": 126.36,
                "volume": 89113631,
            },
        ]

        # Act: Call fetch_price_data
        result_df = fetch_price_data(symbol="AAPL")

        # Step 3: Assert result is pandas DataFrame
        assert isinstance(
            result_df, pd.DataFrame
        ), f"Result should be pandas DataFrame, got {type(result_df)}"

        # Step 4: Assert columns present
        expected_columns = ["symbol", "open", "high", "low", "close", "volume"]
        for col in expected_columns:
            assert col in result_df.columns, (
                f"Column '{col}' should be in DataFrame\n"
                f"Actual columns: {result_df.columns.tolist()}"
            )

        # Step 6: Assert date column is index
        assert (
            result_df.index.name == "date"
        ), f"Index should be named 'date', got '{result_df.index.name}'"

        # Step 5: Assert dtypes are correct
        assert (
            result_df.index.dtype == "datetime64[ns]"
        ), f"Index (date) should be datetime64[ns], got {result_df.index.dtype}"
        assert (
            result_df["open"].dtype == "float64"
        ), f"'open' should be float64, got {result_df['open'].dtype}"
        assert (
            result_df["high"].dtype == "float64"
        ), f"'high' should be float64, got {result_df['high'].dtype}"
        assert (
            result_df["low"].dtype == "float64"
        ), f"'low' should be float64, got {result_df['low'].dtype}"
        assert (
            result_df["close"].dtype == "float64"
        ), f"'close' should be float64, got {result_df['close'].dtype}"
        assert (
            result_df["volume"].dtype == "int64"
        ), f"'volume' should be int64, got {result_df['volume'].dtype}"

        # Verify DataFrame has correct number of rows
        assert len(result_df) == 2, f"DataFrame should have 2 rows, got {len(result_df)}"

        # Verify symbol column has correct value
        assert (result_df["symbol"] == "AAPL").all(), (
            f"All rows should have symbol 'AAPL'\n" f"Actual values: {result_df['symbol'].unique()}"
        )


@pytest.mark.p0
@pytest.mark.unit
def test_1_2_unit_009_list_format() -> None:
    """Test ID: 1.2-UNIT-009 (variant: list format)

    Verify fetch_price_data() handles result as list (alternative format).

    Expected: DataFrame parsed correctly from list format
    """
    # Arrange: Mock with list format (no "data" wrapper)
    with patch("momo.data.bridge.execute_norgate_code") as mock_execute:
        mock_execute.return_value = [
            {
                "date": "2023-01-03",
                "open": 125.07,
                "high": 125.27,
                "low": 124.17,
                "close": 125.07,
                "volume": 112117471,
            }
        ]

        # Act: Call fetch_price_data
        result_df = fetch_price_data(symbol="AAPL")

        # Assert: Verify DataFrame created correctly
        assert isinstance(result_df, pd.DataFrame)
        assert len(result_df) == 1
        assert result_df.index.name == "date"


@pytest.mark.p0
@pytest.mark.unit
def test_1_2_unit_009_missing_columns() -> None:
    """Test ID: 1.2-UNIT-009 (variant: missing columns error)

    Verify fetch_price_data() raises error when required columns missing.

    Expected: NorgateBridgeError raised with clear message
    """
    # Arrange: Mock with incomplete data (missing 'close' column)
    with patch("momo.data.bridge.execute_norgate_code") as mock_execute:
        # Return list of dicts with missing 'close' column
        mock_execute.return_value = [
            {
                "date": "2023-01-03",
                "open": 125.07,
                "high": 125.27,
                "low": 124.17,
                # Missing 'close' column
                "volume": 112117471,
            }
        ]

        # Act & Assert: Verify error raised
        from momo.utils.exceptions import NorgateBridgeError

        with pytest.raises(NorgateBridgeError) as exc_info:
            fetch_price_data(symbol="AAPL")

        assert "Failed to parse price data from bridge" in str(exc_info.value), (
            f"Error should mention parsing failure\n" f"Actual error: {exc_info.value}"
        )


@pytest.mark.p0
@pytest.mark.unit
def test_1_2_unit_009_invalid_format() -> None:
    """Test ID: 1.2-UNIT-009 (variant: invalid format error)

    Verify fetch_price_data() raises error for unexpected result format.

    Expected: NorgateBridgeError raised with clear message
    """
    # Arrange: Mock with invalid format (string instead of dict/list)
    with patch("momo.data.bridge.execute_norgate_code") as mock_execute:
        mock_execute.return_value = "invalid format"

        # Act & Assert: Verify error raised
        from momo.utils.exceptions import NorgateBridgeError

        with pytest.raises(NorgateBridgeError) as exc_info:
            fetch_price_data(symbol="AAPL")

        assert "Expected list of records" in str(exc_info.value), (
            f"Error should mention expected list format\n" f"Actual error: {exc_info.value}"
        )
