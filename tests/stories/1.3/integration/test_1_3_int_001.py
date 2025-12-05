"""Test ID: 1.3-INT-001

Integration test to verify fetched data includes dividend column when using
TOTALRETURN adjustment.

This test makes real bridge calls (requires NDU running) to verify the
adjustment type propagates correctly through the full stack.
"""

from datetime import date

import pandas as pd
import pytest

from momo.data.loader import load_universe


@pytest.mark.p0
@pytest.mark.integration
def test_1_3_int_001_totalreturn_includes_dividend(temp_cache_dir: str) -> None:
    """Test ID: 1.3-INT-001

    Story: 1.3 - Implement Data Loading and Parquet Caching
    Priority: P0
    Test Level: Integration
    Risk Coverage: DATA-001

    Verifies fetched data includes dividend column when using TOTALRETURN adjustment.

    Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac2-fetched-data-includes-adjustment-factors

    Steps:
    1. Call load_universe() with force_refresh=True (fetch from bridge)
    2. Verify bridge call uses TOTALRETURN adjustment (implicit in loader.py)
    3. Verify returned DataFrame includes 'dividend' column
    4. Verify dividend column has correct dtype (float64)
    5. Verify all required columns are present (OHLCV + unadjusted_close + dividend)

    Expected:
    - DataFrame includes 'dividend' column with float64 dtype
    - All price columns present with correct schema
    - TOTALRETURN adjustment successfully propagated to bridge

    Note:
    - This test requires NDU running on Windows
    - Uses a short date range (1 month) to minimize execution time
    - Uses well-known symbols (AAPL) for reliability
    """
    # Test configuration - minimal date range for fast execution
    symbols = ["AAPL"]
    start_date = date(2020, 1, 1)
    end_date = date(2020, 1, 31)
    universe = "test_totalreturn"

    # Fetch data with force_refresh to ensure bridge call
    result_df = load_universe(
        symbols=symbols,
        start_date=start_date,
        end_date=end_date,
        universe=universe,
        force_refresh=True,  # Force bridge call
    )

    # Verify DataFrame is not empty
    assert len(result_df) > 0, "Expected non-empty DataFrame from bridge fetch"

    # Verify dividend column exists
    assert (
        "dividend" in result_df.columns
    ), f"Expected 'dividend' column in result, got columns: {result_df.columns.tolist()}"

    # Verify dividend column has correct dtype
    assert (
        result_df["dividend"].dtype == "float64"
    ), f"Expected dividend dtype float64, got {result_df['dividend'].dtype}"

    # Verify all required columns are present
    required_columns = [
        "open",
        "high",
        "low",
        "close",
        "volume",
        "unadjusted_close",
        "dividend",
    ]
    for col in required_columns:
        assert col in result_df.columns, f"Expected column '{col}' in result DataFrame"

    # Verify column dtypes match schema
    expected_dtypes = {
        "open": "float64",
        "high": "float64",
        "low": "float64",
        "close": "float64",
        "volume": "int64",
        "unadjusted_close": "float64",
        "dividend": "float64",
    }

    for col, expected_dtype in expected_dtypes.items():
        actual_dtype = str(result_df[col].dtype)
        assert (
            actual_dtype == expected_dtype
        ), f"Column '{col}' has dtype {actual_dtype}, expected {expected_dtype}"

    # Verify MultiIndex structure
    assert isinstance(result_df.index, pd.MultiIndex), "Expected MultiIndex"
    assert result_df.index.names == [
        "date",
        "symbol",
    ], f"Expected index names ['date', 'symbol'], got {result_df.index.names}"

    # Verify date index has correct dtype
    date_dtype = result_df.index.get_level_values("date").dtype
    assert date_dtype == "datetime64[ns]", f"Expected datetime64[ns], got {date_dtype}"

    # Optional: Verify dividend values are reasonable (non-negative)
    # AAPL may or may not have paid dividends in Jan 2020, but values should be valid
    assert (result_df["dividend"] >= 0).all(), "Expected all dividend values >= 0"

    print("✓ TOTALRETURN adjustment verified - dividend column present with dtype float64")
    print(f"✓ Fetched {len(result_df)} rows for {symbols[0]} from {start_date} to {end_date}")
