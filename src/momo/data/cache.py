"""Parquet cache manager for price data.

This module provides functions to cache price data to local Parquet files for
offline operation and fast iteration.

Cache Path Convention:
    {universe}_{start_date}_{end_date}.parquet
    Example: russell_1000_cp_2010-01-01_2020-12-31.parquet
    Location: data/cache/prices/{filename}

Schema Requirements (from docs/architecture/data-models.md):
    - Index: MultiIndex (date: datetime64[ns], symbol: str)
    - Columns: open, high, low, close, volume, unadjusted_close, dividend
    - Required dtypes:
        * open: float64
        * high: float64
        * low: float64
        * close: float64
        * volume: int64
        * unadjusted_close: float64
        * dividend: float64
"""

from datetime import date
from pathlib import Path

import pandas as pd

from momo.utils.exceptions import CacheError


def get_cache_path(universe: str, start_date: date, end_date: date) -> Path:
    """Generate consistent cache file path for given parameters.

    Args:
        universe: Universe identifier (e.g., "russell_1000_cp")
        start_date: Start date of price data range
        end_date: End date of price data range

    Returns:
        Path object pointing to cache file location.
        Format: data/cache/prices/{universe}_{start_date}_{end_date}.parquet

    Examples:
        >>> get_cache_path("russell_1000_cp", date(2010, 1, 1), date(2020, 12, 31))
        Path('data/cache/prices/russell_1000_cp_2010-01-01_2020-12-31.parquet')
    """
    filename = f"{universe}_{start_date.isoformat()}_{end_date.isoformat()}.parquet"
    return Path("data") / "cache" / "prices" / filename


def _validate_price_schema(df: pd.DataFrame) -> None:
    """Validate DataFrame schema matches expected price data structure.

    This function performs comprehensive schema validation:
    1. Verifies all required columns are present
    2. Validates column dtypes match specification
    3. Ensures MultiIndex structure (date, symbol)
    4. Rejects empty DataFrames

    Args:
        df: DataFrame to validate

    Raises:
        CacheError: If validation fails with detailed error message:
            - Missing required columns
            - Incorrect column dtypes
            - Missing or incorrect MultiIndex structure
            - Empty DataFrame (0 rows)

    Schema Requirements:
        - Index: MultiIndex with names ['date', 'symbol']
        - Index levels: (datetime64[ns], object for strings)
        - Columns: open, high, low, close, volume, unadjusted_close, dividend
        - Dtypes: float64 for prices/dividends, int64 for volume
    """
    # Check 1: DataFrame must not be empty
    if len(df) == 0:
        raise CacheError("Cannot cache empty DataFrame (0 rows)")

    # Check 2: Required columns must be present
    required_columns = {
        "open",
        "high",
        "low",
        "close",
        "volume",
        "unadjusted_close",
        "dividend",
    }
    actual_columns = set(df.columns)
    missing_columns = required_columns - actual_columns

    if missing_columns:
        raise CacheError(
            f"Missing required columns: {sorted(missing_columns)}. "
            f"Expected: {sorted(required_columns)}"
        )

    # Check 3: Column dtypes must match specification
    expected_dtypes = {
        "open": "float64",
        "high": "float64",
        "low": "float64",
        "close": "float64",
        "volume": "int64",
        "unadjusted_close": "float64",
        "dividend": "float64",
    }

    dtype_mismatches = []
    for col, expected_dtype in expected_dtypes.items():
        actual_dtype = str(df[col].dtype)
        if actual_dtype != expected_dtype:
            dtype_mismatches.append(f"{col}: expected {expected_dtype}, got {actual_dtype}")

    if dtype_mismatches:
        raise CacheError("Column dtype mismatches:\n  " + "\n  ".join(dtype_mismatches))

    # Check 4: Must have MultiIndex with (date, symbol)
    if not isinstance(df.index, pd.MultiIndex):
        raise CacheError(
            f"Expected MultiIndex, got {type(df.index).__name__}. "
            "Price data must use MultiIndex with (date, symbol) levels."
        )

    # Check 5: MultiIndex must have correct names
    expected_index_names = ["date", "symbol"]
    actual_index_names = list(df.index.names)

    if actual_index_names != expected_index_names:
        raise CacheError(
            f"MultiIndex names mismatch: expected {expected_index_names}, "
            f"got {actual_index_names}"
        )


def save_prices(df: pd.DataFrame, universe: str, start_date: date, end_date: date) -> Path:
    """Save price DataFrame to Parquet cache with validation.

    This function validates the DataFrame schema and writes it to a Parquet file
    using the pyarrow engine with snappy compression. Cache directories are
    created automatically if they don't exist.

    Args:
        df: Price data DataFrame to cache
        universe: Universe identifier (e.g., "russell_1000_cp")
        start_date: Start date of price data range
        end_date: End date of price data range

    Returns:
        Path to the saved Parquet file

    Raises:
        CacheError: If schema validation fails or write operation encounters errors

    Schema Requirements:
        See _validate_price_schema() for detailed validation rules.
        DataFrame must have MultiIndex (date, symbol) and all required columns
        with correct dtypes.

    Examples:
        >>> prices_df = load_from_api(symbols, start_date, end_date)
        >>> cache_path = save_prices(prices_df, "russell_1000_cp", start_date, end_date)
        >>> print(f"Cached to {cache_path}")
    """
    # Validate schema before writing
    _validate_price_schema(df)

    # Get cache path and ensure directory exists
    cache_path = get_cache_path(universe, start_date, end_date)
    cache_path.parent.mkdir(parents=True, exist_ok=True)

    # Write to Parquet with pyarrow engine and snappy compression
    df.to_parquet(cache_path, engine="pyarrow", compression="snappy")

    return cache_path


def load_prices(universe: str, start_date: date, end_date: date) -> pd.DataFrame | None:
    """Load price DataFrame from Parquet cache if it exists.

    This function checks if a cached Parquet file exists for the given parameters
    and loads it if present. The MultiIndex structure is preserved during loading.

    Args:
        universe: Universe identifier (e.g., "russell_1000_cp")
        start_date: Start date of price data range
        end_date: End date of price data range

    Returns:
        Price DataFrame with MultiIndex (date, symbol) if cache exists,
        None if cache file does not exist

    Examples:
        >>> prices_df = load_prices("russell_1000_cp", date(2010, 1, 1), date(2020, 12, 31))
        >>> if prices_df is None:
        ...     # Cache miss - fetch from API
        ...     prices_df = fetch_from_api(...)
        >>> else:
        ...     # Cache hit - use cached data
        ...     print(f"Loaded {len(prices_df)} rows from cache")
    """
    cache_path = get_cache_path(universe, start_date, end_date)

    # Return None if cache doesn't exist
    if not cache_path.exists():
        return None

    # Load from Parquet using pyarrow engine (preserves MultiIndex)
    df = pd.read_parquet(cache_path, engine="pyarrow")

    return df
