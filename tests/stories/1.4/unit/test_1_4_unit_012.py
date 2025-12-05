"""Test ID: 1.4-UNIT-012

Verify _check_adjustment_consistency() flags 50% price jump without dividend.

Ref: docs/qa/assessments/1.4-test-design-20251205.md#14-unit-012-_check_adjustment_consistency-flags-50-jump-without-dividend

Steps:
1. Create prices DataFrame where ticker XYZ has 50% price jump without dividend entry
2. Call _check_adjustment_consistency(prices_df)
3. Verify "XYZ" is in the returned list
4. Verify heuristic threshold correctly identifies suspicious jump

Expected: "XYZ" flagged for 50% jump without dividend (detects missing split/dividend adjustment)
"""

import pandas as pd
import pytest

from momo.data.validation import _check_adjustment_consistency


@pytest.mark.p1
@pytest.mark.unit
def test_1_4_unit_012(sample_price_df_with_50pct_jump_no_div: pd.DataFrame) -> None:
    """Test _check_adjustment_consistency() flags 50% price jump without dividend."""
    # Given: DataFrame with XYZ ticker having 50% price jump and dividend=0
    prices_df = sample_price_df_with_50pct_jump_no_div

    # When: Call _check_adjustment_consistency()
    result = _check_adjustment_consistency(prices_df)

    # Then: "XYZ" should be flagged for suspicious jump
    assert "XYZ" in result, "XYZ ticker with 50% jump and no dividend should be flagged"

    # And: Other clean tickers should not be flagged
    clean_tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
    for ticker in clean_tickers:
        assert ticker not in result, f"{ticker} should not be flagged (no price jumps)"
