"""Test ID: 1.4-UNIT-006

Test that _check_missing_values() detects NaN in close column.

Ref: docs/qa/assessments/1.4-test-design-20251205.md#14-unit-006-_check_missing_values-detects-nan-in-close-column

Steps:
1. Load price DataFrame with 3 NaN values in AAPL close column
2. Call _check_missing_values(prices_df)
3. Verify function returns {"AAPL": 3}
4. Verify other tickers are not in result (no false positives)

Expected: _check_missing_values() returns {"AAPL": 3}, correctly detecting NaN values.
"""

import pandas as pd
import pytest

from momo.data.validation import _check_missing_values


@pytest.mark.p0
@pytest.mark.unit
def test_1_4_unit_006(sample_price_df_with_nans_close: pd.DataFrame) -> None:
    """Test _check_missing_values() detects NaN in close column."""
    # Step 1: Load price DataFrame with NaN in AAPL close column (via fixture)
    prices_df = sample_price_df_with_nans_close

    # Step 2: Call _check_missing_values()
    result = _check_missing_values(prices_df)

    # Step 3: Verify function detects exactly 3 NaN in AAPL
    assert "AAPL" in result, f"Expected 'AAPL' in result, got: {result}"
    assert result["AAPL"] == 3, f"Expected AAPL to have 3 missing values, got: {result['AAPL']}"

    # Step 4: Verify other tickers are not flagged (no false positives)
    assert "MSFT" not in result, "MSFT should not have missing data, but found in result"
    assert "GOOGL" not in result, "GOOGL should not have missing data, but found in result"
    assert "AMZN" not in result, "AMZN should not have missing data, but found in result"
    assert "TSLA" not in result, "TSLA should not have missing data, but found in result"

    # Additional check: only one ticker should be in result
    assert len(result) == 1, f"Expected only AAPL in result, got: {result}"
