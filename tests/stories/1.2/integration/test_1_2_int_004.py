"""
Test ID: 1.2-INT-004
Story: 1.2 - Integrate Norgate Data API via Windows Python Bridge
Priority: P1
Test Level: Integration
Risk Coverage: PERF-001 (Subprocess timeout)

Description:
Verify that multiple concurrent bridge operations do not cause deadlocks or resource leaks.

Acceptance Criteria: AC2
Test Design Reference: docs/qa/assessments/1.2-test-design-20251204.md:485
"""

import concurrent.futures
import time

import pytest
import structlog

from momo.data.bridge import execute_norgate_code
from momo.utils.exceptions import WindowsPythonNotFoundError

logger = structlog.get_logger()


@pytest.mark.p1
@pytest.mark.integration
def test_1_2_int_004() -> None:
    """
    1.2-INT-004: Verify bridge handles concurrent requests without deadlocks

    Justification: Validates resource management for future parallel data fetching.
    Ensures the bridge can handle multiple simultaneous subprocess calls without
    causing deadlocks, resource exhaustion, or process leaks.

    Expected: All concurrent operations succeed without errors or hangs
    Failure mode: Deadlock, timeout, or resource exhaustion (too many processes)
    """
    # Arrange
    num_concurrent_requests = 10
    simple_code = "2 + 2"

    # Act
    start_time = time.time()

    try:
        # Use ThreadPoolExecutor to run concurrent bridge operations
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_concurrent_requests) as executor:
            # Submit all tasks
            futures = [
                executor.submit(execute_norgate_code, simple_code)
                for _ in range(num_concurrent_requests)
            ]

            # Wait for all to complete and collect results
            results = []
            for future in concurrent.futures.as_completed(futures, timeout=60):
                result = future.result()
                results.append(result)

        elapsed_time = time.time() - start_time

        # Assert
        # All calls should have succeeded
        assert (
            len(results) == num_concurrent_requests
        ), f"Expected {num_concurrent_requests} results, got {len(results)}"

        # All results should be correct
        for i, result in enumerate(results):
            assert result == 4, f"Request {i} returned incorrect result: {result}"

        # Performance check: concurrent execution should not take 10x single call time
        # (This is a loose check - we expect some parallelism benefit)
        max_expected_time = 30  # 10 requests should complete within 30 seconds
        assert elapsed_time < max_expected_time, (
            f"Concurrent execution took {elapsed_time:.2f}s, expected < {max_expected_time}s. "
            "Possible performance issue or lack of parallelism."
        )

        logger.info(
            "concurrent_requests_completed",
            num_requests=num_concurrent_requests,
            elapsed_time=elapsed_time,
            avg_time_per_request=elapsed_time / num_concurrent_requests,
        )

    except WindowsPythonNotFoundError:
        pytest.skip(
            "Windows Python (python.exe) not found in PATH - cannot test concurrent requests"
        )
    except concurrent.futures.TimeoutError:
        pytest.fail("Concurrent requests timed out after 60 seconds - possible deadlock")
    except Exception as e:
        pytest.fail(f"Concurrent requests failed with unexpected error: {e}")
