"""Test ID: 1.4-INT-003

Story: 1.4 - Build Data Quality Validation Pipeline
Priority: P1
Test Level: Integration
Risk Coverage: PERF-001

Validation performance on 100-ticker universe completes in < 5 seconds.
"""

import time

import pandas as pd
import pytest

from momo.data.validation import ValidationReport, validate_prices


@pytest.mark.p1
@pytest.mark.integration
def test_1_4_int_003(sample_price_df_100tickers: pd.DataFrame) -> None:
    """Test ID: 1.4-INT-003

    Verify validation performance meets < 5s requirement for 100-ticker universe.

    Ref: docs/qa/assessments/1.4-test-design-20251205.md#integration-tests

    Steps:
    1. Load 100-ticker price DataFrame (252 trading days = 1 year)
    2. Measure execution time of validate_prices()
    3. Verify execution completes in < 5.0 seconds
    4. Verify ValidationReport is returned successfully
    5. Log performance metrics for observability

    Expected: Validation completes in < 5 seconds with valid ValidationReport returned
    """
    # Step 1: Verify fixture data structure
    assert isinstance(sample_price_df_100tickers, pd.DataFrame)
    assert sample_price_df_100tickers.index.names == ["date", "symbol"]

    # Verify expected data size: 100 tickers x 252 days = 25,200 rows
    expected_rows = 100 * 252
    assert (
        len(sample_price_df_100tickers) == expected_rows
    ), f"Expected {expected_rows} rows, got {len(sample_price_df_100tickers)}"

    # Step 2: Measure execution time of validate_prices()
    start_time = time.time()
    result = validate_prices(sample_price_df_100tickers, check_delistings=True)
    elapsed_time = time.time() - start_time

    # Step 3: Verify execution completes in < 5.0 seconds
    assert (
        elapsed_time < 5.0
    ), f"Validation took {elapsed_time:.2f}s, expected < 5.0s (performance requirement)"

    # Step 4: Verify ValidationReport is returned successfully
    assert isinstance(result, ValidationReport), "Expected ValidationReport instance"
    assert result.total_tickers == 100, f"Expected 100 tickers, got {result.total_tickers}"

    # Step 5: Log performance metrics for observability
    print("\nPerformance Metrics:")
    print(f"  Data size: {len(sample_price_df_100tickers):,} rows")
    print(f"  Tickers: {result.total_tickers}")
    print(f"  Date range: {result.date_range[0]} to {result.date_range[1]}")
    print(f"  Execution time: {elapsed_time:.3f}s")
    print(f"  Throughput: {len(sample_price_df_100tickers) / elapsed_time:.0f} rows/sec")
    print(f"  Validation status: {'VALID' if result.is_valid else 'INVALID'}")
