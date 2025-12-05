"""Test ID: 1.3-INT-010

Integration test to verify cache consistency when mix of valid and invalid
symbols are fetched (partial failure scenario).

This test validates that partial results are cached correctly and can be
retrieved, ensuring graceful degradation in production scenarios.
"""

from datetime import date
from unittest.mock import patch

import pandas as pd
import pytest

from momo.data import cache
from momo.data.loader import load_universe
from momo.utils.exceptions import NorgateBridgeError


@pytest.mark.p0
@pytest.mark.integration
def test_1_3_int_010_cache_consistency_partial_failures(
    sample_price_df: pd.DataFrame,
    temp_cache_dir: str,
) -> None:
    """Test ID: 1.3-INT-010

    Story: 1.3 - Implement Data Loading and Parquet Caching
    Priority: P0
    Test Level: Integration
    Risk Coverage: TECH-002

    Verifies cache consistency when mix of valid and invalid symbols fetched.

    Ref: docs/qa/assessments/1.3-test-design-20251204.md#tech-002-bridge-integration-error-handling

    Steps:
    1. Mock bridge to fail for specific symbols (simulate partial failure)
    2. Call load_universe() with mix of valid and invalid symbols
    3. Verify partial results are saved to cache using actual filesystem
    4. Load data from cache using cache.load_prices()
    5. Verify cached data contains only successfully fetched symbols
    6. Verify cached data has correct schema and dtypes
    7. Verify second call to load_universe() returns cached partial results

    Expected:
    - Partial results successfully saved to cache (real Parquet I/O)
    - Cached data includes only successful symbols
    - Cache load returns same data (round-trip consistency)
    - Schema validation passes for partial data
    """
    # Test configuration
    symbols = ["AAPL", "INVALID_XYZ", "MSFT", "BAD_SYMBOL", "GOOGL"]
    start_date = date(2020, 1, 1)
    end_date = date(2020, 1, 10)
    universe = "test_partial_cache"

    # Create mock DataFrames for successful symbols
    aapl_df = sample_price_df[sample_price_df.index.get_level_values("symbol") == "AAPL"]
    msft_df = sample_price_df[sample_price_df.index.get_level_values("symbol") == "MSFT"]
    googl_df = sample_price_df[sample_price_df.index.get_level_values("symbol") == "GOOGL"]

    # Mock fetch_price_data to fail for specific symbols
    def mock_fetch_partial_failure(symbol: str, **kwargs):  # type: ignore[no-untyped-def]
        if symbol in ["INVALID_XYZ", "BAD_SYMBOL"]:
            raise NorgateBridgeError(f"Symbol not found: {symbol}")
        elif symbol == "AAPL":
            return aapl_df
        elif symbol == "MSFT":
            return msft_df
        elif symbol == "GOOGL":
            return googl_df
        else:
            raise ValueError(f"Unexpected symbol: {symbol}")

    with patch(
        "momo.data.loader.bridge.fetch_price_data",
        side_effect=mock_fetch_partial_failure,
    ):
        # Step 1-2: Fetch with partial failures
        first_result = load_universe(
            symbols=symbols,
            start_date=start_date,
            end_date=end_date,
            universe=universe,
            force_refresh=True,
        )

        # Verify first result contains only successful symbols
        first_symbols = first_result.index.get_level_values("symbol").unique().tolist()
        assert set(first_symbols) == {
            "AAPL",
            "MSFT",
            "GOOGL",
        }, f"Expected successful symbols only, got {first_symbols}"

    # Step 3-4: Load from cache using actual cache layer
    cached_df = cache.load_prices(
        universe=universe,
        start_date=start_date,
        end_date=end_date,
    )

    # Step 5: Verify cached data exists and matches
    assert cached_df is not None, "Expected cached data to exist after partial fetch"

    cached_symbols = cached_df.index.get_level_values("symbol").unique().tolist()
    assert set(cached_symbols) == {
        "AAPL",
        "MSFT",
        "GOOGL",
    }, f"Expected cached data to contain only successful symbols, got {cached_symbols}"

    # Step 6: Verify schema and dtypes
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
        assert col in cached_df.columns, f"Expected column '{col}' in cached data"

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
        actual_dtype = str(cached_df[col].dtype)
        assert (
            actual_dtype == expected_dtype
        ), f"Cached data column '{col}' has dtype {actual_dtype}, expected {expected_dtype}"

    # Verify MultiIndex preserved
    assert isinstance(cached_df.index, pd.MultiIndex), "Expected MultiIndex in cached data"
    assert cached_df.index.names == [
        "date",
        "symbol",
    ], f"Expected index names ['date', 'symbol'], got {cached_df.index.names}"

    # Step 7: Second load_universe() call should return cached partial results
    # Mock bridge again to verify it's NOT called (cache hit)
    with patch(
        "momo.data.loader.bridge.fetch_price_data",
        side_effect=lambda *args, **kwargs: pytest.fail("Bridge should not be called on cache hit"),
    ):
        second_result = load_universe(
            symbols=symbols,  # Same symbols as before
            start_date=start_date,
            end_date=end_date,
            universe=universe,
            force_refresh=False,  # Allow cache hit
        )

        # Verify second result matches cached data (same partial results)
        second_symbols = second_result.index.get_level_values("symbol").unique().tolist()
        assert set(second_symbols) == {
            "AAPL",
            "MSFT",
            "GOOGL",
        }, f"Expected cache hit to return partial results, got {second_symbols}"

        # Verify data equality (round-trip consistency)
        pd.testing.assert_frame_equal(
            second_result.sort_index(),
            cached_df.sort_index(),
            check_dtype=True,
            check_index_type=True,
        )

    print("✓ Cache consistency verified for partial failure scenario")
    print("✓ Partial results (3 of 5 symbols) successfully cached and retrieved")
    print("✓ Round-trip cache consistency validated")
