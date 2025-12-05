"""Test ID: 1.3-INT-007

Verify cache speedup >10x compared to API fetch for same dataset.

Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac6-cache-10x-faster-than-api

Steps:
1. Select 10 test symbols for 1 month date range
2. Fetch fresh data via API (force_refresh=True) and measure time
3. Load same data from cache and measure time
4. Calculate speedup ratio: API time / cache time
5. Assert speedup > 10x

Expected: Cache speedup >10x vs API fetch (validates AC6 performance requirement)

Note: This test requires NDU running on Windows. It will skip gracefully if NDU unavailable.
"""

import time
from datetime import date
from pathlib import Path
from unittest.mock import patch

import pytest

from momo.data.cache import load_prices
from momo.data.loader import load_universe
from momo.utils.exceptions import NDUNotRunningError, WindowsPythonNotFoundError


@pytest.mark.p1
@pytest.mark.integration
def test_1_3_int_007_cache_speedup_validation(temp_cache_dir: Path) -> None:
    """Test ID: 1.3-INT-007

    Story: 1.3 - Implement Data Loading and Parquet Caching
    Priority: P1
    Test Level: Integration
    Risk Coverage: PERF-001

    Verifies cache provides >10x speedup compared to API fetch for same dataset.
    Validates AC6 performance requirement.

    NOTE: Requires NDU running on Windows. Skips gracefully if unavailable.
    """
    # Step 1: Select 10 test symbols
    test_symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "NFLX", "AMD", "INTC"]
    start = date(2020, 1, 1)
    end = date(2020, 1, 31)
    universe = "perf_test_speedup"

    # Patch get_cache_path to use temp directory
    def mock_get_cache_path(universe_param: str, start_date: date, end_date: date) -> Path:
        filename = f"{universe_param}_{start_date.isoformat()}_{end_date.isoformat()}.parquet"
        return temp_cache_dir / filename

    try:
        with (
            patch("momo.data.cache.get_cache_path", side_effect=mock_get_cache_path),
            patch("momo.data.loader.cache.get_cache_path", side_effect=mock_get_cache_path),
        ):
            # Step 2: Fetch fresh data via API and measure time
            api_start_time = time.perf_counter()
            api_df = load_universe(
                symbols=test_symbols,
                start_date=start,
                end_date=end,
                universe=universe,
                force_refresh=True,  # Force bridge calls
            )
            api_end_time = time.perf_counter()
            api_time_ms = (api_end_time - api_start_time) * 1000

            # Verify API fetch succeeded
            assert len(api_df) > 0, "API fetch returned empty DataFrame"

            # Step 3: Load same data from cache and measure time (5 iterations for stable measurement)
            cache_times = []
            for _ in range(5):
                cache_start_time = time.perf_counter()
                cache_df = load_prices(universe=universe, start_date=start, end_date=end)
                cache_end_time = time.perf_counter()
                cache_times.append((cache_end_time - cache_start_time) * 1000)

                # Verify cache hit
                assert cache_df is not None, "Cache load failed (should have data from API fetch)"
                assert len(cache_df) == len(api_df), "Cache data doesn't match API data size"

            avg_cache_time_ms = sum(cache_times) / len(cache_times)

            # Step 4: Calculate speedup ratio
            speedup = api_time_ms / avg_cache_time_ms

            # Print performance summary
            print("\n✓ Performance Comparison:")
            print(f"  API fetch time:   {api_time_ms:.2f}ms")
            print(
                f"  Cache load time:  {avg_cache_time_ms:.2f}ms (avg over {len(cache_times)} iterations)"
            )
            print(f"  Cache iterations: {[f'{t:.2f}ms' for t in cache_times]}")
            print(f"  Speedup ratio:    {speedup:.1f}x")

            # Step 5: Assert speedup > 10x
            assert speedup > 10.0, (
                f"Cache speedup {speedup:.1f}x does not meet 10x requirement. "
                f"API: {api_time_ms:.2f}ms, Cache: {avg_cache_time_ms:.2f}ms"
            )

            print(f"✓ Cache speedup validated: {speedup:.1f}x > 10x (PASS)")

    except (NDUNotRunningError, WindowsPythonNotFoundError) as e:
        pytest.skip(f"NDU not available: {e}")
    except Exception as e:
        pytest.fail(f"Performance test failed unexpectedly: {e}")
