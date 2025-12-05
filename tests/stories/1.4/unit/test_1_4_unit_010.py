"""Test ID: 1.4-UNIT-010

Test that _check_date_gaps() ignores known market holidays.

Ref: docs/qa/assessments/1.4-test-design-20251205.md#14-unit-010-_check_date_gaps-ignores-known-market-holidays

Steps:
1. Load price DataFrame missing 2020-07-03 (Independence Day observed, Friday)
2. Call _check_date_gaps(prices_df)
3. Verify function returns {} (no gaps detected for known market holiday)
4. Verify market holiday does not trigger false positive

Expected: _check_date_gaps() returns empty dict, market holiday not flagged.

Note: This test documents the limitation that without NYSE holiday calendar,
      single-day holidays are not explicitly recognized, but the 10-day threshold
      prevents them from being flagged as suspicious gaps.
"""

import pandas as pd
import pytest

from momo.data.validation import _check_date_gaps


@pytest.mark.p1
@pytest.mark.unit
def test_1_4_unit_010(sample_price_df_with_july4_missing: pd.DataFrame) -> None:
    """Test _check_date_gaps() ignores known market holidays."""
    # Step 1: Load price DataFrame missing July 3, 2020 (via fixture)
    prices_df = sample_price_df_with_july4_missing

    # Step 2: Call _check_date_gaps()
    result = _check_date_gaps(prices_df)

    # Step 3: Verify function returns empty dict (no gaps detected)
    assert len(result) == 0, f"Expected no gaps detected, but found: {result}"

    # Step 4: Verify market holiday does not trigger false positive
    # The fixture has dates: 2020-07-01 (Wed), 2020-07-02 (Thu), 2020-07-06 (Mon)
    # Missing: 2020-07-03 (Fri, Independence Day observed)
    # Gap from Thu to Mon (spanning weekend + holiday) is only 1 business day
    # Should not exceed 10-day threshold

    # Verify all tickers have no gaps detected
    for ticker in ["AAPL", "MSFT", "GOOGL"]:
        assert ticker not in result, f"{ticker} should not have gaps, but found in result"

    # Additional verification: check fixture dates are correct
    dates = prices_df.index.get_level_values("date").unique().sort_values()
    assert len(dates) == 3, f"Expected 3 dates in fixture, got: {len(dates)}"
    assert dates[0].date().isoformat() == "2020-07-01", "Expected first date 2020-07-01"
    assert dates[1].date().isoformat() == "2020-07-02", "Expected second date 2020-07-02"
    assert dates[2].date().isoformat() == "2020-07-06", "Expected third date 2020-07-06"
