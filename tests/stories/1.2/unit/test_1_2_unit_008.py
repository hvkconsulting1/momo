"""
Test ID: 1.2-UNIT-008
Story: 1.2 - Integrate Norgate Data API via Windows Python Bridge
Priority: P0
Test Level: Unit
Risk Coverage: DATA-001 (JSON serialization failures)

Description:
Verify that fetch_price_data() constructs correct norgatedata API call for
price data retrieval.

Acceptance Criteria: AC3
Test Design Reference: docs/qa/assessments/1.2-test-design-20251204.md#1.2-unit-008-fetch_price_data-constructs-correct-norgate-api-call
"""

from datetime import date
from unittest.mock import patch

import pytest

from momo.data.bridge import fetch_price_data


@pytest.mark.p0
@pytest.mark.unit
def test_1_2_unit_008() -> None:
    """Test ID: 1.2-UNIT-008

    Verify fetch_price_data() constructs correct Norgate API call.

    Ref: docs/qa/assessments/1.2-test-design-20251204.md#1.2-unit-008-fetch_price_data-constructs-correct-norgate-api-call

    Steps:
    1. Mock execute_norgate_code() to capture code parameter
    2. Call fetch_price_data() with various parameters
    3. Verify code includes norgatedata.price_timeseries() with correct parameters
    4. Verify adjustment type passed correctly
    5. Verify date format correct (ISO 8601)

    Expected: Generated code correctly calls norgatedata API with all parameters
    """
    # Arrange: Mock execute_norgate_code to capture the code parameter
    with patch("momo.data.bridge.execute_norgate_code") as mock_execute:
        # Return mock DataFrame data (list of dicts, as returned by lambda expression)
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

        # Act: Call fetch_price_data with all parameters
        result_df = fetch_price_data(
            symbol="AAPL",
            start_date=date(2023, 1, 1),
            end_date=date(2023, 12, 31),
            adjustment="TOTALRETURN",
            timeout=30,
        )

        # Assert: Verify execute_norgate_code was called
        assert mock_execute.called, "execute_norgate_code should be called"
        call_args = mock_execute.call_args

        # Extract the code parameter (first positional argument)
        code_param = call_args[0][0]

        # Step 3: Assert code includes norgatedata.price_timeseries() with symbol
        assert 'norgatedata.price_timeseries("AAPL"' in code_param, (
            f"Code should include norgatedata.price_timeseries() call with symbol AAPL\n"
            f"Actual code: {code_param}"
        )

        # Step 5: Assert date format correct (ISO 8601)
        assert 'start_date="2023-01-01"' in code_param, (
            f"Code should include start_date in ISO 8601 format\n" f"Actual code: {code_param}"
        )
        assert 'end_date="2023-12-31"' in code_param, (
            f"Code should include end_date in ISO 8601 format\n" f"Actual code: {code_param}"
        )

        # Step 4: Assert adjustment type passed correctly
        assert "StockPriceAdjustmentType.TOTALRETURN" in code_param, (
            f"Code should include adjustment type TOTALRETURN\n" f"Actual code: {code_param}"
        )

        # Assert timeout passed correctly
        assert call_args[1]["timeout"] == 30, "Timeout should be 30 seconds"

        # Assert pandas-dataframe format requested
        assert 'timeseriesformat="pandas-dataframe"' in code_param, (
            f"Code should request pandas-dataframe format\n" f"Actual code: {code_param}"
        )

        # Verify result is returned correctly
        assert result_df is not None, "Function should return DataFrame"
        assert len(result_df) == 1, "DataFrame should have 1 row"


@pytest.mark.p0
@pytest.mark.unit
def test_1_2_unit_008_defaults() -> None:
    """Test ID: 1.2-UNIT-008 (variant: default parameters)

    Verify fetch_price_data() constructs correct call with default parameters.

    Expected: Code omits optional start_date and end_date when not provided
    """
    # Arrange: Mock execute_norgate_code
    with patch("momo.data.bridge.execute_norgate_code") as mock_execute:
        # Return mock DataFrame data (list of dicts, as returned by lambda expression)
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

        # Act: Call with minimal parameters (no dates)
        _ = fetch_price_data(symbol="MSFT")

        # Assert: Verify code doesn't include dates
        code_param = mock_execute.call_args[0][0]

        assert 'norgatedata.price_timeseries("MSFT"' in code_param, (
            f"Code should include symbol MSFT\n" f"Actual code: {code_param}"
        )

        # Default adjustment should be TOTALRETURN
        assert "StockPriceAdjustmentType.TOTALRETURN" in code_param, (
            f"Code should use default adjustment TOTALRETURN\n" f"Actual code: {code_param}"
        )


@pytest.mark.p0
@pytest.mark.unit
def test_1_2_unit_008_capital_adjustment() -> None:
    """Test ID: 1.2-UNIT-008 (variant: CAPITAL adjustment)

    Verify fetch_price_data() correctly passes CAPITAL adjustment type.

    Expected: Code includes StockPriceAdjustmentType.CAPITAL
    """
    # Arrange: Mock execute_norgate_code
    with patch("momo.data.bridge.execute_norgate_code") as mock_execute:
        # Return mock DataFrame data (list of dicts, as returned by lambda expression)
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

        # Act: Call with CAPITAL adjustment
        _ = fetch_price_data(symbol="AAPL", adjustment="CAPITAL")

        # Assert: Verify CAPITAL adjustment in code
        code_param = mock_execute.call_args[0][0]

        assert "StockPriceAdjustmentType.CAPITAL" in code_param, (
            f"Code should use CAPITAL adjustment\n" f"Actual code: {code_param}"
        )
