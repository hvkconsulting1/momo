"""Test ID: 1.4-UNIT-013

Verify _check_adjustment_consistency() allows legitimate Apple 7:1 stock split.

Ref: docs/qa/assessments/1.4-test-design-20251205.md#14-unit-013-_check_adjustment_consistency-allows-aapl-71-split

Steps:
1. Load prices DataFrame with Apple's historical 7:1 stock split (June 9, 2014)
2. Call _check_adjustment_consistency(prices_df)
3. Verify "AAPL" is NOT in the returned list
4. Verify known corporate actions do not trigger false positives

Expected: "AAPL" not flagged (legitimate split with proper adjustment should not be flagged)
"""

import pytest

from momo.data.validation import _check_adjustment_consistency


@pytest.mark.p1
@pytest.mark.unit
def test_1_4_unit_013(sample_price_df_with_aapl_split):
    """Test _check_adjustment_consistency() allows legitimate AAPL 7:1 split."""
    # Given: DataFrame with Apple's historical 7:1 split properly adjusted
    prices_df = sample_price_df_with_aapl_split

    # When: Call _check_adjustment_consistency()
    result = _check_adjustment_consistency(prices_df)

    # Then: "AAPL" should NOT be flagged (properly adjusted split)
    assert "AAPL" not in result, (
        "AAPL with properly adjusted 7:1 split should not be flagged. "
        "Adjusted prices remain consistent across split date."
    )

    # And: Result should be empty (no issues detected)
    assert len(result) == 0, f"Expected no adjustment issues, but found: {result}"
