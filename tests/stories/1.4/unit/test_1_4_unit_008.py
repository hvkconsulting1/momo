"""Test ID: 1.4-UNIT-008

Test that _check_date_gaps() detects 10-business-day gap.

Ref: docs/qa/assessments/1.4-test-design-20251205.md#14-unit-008-_check_date_gaps-detects-10-business-day-gap

Steps:
1. Load price DataFrame with 10-business-day gap for TSLA (2020-05-29 to 2020-06-15)
2. Call _check_date_gaps(prices_df)
3. Verify function returns {"TSLA": [(date(2020, 5, 29), date(2020, 6, 15))]}
4. Verify gap span is >= 10 business days
5. Verify other tickers are not in result (no false positives)

Expected: _check_date_gaps() correctly identifies 10-day gap for TSLA.
"""

from datetime import date

import pandas as pd
import pytest

from momo.data.validation import _check_date_gaps


@pytest.mark.p1
@pytest.mark.unit
def test_1_4_unit_008(sample_price_df_with_10day_gap: pd.DataFrame) -> None:
    """Test _check_date_gaps() detects 10-business-day gap."""
    # Step 1: Load price DataFrame with 10-day gap for TSLA (via fixture)
    prices_df = sample_price_df_with_10day_gap

    # Step 2: Call _check_date_gaps()
    result = _check_date_gaps(prices_df)

    # Step 3: Verify function detects gap for TSLA
    assert "TSLA" in result, f"Expected 'TSLA' in result, got: {result}"
    assert len(result["TSLA"]) == 1, f"Expected 1 gap for TSLA, got: {len(result['TSLA'])}"

    # Get the detected gap
    gap_start, gap_end = result["TSLA"][0]

    # Verify gap dates match fixture (last date before gap: 2020-05-29, first date after: 2020-06-15)
    assert gap_start == date(2020, 5, 29), f"Expected gap start 2020-05-29, got: {gap_start}"
    assert gap_end == date(2020, 6, 15), f"Expected gap end 2020-06-15, got: {gap_end}"

    # Step 4: Verify gap span is >= 10 business days
    # Count business days between 2020-05-29 and 2020-06-15
    business_days = pd.bdate_range(start=gap_start, end=gap_end, freq="B")
    gap_size = len(business_days) - 1  # Exclude endpoints from gap count
    assert gap_size >= 10, f"Expected gap >= 10 business days, got: {gap_size}"

    # Step 5: Verify other tickers are not flagged (no false positives)
    assert "AAPL" not in result, "AAPL should not have date gaps, but found in result"
    assert "MSFT" not in result, "MSFT should not have date gaps, but found in result"
    assert "GOOGL" not in result, "GOOGL should not have date gaps, but found in result"
    assert "AMZN" not in result, "AMZN should not have date gaps, but found in result"

    # Additional check: only TSLA should be in result
    assert len(result) == 1, f"Expected only TSLA in result, got: {result}"
