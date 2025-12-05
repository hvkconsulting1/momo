"""Test ID: 1.4-UNIT-011

Verify _check_adjustment_consistency() flags negative prices as invalid.

Ref: docs/qa/assessments/1.4-test-design-20251205.md#14-unit-011-_check_adjustment_consistency-flags-negative-prices

Steps:
1. Create prices DataFrame with ticker FAIL having negative close price
2. Call _check_adjustment_consistency(prices_df)
3. Verify "FAIL" is in the returned list
4. Verify other tickers are not flagged

Expected: "FAIL" flagged for negative price (invalid state after adjustment error)
"""

import pytest

from momo.data.validation import _check_adjustment_consistency


@pytest.mark.p0
@pytest.mark.unit
def test_1_4_unit_011(sample_price_df_with_negative_price):
    """Test _check_adjustment_consistency() flags negative prices."""
    # Given: DataFrame with FAIL ticker having negative close price
    prices_df = sample_price_df_with_negative_price

    # When: Call _check_adjustment_consistency()
    result = _check_adjustment_consistency(prices_df)

    # Then: "FAIL" should be flagged
    assert "FAIL" in result, "FAIL ticker with negative price should be flagged"

    # And: Other tickers should not be flagged
    clean_tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
    for ticker in clean_tickers:
        assert ticker not in result, f"{ticker} should not be flagged (has valid prices)"
