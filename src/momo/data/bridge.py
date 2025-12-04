"""Windows Python bridge for Norgate Data API access.

This module provides subprocess-based communication between WSL Python and Windows
Python to access the Norgate Data Updater (NDU) API.

Architecture:
    WSL Python → subprocess → Windows Python (python.exe) → norgatedata → NDU

See docs/architecture/windows-python-bridge.md for detailed documentation.
"""

import json
import subprocess
from datetime import date
from typing import Any

import pandas as pd
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
    except FileNotFoundError as e:
        logger.error("windows_python_not_found")
        raise WindowsPythonNotFoundError(
            "Windows Python (python.exe) not found. Ensure Windows Python is "
            "installed and in WSL PATH."
        ) from e
    except subprocess.TimeoutExpired as e:
        logger.error("bridge_timeout", timeout=timeout)
        raise NorgateBridgeError(
            f"Bridge operation timed out after {timeout} seconds. " "Check if NDU is responding."
        ) from e

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
        logger.error("bridge_execution_failed", stderr=result.stderr, stdout=result.stdout)
        raise NorgateBridgeError(
            f"Bridge execution failed:\nStderr: {result.stderr}\nStdout: {result.stdout}"
        )

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
        ) from e


def fetch_price_data(
    symbol: str,
    start_date: date | None = None,
    end_date: date | None = None,
    adjustment: str = "TOTALRETURN",
    timeout: int = 30,
) -> pd.DataFrame:
    """Fetch price data for a symbol via the Windows Python bridge.

    This function constructs a norgatedata API call to retrieve historical price
    data for a given symbol and returns it as a pandas DataFrame.

    DataFrame Schema:
        Columns:
            - date (datetime64[ns]): Trading date (index)
            - symbol (str): Ticker symbol
            - open (float64): Opening price (adjusted)
            - high (float64): High price (adjusted)
            - low (float64): Low price (adjusted)
            - close (float64): Closing price (adjusted)
            - volume (int64): Trading volume

    Args:
        symbol: Ticker symbol (e.g., "AAPL")
        start_date: Start date for price data (optional, defaults to earliest available)
        end_date: End date for price data (optional, defaults to most recent)
        adjustment: Price adjustment type - "TOTALRETURN" (default) or "CAPITAL"
        timeout: Subprocess timeout in seconds (default: 30)

    Returns:
        DataFrame with price data matching the schema above

    Raises:
        WindowsPythonNotFoundError: python.exe not found in PATH
        NDUNotRunningError: Norgate Data Updater is not running
        NorgateBridgeError: Bridge communication or data parsing errors

    Example:
        >>> from datetime import date
        >>> prices_df = fetch_price_data(
        ...     "AAPL", start_date=date(2023, 1, 1), end_date=date(2023, 12, 31)
        ... )
        >>> print(prices_df.head())
                    symbol    open    high     low   close     volume
        date
        2023-01-03   AAPL  125.07  125.27  124.17  125.07  112117471
        2023-01-04   AAPL  126.89  128.66  125.08  126.36   89113631
    """
    logger.info(
        "fetching_price_data",
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
        adjustment=adjustment,
    )

    # Construct norgatedata API call that returns DataFrame and serializes it
    # Use a function to encapsulate the logic and return the final result
    code_parts = [
        "(lambda: (",
        "norgatedata.price_timeseries(",
        f'"{symbol}"',
    ]

    if start_date:
        code_parts.append(f', start_date="{start_date.isoformat()}"')
    if end_date:
        code_parts.append(f', end_date="{end_date.isoformat()}"')

    code_parts.append(', timeseriesformat="pandas-dataframe"')
    code_parts.append(
        f", stock_price_adjustment_setting=norgatedata.StockPriceAdjustmentType.{adjustment}"
    )
    code_parts.append(")")

    # Chain DataFrame operations to serialize for JSON transfer
    # Convert dates to ISO format strings for JSON compatibility
    code_parts.append(".reset_index()")
    code_parts.append(".assign(Date=lambda x: x['Date'].astype(str))")
    code_parts.append(".to_dict('records')")
    code_parts.append("))()")

    code = "".join(code_parts)

    # Execute via bridge
    result = execute_norgate_code(code, timeout=timeout)

    # Parse result into DataFrame
    # Result is a list of dicts from df.to_dict('records')
    try:
        # Convert to DataFrame
        if not isinstance(result, list):
            raise ValueError(f"Expected list of records, got {type(result)}")

        prices_df = pd.DataFrame(result)

        # Normalize column names to lowercase
        prices_df.columns = prices_df.columns.str.lower()

        # Rename norgatedata columns to match our schema
        column_mapping = {
            "date": "date",
            "open": "open",
            "high": "high",
            "low": "low",
            "close": "close",
            "volume": "volume",
        }
        prices_df = prices_df.rename(columns=column_mapping)

        # Add symbol column
        prices_df["symbol"] = symbol

        # Select and reorder columns
        required_columns = ["date", "symbol", "open", "high", "low", "close", "volume"]
        prices_df = prices_df[required_columns]

        # Convert types
        prices_df["date"] = pd.to_datetime(prices_df["date"])
        prices_df["open"] = prices_df["open"].astype("float64")
        prices_df["high"] = prices_df["high"].astype("float64")
        prices_df["low"] = prices_df["low"].astype("float64")
        prices_df["close"] = prices_df["close"].astype("float64")
        prices_df["volume"] = prices_df["volume"].astype("int64")

        # Set date as index
        prices_df.set_index("date", inplace=True)
        prices_df.index.name = "date"

        logger.info("price_data_fetched", symbol=symbol, rows=len(prices_df))
        return prices_df

    except (KeyError, ValueError, TypeError) as e:
        logger.error("price_data_parse_failed", error=str(e), result_type=type(result))
        raise NorgateBridgeError(f"Failed to parse price data from bridge: {e}") from e


def check_ndu_status(timeout: int = 10) -> bool:
    """Check if Norgate Data Updater (NDU) is running and accessible.

    This function attempts to execute a simple norgatedata function via the
    bridge to verify NDU connectivity.

    Args:
        timeout: Subprocess timeout in seconds (default: 10)

    Returns:
        True if NDU is running and accessible, False otherwise

    Example:
        >>> if check_ndu_status():
        ...     print("NDU is available")
        ... else:
        ...     print("NDU is not running - please start it")
    """
    logger.info("checking_ndu_status")

    try:
        # Try a simple norgatedata call that requires NDU
        execute_norgate_code("norgatedata.databases()", timeout=timeout)
        logger.info("ndu_status_check", available=True)
        return True
    except NDUNotRunningError:
        logger.info("ndu_status_check", available=False)
        return False
    except Exception as e:
        logger.warning("ndu_status_check_failed", error=str(e))
        return False
