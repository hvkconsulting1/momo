"""Custom exceptions for the momo project.

This module defines exception classes for various error scenarios throughout
the application, with a focus on bridge communication errors between WSL and
Windows Python environments.
"""


class BridgeError(Exception):
    """Base exception for Windows Python bridge errors.

    Raised when communication between WSL Python and Windows Python fails.
    This is the base class for all bridge-related exceptions.

    Examples of scenarios:
    - Windows Python executable not found
    - Subprocess communication failures
    - JSON serialization/deserialization errors
    """

    pass


class NorgateBridgeError(BridgeError):
    """Norgate Data API errors via bridge.

    Raised when errors occur during Norgate Data API operations executed
    via the Windows Python bridge.

    Examples of scenarios:
    - norgatedata package not installed in Windows Python
    - NDU (Norgate Data Updater) communication failures
    - Timeout during data retrieval
    - Subprocess execution errors
    """

    pass


class NDUNotRunningError(NorgateBridgeError):
    """NDU (Norgate Data Updater) is not running.

    Raised when the Norgate Data Updater application is not running or
    not accessible on the Windows host.

    Resolution:
    1. Start the Norgate Data Updater application on Windows
    2. Ensure you're logged in with valid credentials
    3. Verify NDU is authenticated with an active subscription
    """

    pass


class WindowsPythonNotFoundError(BridgeError):
    """Windows Python executable not found.

    Raised when python.exe cannot be found in the WSL PATH, preventing
    bridge communication between WSL and Windows Python environments.

    Resolution:
    1. Ensure Windows Python is installed (version 3.11+)
    2. Add Windows Python to WSL PATH (e.g., /mnt/c/Users/.../Python311/)
    3. Verify python.exe is accessible: `which python.exe`
    """

    pass


class DataError(Exception):
    """Base exception for data layer errors.

    Raised when errors occur during data operations such as fetching,
    caching, validation, or transformation.
    """

    pass


class CacheError(DataError):
    """Cache operation errors.

    Raised when errors occur during cache operations such as:
    - Schema validation failures
    - Invalid DataFrame structure (missing MultiIndex, empty DataFrame, etc.)
    - Parquet I/O errors
    - Cache path generation errors
    """

    pass
