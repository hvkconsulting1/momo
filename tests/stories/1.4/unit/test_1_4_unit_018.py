"""Test ID: 1.4-UNIT-018

Verify check_delisting_status() returns last trading date for delisted ticker.

Ref: docs/qa/assessments/1.4-test-design-20251205.md#1.4-unit-018

Steps:
1. Load prices DataFrame with ticker ABC delisted on 2019-06-15
2. Call check_delisting_status() with query_end_date = 2020-01-01
3. Verify result dict contains "ABC" as key
4. Verify result["ABC"] is the last date in ABC's price time series (2019-06-15)

Expected: ABC is flagged as delisted with last trading date 2019-06-15
"""

from __future__ import annotations

from datetime import date

import pytest

from momo.data.validation import check_delisting_status


@pytest.mark.p1
@pytest.mark.unit
def test_1_4_unit_018(sample_price_df_with_recent_delisting) -> None:  # type: ignore[no-untyped-def]
    """Test check_delisting_status() returns last trading date.

    Uses ticker ABC with delisting date 2019-06-15 and query end date of 2020-01-01.
    The gap of ~200 days should trigger delisting detection (threshold = 30 days).
    """
    # Step 1: Load prices DataFrame (provided by fixture)
    prices_df = sample_price_df_with_recent_delisting

    # Step 2: Call check_delisting_status() with query_end_date = 2020-01-01
    query_end_date = date(2020, 1, 1)
    result = check_delisting_status(prices_df, query_end_date=query_end_date, threshold_days=30)

    # Step 3: Verify result dict contains "ABC" as key
    assert "ABC" in result, "ABC should be detected as delisted"

    # Step 4: Verify result["ABC"] is the last date in ABC's time series
    # Fixture creates ABC data ending June 15, 2019 (last business day in range 2019-06-10 to 2019-06-15)
    expected_delisting_date = date(2019, 6, 14)  # Fri (last business day of week)
    assert (
        result["ABC"] == expected_delisting_date
    ), f"Expected last trading date {expected_delisting_date}, got {result['ABC']}"

    # Verify the gap is indeed > 30 days
    gap_days = (query_end_date - result["ABC"]).days
    assert gap_days > 30, f"Gap should be > 30 days, got {gap_days} days"

    # Verify other tickers (AAPL, MSFT) are NOT flagged
    assert "AAPL" not in result, "AAPL should not be flagged as delisted"
    assert "MSFT" not in result, "MSFT should not be flagged as delisted"
