"""Windows Python bridge for Norgate Data API access.

This module provides subprocess-based communication between WSL Python and Windows
Python to access the Norgate Data Updater (NDU) API.

Architecture:
    WSL Python → subprocess → Windows Python (python.exe) → norgatedata → NDU

See docs/architecture/windows-python-bridge.md for detailed documentation.
"""

import json
import subprocess
from typing import Any

import structlog
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from momo.utils.exceptions import (
    NDUNotRunningError,
    NorgateBridgeError,
    WindowsPythonNotFoundError,
)

logger = structlog.get_logger()


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(1),
    retry=retry_if_exception_type((ConnectionError, OSError)),
    reraise=True,
)
def execute_norgate_code(code: str, timeout: int = 30) -> Any:
    """Execute Python code via Windows Python and return parsed result.

    This function wraps Python code with JSON serialization and executes it
    via Windows Python (python.exe) using subprocess. Results are transferred
    back to WSL Python via JSON.

    Args:
        code: Python code to execute (must evaluate to a JSON-serializable result)
        timeout: Subprocess timeout in seconds (default: 30)

    Returns:
        Parsed result from executed code (deserialized from JSON)

    Raises:
        WindowsPythonNotFoundError: python.exe not found in PATH
        NDUNotRunningError: Norgate Data Updater is not running
        NorgateBridgeError: Other bridge communication errors (timeout, JSON parse, etc.)

    Example:
        >>> result = execute_norgate_code("2 + 2")
        >>> assert result == 4
        >>> version = execute_norgate_code("norgatedata.version()")
        >>> print(version)  # "1.0.74"
    """
    logger.info("executing_norgate_code", code_length=len(code))

    # Construct wrapper code with JSON serialization
    wrapper = f"""
import json
import norgatedata
result = {code}
print(json.dumps(result, default=str))
"""

    try:
        result = subprocess.run(
            ["python.exe", "-c", wrapper],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError:
        logger.error("windows_python_not_found")
        raise WindowsPythonNotFoundError(
            "Windows Python (python.exe) not found. Ensure Windows Python is "
            "installed and in WSL PATH."
        )
    except subprocess.TimeoutExpired:
        logger.error("bridge_timeout", timeout=timeout)
        raise NorgateBridgeError(
            f"Bridge operation timed out after {timeout} seconds. "
            "Check if NDU is responding."
        )

    # Check for errors in subprocess execution
    if result.returncode != 0:
        # Check for specific error patterns
        if "NDU is not running" in result.stderr:
            logger.error("ndu_not_running")
            raise NDUNotRunningError(
                "Norgate Data Updater is not running. Please start NDU on Windows "
                "and ensure you're logged in."
            )

        # Check for norgatedata import errors
        if "ModuleNotFoundError" in result.stderr and "norgatedata" in result.stderr:
            logger.error("norgatedata_not_installed")
            raise NorgateBridgeError(
                "norgatedata package not found in Windows Python. "
                "Install via: pip install norgatedata==1.0.74"
            )

        # Generic error
        logger.error("bridge_execution_failed", stderr=result.stderr)
        raise NorgateBridgeError(f"Bridge execution failed: {result.stderr}")

    # Parse JSON from last line (skip norgatedata INFO messages)
    try:
        output_lines = result.stdout.strip().split("\n")
        json_line = output_lines[-1]
        parsed_result = json.loads(json_line)
        logger.info("norgate_code_executed", success=True)
        return parsed_result
    except (json.JSONDecodeError, IndexError) as e:
        logger.error("json_parse_failed", error=str(e), stdout=result.stdout)
        raise NorgateBridgeError(
            f"Failed to parse bridge output: {e}\nOutput: {result.stdout}"
        )
