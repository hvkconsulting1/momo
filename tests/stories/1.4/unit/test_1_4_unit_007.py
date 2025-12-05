"""Test ID: 1.4-UNIT-007

Test that _check_missing_values() detects NaN in OHLC columns.

Ref: docs/qa/assessments/1.4-test-design-20251205.md#14-unit-007-_check_missing_values-detects-nan-in-ohlc-columns

Steps:
1. Load price DataFrame with NaN values across OHLC columns for MSFT
2. Call _check_missing_values(prices_df)
3. Verify function returns {"MSFT": N} where N >= 3
4. Verify function checks all OHLC columns, not just close
5. Verify other tickers are not in result

Expected: _check_missing_values() returns {"MSFT": 3+}, aggregating NaN across multiple columns.
"""

import pandas as pd
import pytest

from momo.data.validation import _check_missing_values


@pytest.mark.p0
@pytest.mark.unit
def test_1_4_unit_007(sample_price_df_with_nans_ohlc: pd.DataFrame) -> None:
    """Test _check_missing_values() detects NaN in OHLC columns."""
    # Step 1: Load price DataFrame with NaN in MSFT OHLC columns (via fixture)
    # Fixture has: 2 NaN in open, 1 NaN in high = 3 total
    prices_df = sample_price_df_with_nans_ohlc

    # Step 2: Call _check_missing_values()
    result = _check_missing_values(prices_df)

    # Step 3: Verify function detects at least 3 NaN in MSFT (2 in open + 1 in high)
    assert "MSFT" in result, f"Expected 'MSFT' in result, got: {result}"
    assert (
        result["MSFT"] >= 3
    ), f"Expected MSFT to have at least 3 missing values (2 open + 1 high), got: {result['MSFT']}"

    # Step 4: Verify function checks multiple columns (not just close)
    # This is implicitly tested by the fixture design:
    # - MSFT has NaN in open and high columns (not close)
    # - If function only checked close, it would not detect MSFT issues
    assert result["MSFT"] == 3, f"Expected exactly 3 NaN (2 open + 1 high), got: {result['MSFT']}"

    # Step 5: Verify other tickers are not flagged
    assert "AAPL" not in result, "AAPL should not have missing data"
    assert "GOOGL" not in result, "GOOGL should not have missing data"
    assert "AMZN" not in result, "AMZN should not have missing data"
    assert "TSLA" not in result, "TSLA should not have missing data"

    # Additional check: only one ticker should be in result
    assert len(result) == 1, f"Expected only MSFT in result, got: {result}"
