"""Test ID: 1.4-UNIT-009

Test that _check_date_gaps() ignores weekend gaps.

Ref: docs/qa/assessments/1.4-test-design-20251205.md#14-unit-009-_check_date_gaps-ignores-weekend-gaps

Steps:
1. Load price DataFrame with continuous weekday data (no weekend price data)
2. Call _check_date_gaps(prices_df)
3. Verify function returns {} (no gaps detected)
4. Verify weekend gaps do not trigger false positives

Expected: _check_date_gaps() returns empty dict, no weekend gaps flagged.
"""

import pandas as pd
import pytest

from momo.data.validation import _check_date_gaps


@pytest.mark.p1
@pytest.mark.unit
def test_1_4_unit_009(sample_price_df_with_weekends_missing: pd.DataFrame) -> None:
    """Test _check_date_gaps() ignores weekend gaps."""
    # Step 1: Load price DataFrame with weekday-only data (via fixture)
    prices_df = sample_price_df_with_weekends_missing

    # Step 2: Call _check_date_gaps()
    result = _check_date_gaps(prices_df)

    # Step 3: Verify function returns empty dict (no gaps detected)
    assert len(result) == 0, f"Expected no gaps detected, but found: {result}"

    # Step 4: Verify weekend gaps don't trigger false positives
    # Additional verification: check that fixture indeed has weekday-only dates
    dates = prices_df.index.get_level_values("date").unique()
    weekdays = [d.weekday() for d in dates]  # Monday=0, Sunday=6
    assert all(wd < 5 for wd in weekdays), "Fixture should only contain weekdays (Mon-Fri)"

    # Verify consecutive weekdays don't create false positive gaps
    # (e.g., Friday to Monday should not be flagged as a 3-day gap)
    for ticker in ["AAPL", "MSFT", "GOOGL"]:
        assert ticker not in result, f"{ticker} should not have gaps, but found in result"
