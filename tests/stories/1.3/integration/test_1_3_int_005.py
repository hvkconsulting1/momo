"""Test ID: 1.3-INT-005

Verify cache load time <50ms for 10-symbol dataset.

Ref: docs/qa/assessments/1.3-test-design-20251204.md#ac6-cache-10x-faster-than-api

Steps:
1. Create sample 10-symbol dataset for 1 month (Jan 2020)
2. Save dataset to cache using save_prices()
3. Measure cache load time using time.perf_counter()
4. Assert load time < 50ms

Expected: Cache load completes in <50ms (establishes performance baseline)
"""

import time
from datetime import date
from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest

from momo.data.cache import load_prices, save_prices


@pytest.mark.p1
@pytest.mark.integration
def test_1_3_int_005_cache_load_performance(temp_cache_dir: Path) -> None:
    """Test ID: 1.3-INT-005

    Story: 1.3 - Implement Data Loading and Parquet Caching
    Priority: P1
    Test Level: Integration
    Risk Coverage: PERF-001

    Verifies cache load time <50ms for 10-symbol dataset (1 month).
    Establishes baseline for performance monitoring.
    """
    # Step 1: Create sample 10-symbol dataset for 1 month
    test_symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "NFLX", "AMD", "INTC"]
    start = date(2020, 1, 1)
    end = date(2020, 1, 31)

    # Generate 31 trading days (assume all days for simplicity)
    dates = pd.date_range(start, end, freq="D")

    # Create sample data with correct schema
    data = {
        "open": [100.0] * (len(dates) * len(test_symbols)),
        "high": [105.0] * (len(dates) * len(test_symbols)),
        "low": [95.0] * (len(dates) * len(test_symbols)),
        "close": [102.0] * (len(dates) * len(test_symbols)),
        "volume": [1000000] * (len(dates) * len(test_symbols)),
        "unadjusted_close": [102.0] * (len(dates) * len(test_symbols)),
        "dividend": [0.0] * (len(dates) * len(test_symbols)),
    }

    index = pd.MultiIndex.from_product([dates, test_symbols], names=["date", "symbol"])
    sample_df = pd.DataFrame(data, index=index)

    # Step 2: Save dataset to cache
    universe = "perf_test_cache"

    # Patch get_cache_path to use temp directory
    def mock_get_cache_path(universe_param: str, start_date: date, end_date: date) -> Path:
        filename = f"{universe_param}_{start_date.isoformat()}_{end_date.isoformat()}.parquet"
        return temp_cache_dir / filename

    with patch("momo.data.cache.get_cache_path", side_effect=mock_get_cache_path):
        save_prices(sample_df, universe=universe, start_date=start, end_date=end)

        # Step 3: Measure cache load time (5 iterations to get stable measurement)
        load_times = []
        for _ in range(5):
            start_time = time.perf_counter()
            loaded_df = load_prices(universe=universe, start_date=start, end_date=end)
            end_time = time.perf_counter()
            load_times.append((end_time - start_time) * 1000)  # Convert to milliseconds

            # Sanity check: verify data loaded correctly
            assert loaded_df is not None
            assert len(loaded_df) == len(sample_df)

    # Step 4: Assert average load time < 50ms
    avg_load_time = sum(load_times) / len(load_times)
    print(f"\n✓ Cache load time: {avg_load_time:.2f}ms (avg over {len(load_times)} iterations)")
    print(f"  Iterations: {[f'{t:.2f}ms' for t in load_times]}")

    assert avg_load_time < 50.0, (
        f"Cache load time {avg_load_time:.2f}ms exceeds 50ms threshold. "
        f"Performance regression detected."
    )

    print(f"✓ Cache load performance validated: {avg_load_time:.2f}ms < 50ms (PASS)")
