"""Test ID: 1.3-INT-006

Verify API fetch time ~500ms for 10 symbols (establishes baseline).

Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac6-cache-10x-faster-than-api

Steps:
1. Select 10 test symbols (AAPL, MSFT, GOOGL, AMZN, TSLA, NVDA, META, NFLX, AMD, INTC)
2. Use load_universe() with force_refresh=True to bypass cache and fetch fresh data
3. Measure total fetch time using time.perf_counter()
4. Document baseline performance in test output

Expected: API fetch time ~500ms ±50% for 10 symbols over 1 month (baseline for future optimization)

Note: This test requires NDU running on Windows. It will skip gracefully if NDU unavailable.
"""

import time
from datetime import date
from pathlib import Path
from unittest.mock import patch

import pytest

from momo.data.loader import load_universe
from momo.utils.exceptions import NDUNotRunningError, WindowsPythonNotFoundError


@pytest.mark.p2
@pytest.mark.integration
def test_1_3_int_006_api_fetch_baseline(temp_cache_dir: Path) -> None:
    """Test ID: 1.3-INT-006

    Story: 1.3 - Implement Data Loading and Parquet Caching
    Priority: P2
    Test Level: Integration
    Risk Coverage: PERF-001

    Verifies API fetch time ~500ms for 10 symbols over 1 month.
    Documents baseline performance for future optimization stories.

    NOTE: Requires NDU running on Windows. Skips gracefully if unavailable.
    """
    # Step 1: Select 10 test symbols
    test_symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "NFLX", "AMD", "INTC"]
    start = date(2020, 1, 1)
    end = date(2020, 1, 31)
    universe = "perf_test_api"

    # Step 2: Fetch fresh data via bridge (bypass cache)
    # Patch get_cache_path to use temp directory
    def mock_get_cache_path(universe_param: str, start_date: date, end_date: date) -> Path:
        filename = f"{universe_param}_{start_date.isoformat()}_{end_date.isoformat()}.parquet"
        return temp_cache_dir / filename

    try:
        with (
            patch("momo.data.cache.get_cache_path", side_effect=mock_get_cache_path),
            patch("momo.data.loader.cache.get_cache_path", side_effect=mock_get_cache_path),
        ):
            # Step 3: Measure fetch time
            start_time = time.perf_counter()
            result_df = load_universe(
                symbols=test_symbols,
                start_date=start,
                end_date=end,
                universe=universe,
                force_refresh=True,  # Force bridge calls
            )
            end_time = time.perf_counter()

        fetch_time_ms = (end_time - start_time) * 1000

        # Verify fetch succeeded
        assert len(result_df) > 0, "API fetch returned empty DataFrame"
        assert all(
            symbol in result_df.index.get_level_values("symbol").unique() for symbol in test_symbols
        ), "Not all symbols fetched successfully"

        # Step 4: Document baseline performance
        print(f"\n✓ API fetch time: {fetch_time_ms:.2f}ms for {len(test_symbols)} symbols")
        print(f"  Date range: {start} to {end} (1 month)")
        print(f"  Symbols: {', '.join(test_symbols)}")
        print(f"  Rows fetched: {len(result_df)}")

        # Allow ±50% tolerance (baseline is informational, not strict SLA)
        expected_time = 500.0
        lower_bound = expected_time * 0.5  # 250ms
        upper_bound = expected_time * 1.5  # 750ms

        if lower_bound <= fetch_time_ms <= upper_bound:
            print("✓ API fetch baseline within expected range: ~500ms ±50% (PASS)")
        else:
            print(
                f"⚠ API fetch time {fetch_time_ms:.2f}ms outside expected range "
                f"[{lower_bound:.0f}ms, {upper_bound:.0f}ms]"
            )
            print("  (Baseline test - informational only, not blocking)")

    except (NDUNotRunningError, WindowsPythonNotFoundError) as e:
        pytest.skip(f"NDU not available: {e}")
    except Exception as e:
        pytest.fail(f"API fetch failed unexpectedly: {e}")
