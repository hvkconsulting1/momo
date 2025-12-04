# Windows Python Bridge Architecture

## Overview

The Windows Python Bridge is a subprocess-based communication layer that enables WSL Python to access the Norgate Data Updater (NDU) API, which runs exclusively on Windows.

### Why This Bridge Exists

**The Challenge:**
- Development environment: WSL (Linux) for modern tooling and workflow
- NDU (Norgate Data Updater): Runs on Windows host using Windows-specific IPC
- norgatedata package: Requires direct communication with NDU process (Windows COM/pipes)

**The Solution:**
WSL can execute Windows executables directly (e.g., `python.exe`). The bridge executes Python code via Windows Python using subprocess, with results transferred back via JSON serialization.

**Architecture Summary:**
```
WSL Python → subprocess → Windows Python (python.exe) → norgatedata → NDU
     ↑                                                                    ↓
     └────────────────── JSON Response ←──────────────────────────────────┘
```

---

## Architecture

### Communication Pattern

The bridge uses a subprocess-based pattern with JSON serialization for data transfer:

1. **WSL Python** constructs Python code string
2. **Subprocess call** executes `python.exe -c <code>` from WSL
3. **Windows Python** imports norgatedata and executes code
4. **norgatedata** communicates with NDU via Windows IPC
5. **NDU** returns data to norgatedata
6. **JSON serialization** converts result to string
7. **Subprocess stdout** transfers JSON back to WSL
8. **WSL Python** parses JSON and returns result

### Data Flow Diagram

```
┌─────────────────┐
│   WSL Python    │
│  (momo app)     │
└────────┬────────┘
         │ execute_norgate_code("norgatedata.price_timeseries(...)")
         ↓
┌────────────────────────────────────────────────────────────┐
│                    Bridge Layer                            │
│              (src/momo/data/bridge.py)                     │
│                                                            │
│  1. Wrap code with JSON serialization                     │
│  2. Execute: subprocess.run(['python.exe', '-c', code])   │
│  3. Parse JSON from stdout                                │
└────────┬───────────────────────────────────────────────────┘
         │ subprocess call
         ↓
┌─────────────────┐
│ Windows Python  │ import norgatedata
│  (python.exe)   │ result = norgatedata.price_timeseries(...)
│                 │ print(json.dumps(result))
└────────┬────────┘
         │ norgatedata API call
         ↓
┌─────────────────┐
│      NDU        │ ← Windows IPC (COM/pipes)
│  (Windows App)  │
└─────────────────┘
```

### JSON Serialization

Results are serialized to JSON for transfer across the subprocess boundary:

```python
# Windows Python (subprocess):
import json
import norgatedata

result = norgatedata.version()  # "1.0.74"
print(json.dumps(result))       # Output: "1.0.74"

# WSL Python (bridge):
output = subprocess.stdout      # "1.0.74"
parsed = json.loads(output)     # "1.0.74" (string)
return parsed
```

For pandas DataFrames, norgatedata returns native DataFrame objects which are serialized to lists of records:

```python
# Windows Python:
df = norgatedata.price_timeseries("AAPL", ...)
result = df.to_dict('records')  # Convert to JSON-serializable format
print(json.dumps(result, default=str))

# WSL Python:
records = json.loads(output)
df = pd.DataFrame(records)      # Reconstruct DataFrame
```

---

## Prerequisites

### Windows Environment

| Requirement | Details |
|-------------|---------|
| **Operating System** | Windows 10/11 with WSL 2 |
| **NDU Application** | Norgate Data Updater running and authenticated |
| **Subscription** | Active Norgate Data subscription (Russell 3000 C&P recommended) |
| **Windows Python** | Python 3.11+ installed on Windows host |
| **PATH Configuration** | Windows Python accessible from WSL as `python.exe` |

### Python Packages

**Windows Python** (required for NDU communication):
```bash
# Install in Windows Python (from Windows terminal or PowerShell)
pip install norgatedata==1.0.74
```

**WSL Python** (required for bridge operation):
```bash
# Already included in project dependencies (pyproject.toml)
uv sync  # Installs: structlog, tenacity, pandas
```

### PATH Configuration

Windows Python must be accessible from WSL. Verify with:

```bash
# From WSL terminal
python.exe --version
# Expected: Python 3.11.x or higher
```

If `python.exe` is not found, add Windows Python to WSL PATH:

```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$PATH:/mnt/c/Users/<YourUsername>/AppData/Local/Programs/Python/Python311"

# Reload shell
source ~/.bashrc
```

### NDU Setup

1. **Install NDU**: Download from https://norgatedata.com/
2. **Authenticate**: Launch NDU and log in with subscription credentials
3. **Verify**: NDU system tray icon should show "Connected" status
4. **Test**: From WSL, run:
   ```bash
   python.exe -c "import norgatedata; print(norgatedata.databases())"
   ```
   Should print list of available databases (e.g., `['US Equities', 'US Equities Delisted', ...]`)

---

## Usage Examples

### Basic Bridge Usage

#### Example 1: Execute Simple Python Code

```python
from momo.data.bridge import execute_norgate_code

# Simple arithmetic
result = execute_norgate_code("2 + 2")
print(result)  # Output: 4

# Dictionary result
result = execute_norgate_code("{'version': '1.0.74', 'status': 'ok'}")
print(result)  # Output: {'version': '1.0.74', 'status': 'ok'}
```

#### Example 2: Get Norgate Data Version

```python
from momo.data.bridge import execute_norgate_code

version = execute_norgate_code("norgatedata.version()")
print(f"norgatedata version: {version}")
# Output: norgatedata version: 1.0.74
```

#### Example 3: List Available Databases

```python
from momo.data.bridge import execute_norgate_code

databases = execute_norgate_code("norgatedata.databases()")
print(f"Available databases: {databases}")
# Output: Available databases: ['US Equities', 'US Equities Delisted', ...]
```

### Fetching Price Data

#### Example 1: Fetch Recent Price Data (Simple)

```python
from datetime import date
from momo.data.bridge import fetch_price_data

# Fetch AAPL data for 2023
prices_df = fetch_price_data(
    symbol="AAPL",
    start_date=date(2023, 1, 1),
    end_date=date(2023, 12, 31)
)

print(prices_df.head())
#             symbol    open    high     low   close     volume
# date
# 2023-01-03   AAPL  125.07  125.27  124.17  125.07  112117471
# 2023-01-04   AAPL  126.89  128.66  125.08  126.36   89113631
# 2023-01-05   AAPL  127.13  127.77  124.76  125.02   80962686
```

#### Example 2: Fetch All Available History

```python
from momo.data.bridge import fetch_price_data

# Fetch all available history (no date parameters)
prices_df = fetch_price_data(symbol="MSFT")

print(f"Date range: {prices_df.index.min()} to {prices_df.index.max()}")
print(f"Total rows: {len(prices_df)}")
# Output: Date range: 1986-03-13 to 2025-12-04
#         Total rows: 10,045
```

#### Example 3: Fetch with CAPITAL Adjustment (Splits Only)

```python
from momo.data.bridge import fetch_price_data

# Use CAPITAL adjustment (splits only, no dividends)
prices_df = fetch_price_data(
    symbol="AAPL",
    start_date=date(2023, 1, 1),
    end_date=date(2023, 12, 31),
    adjustment="CAPITAL"  # Default is "TOTALRETURN"
)

print(prices_df.head())
# Note: Prices differ from TOTALRETURN adjustment
```

#### Example 4: Custom Timeout for Large Requests

```python
from momo.data.bridge import fetch_price_data

# Increase timeout for large date ranges or slow NDU
prices_df = fetch_price_data(
    symbol="AAPL",
    timeout=60  # 60 seconds (default is 30)
)
```

### Checking NDU Status

#### Example 1: Proactive Status Check

```python
from momo.data.bridge import check_ndu_status

if check_ndu_status():
    print("NDU is running and accessible")
    # Proceed with data operations
else:
    print("NDU is not running - please start NDU")
    # Exit or wait for user action
```

#### Example 2: Graceful Degradation

```python
from momo.data.bridge import check_ndu_status, fetch_price_data

def get_price_data_safe(symbol: str):
    """Fetch price data with graceful degradation."""
    if not check_ndu_status():
        # Fall back to cached data or return None
        print(f"⚠️  NDU not available - returning cached data for {symbol}")
        return load_from_cache(symbol)

    # NDU available - fetch fresh data
    return fetch_price_data(symbol)
```

#### Example 3: Status Check with Custom Timeout

```python
from momo.data.bridge import check_ndu_status

# Quick status check (5 seconds)
is_available = check_ndu_status(timeout=5)
```

---

## Error Handling

### Exception Hierarchy

```
Exception
└── BridgeError (base exception for all bridge errors)
    ├── NorgateBridgeError (Norgate Data API errors)
    │   └── NDUNotRunningError (NDU is not running)
    └── WindowsPythonNotFoundError (python.exe not in PATH)
```

All custom exceptions are defined in `src/momo/utils/exceptions.py`.

### Common Error Scenarios

#### 1. NDU Not Running

**Symptom:**
```python
from momo.data.bridge import fetch_price_data

try:
    prices_df = fetch_price_data("AAPL")
except NDUNotRunningError as e:
    print(e)
    # Output: Norgate Data Updater is not running. Please start NDU on Windows
    #         and ensure you're logged in.
```

**Resolution:**
1. Launch NDU from Windows Start menu
2. Verify "Connected" status in NDU system tray icon
3. If not connected, log in with subscription credentials
4. Retry operation

**Prevention:**
```python
from momo.data.bridge import check_ndu_status

if not check_ndu_status():
    print("⚠️  Please start NDU before running data operations")
    exit(1)
```

---

#### 2. Windows Python Not Found

**Symptom:**
```python
from momo.data.bridge import execute_norgate_code

try:
    result = execute_norgate_code("2 + 2")
except WindowsPythonNotFoundError as e:
    print(e)
    # Output: Windows Python (python.exe) not found. Ensure Windows Python is
    #         installed and in WSL PATH.
```

**Resolution:**
1. Verify Windows Python installed:
   ```powershell
   # From Windows PowerShell
   python --version
   ```
2. Add Windows Python to WSL PATH (see [Prerequisites](#path-configuration))
3. Verify from WSL:
   ```bash
   python.exe --version  # Should show Windows Python version
   ```

---

#### 3. norgatedata Package Not Installed

**Symptom:**
```python
from momo.data.bridge import execute_norgate_code

try:
    version = execute_norgate_code("norgatedata.version()")
except NorgateBridgeError as e:
    print(e)
    # Output: norgatedata package not found in Windows Python.
    #         Install via: pip install norgatedata==1.0.74
```

**Resolution:**
```powershell
# From Windows PowerShell or Command Prompt
pip install norgatedata==1.0.74
```

**Verification:**
```bash
# From WSL
python.exe -c "import norgatedata; print(norgatedata.version())"
# Expected: 1.0.74
```

---

#### 4. Timeout Error

**Symptom:**
```python
from momo.data.bridge import fetch_price_data

try:
    prices_df = fetch_price_data("AAPL", timeout=5)  # Very short timeout
except NorgateBridgeError as e:
    print(e)
    # Output: Bridge operation timed out after 5 seconds. Check if NDU is responding.
```

**Resolution:**
1. Check NDU responsiveness in Windows (launch NDU UI)
2. Verify no other processes heavily using NDU
3. Increase timeout parameter:
   ```python
   prices_df = fetch_price_data("AAPL", timeout=60)  # Increase to 60 seconds
   ```
4. For batch operations, process symbols sequentially to avoid NDU overload

---

#### 5. JSON Parse Error

**Symptom:**
```python
# Rare - usually indicates subprocess communication issue
try:
    result = execute_norgate_code("malformed code")
except NorgateBridgeError as e:
    print(e)
    # Output: Failed to parse bridge output: ...
```

**Resolution:**
- This typically indicates a code generation bug
- Check that code parameter is valid Python
- Review subprocess stderr in logs for details
- Report issue if code appears valid

---

## Troubleshooting

### Windows Python Not Found

**Problem:** `WindowsPythonNotFoundError: Windows Python (python.exe) not found`

**Diagnostic Steps:**
```bash
# 1. Check if Windows Python is installed
ls /mnt/c/Users/*/AppData/Local/Programs/Python/

# 2. Find python.exe location
find /mnt/c/Users/ -name "python.exe" 2>/dev/null | grep -i "Python3"

# 3. Test direct execution
/mnt/c/Users/YourUsername/AppData/Local/Programs/Python/Python311/python.exe --version
```

**Solutions:**

**Option 1: Add to WSL PATH** (recommended)
```bash
# Add to ~/.bashrc
echo 'export PATH="$PATH:/mnt/c/Users/YourUsername/AppData/Local/Programs/Python/Python311"' >> ~/.bashrc
source ~/.bashrc

# Verify
python.exe --version
```

**Option 2: Create symlink**
```bash
sudo ln -s /mnt/c/Users/YourUsername/AppData/Local/Programs/Python/Python311/python.exe /usr/local/bin/python.exe
```

**Option 3: Use Windows Python installer** (if not installed)
1. Download from https://www.python.org/downloads/windows/
2. Run installer, select "Add Python to PATH"
3. Restart WSL terminal

---

### NDU Not Running

**Problem:** `NDUNotRunningError: Norgate Data Updater is not running`

**Diagnostic Steps:**
```bash
# 1. Check if NDU process is running (from WSL)
powershell.exe "Get-Process | Where-Object {$_.ProcessName -like '*Norgate*'}"

# 2. Verify NDU can be accessed
python.exe -c "import norgatedata; print(norgatedata.databases())"
```

**Solutions:**

**Step 1: Launch NDU**
- Press Windows key, search "Norgate Data Updater"
- Launch application
- Check system tray for NDU icon

**Step 2: Verify Authentication**
- Right-click NDU system tray icon
- Select "Settings" → "Subscription"
- Ensure valid credentials and "Connected" status

**Step 3: Restart NDU if Hung**
```powershell
# From Windows PowerShell (as Administrator)
Stop-Process -Name "NorgateDataUpdater" -Force
# Then relaunch NDU from Start menu
```

**Step 4: Verify Subscription Active**
- Log into https://norgatedata.com/members/
- Check subscription status and expiry date
- Renew if expired

---

### norgatedata Import Error

**Problem:** `norgatedata package not found in Windows Python`

**Diagnostic Steps:**
```bash
# 1. Check if norgatedata installed in Windows Python
python.exe -m pip list | grep norgatedata

# 2. Check Windows Python pip version
python.exe -m pip --version

# 3. Verify Windows Python can import packages
python.exe -c "import sys; print(sys.path)"
```

**Solutions:**

**Step 1: Install norgatedata in Windows Python**
```powershell
# From Windows PowerShell or Command Prompt
python -m pip install norgatedata==1.0.74
```

**Step 2: Verify installation**
```bash
# From WSL
python.exe -c "import norgatedata; print(norgatedata.version())"
# Expected output: 1.0.74
```

**Step 3: If multiple Python versions installed**
```powershell
# List all Python installations
where python

# Install norgatedata for specific version
C:\Users\YourUsername\AppData\Local\Programs\Python\Python311\python.exe -m pip install norgatedata==1.0.74
```

**Step 4: Verify correct Python used by WSL**
```bash
# From WSL
which python.exe  # Should point to correct Windows Python
python.exe --version  # Should match expected version
```

---

### Timeout Errors

**Problem:** `Bridge operation timed out after 30 seconds`

**Diagnostic Steps:**
```bash
# 1. Test simple operation (should be fast)
python.exe -c "import time; start = time.time(); import norgatedata; print(time.time() - start)"
# Expected: < 1 second

# 2. Test NDU responsiveness
python.exe -c "import time; import norgatedata; start = time.time(); norgatedata.databases(); print(f'Time: {time.time()-start:.2f}s')"
# Expected: < 2 seconds

# 3. Check Windows resource usage
powershell.exe "Get-Process | Where-Object {$_.CPU -gt 50} | Select-Object ProcessName, CPU"
```

**Solutions:**

**Short-term: Increase Timeout**
```python
from momo.data.bridge import fetch_price_data

# Increase timeout for slow operations
prices_df = fetch_price_data("AAPL", timeout=60)  # 60 seconds
```

**Long-term: Optimize NDU Performance**

1. **Restart NDU** (clears caches, resolves temporary hangs)
   ```powershell
   Stop-Process -Name "NorgateDataUpdater" -Force
   # Relaunch from Start menu
   ```

2. **Update NDU Database** (old data can slow queries)
   - Right-click NDU system tray icon
   - Select "Update Database"
   - Wait for update to complete

3. **Check Windows Performance**
   - Close unnecessary applications
   - Verify adequate RAM available (Task Manager)
   - Check disk usage (NDU database on SSD recommended)

4. **Reduce Concurrent Requests** (avoid overloading NDU)
   ```python
   # Bad: Too many concurrent requests
   with ThreadPoolExecutor(max_workers=20) as executor:
       results = executor.map(fetch_price_data, symbols)

   # Good: Limit concurrency
   with ThreadPoolExecutor(max_workers=5) as executor:  # Max 5 concurrent
       results = executor.map(fetch_price_data, symbols)
   ```

---

### norgatedata INFO Messages

**Problem:** `Failed to parse bridge output` (with INFO messages in logs)

**Context:**
The norgatedata package prints INFO messages to stdout, which can interfere with JSON parsing:
```
INFO: Norgate Data Updater connection established
{"symbol": "AAPL", "rows": 252}
```

**Solution:**
This is already handled by the bridge implementation (parses only the last line of stdout). If you see this error:

1. **Check for custom subprocess code** (not using `execute_norgate_code()`)
   - Use `execute_norgate_code()` which handles INFO messages correctly

2. **Verify JSON is on last line**
   ```python
   # In custom code, parse only last line:
   output_lines = result.stdout.strip().split('\n')
   json_line = output_lines[-1]
   parsed = json.loads(json_line)
   ```

3. **Report if occurring in bridge functions** (should not happen)

---

## Performance Characteristics

### Latency Benchmarks

Based on Story 1.0 exploration findings:

| Operation | Expected Latency | Notes |
|-----------|------------------|-------|
| Simple code execution | ~50-100ms | Subprocess overhead |
| NDU status check | ~100-200ms | Includes norgatedata import |
| Single symbol price data | ~7ms | Per symbol, from NDU cache |
| Full Russell 3000 C&P fetch | ~82 seconds | 12,225 symbols × ~7ms |
| Index constituent timeseries | ~10-20ms | Per symbol, point-in-time data |

**Key Insights:**
- **Subprocess overhead**: ~50ms per call (Python interpreter startup)
- **NDU lookup**: ~7ms per symbol (highly optimized local IPC)
- **Batch operations**: Process multiple symbols in single subprocess call when possible

### Timeout Defaults

| Function | Default Timeout | Rationale |
|----------|-----------------|-----------|
| `execute_norgate_code()` | 30 seconds | Handles slow NDU responses |
| `fetch_price_data()` | 30 seconds | Large date ranges may be slow |
| `check_ndu_status()` | 10 seconds | Status check should be fast |

**Recommendations:**
- Use default timeouts for interactive operations
- Increase timeouts for batch processing (60+ seconds)
- Monitor logs for timeout warnings

### Retry Behavior

The bridge uses **tenacity** for automatic retry on transient errors:

| Setting | Value | Rationale |
|---------|-------|-----------|
| Max attempts | 3 | Handles temporary NDU unavailability |
| Wait between retries | 1 second | Fixed delay (not exponential) |
| Retry conditions | `ConnectionError`, `OSError` | Network/subprocess issues only |
| No retry | `NDUNotRunningError` | User action required (start NDU) |

**Example:**
```python
# Retry behavior is automatic (via @retry decorator)
result = execute_norgate_code("norgatedata.version()")
# If fails with OSError:
#   - Attempt 1: Immediate
#   - Attempt 2: After 1 second
#   - Attempt 3: After 2 seconds total
#   - Then raise exception
```

### Concurrent Request Handling

The bridge supports concurrent requests (multiple threads/processes calling bridge functions):

| Scenario | Behavior | Notes |
|----------|----------|-------|
| Multiple threads | ✅ Safe | Each thread spawns independent subprocess |
| Multiple processes | ✅ Safe | Each process has independent subprocess pool |
| Subprocess leaks | ✅ Prevented | subprocess.run() waits for completion |
| NDU overload | ⚠️ Possible | Limit concurrent requests to ~5-10 |

**Best Practices:**
```python
from concurrent.futures import ThreadPoolExecutor
from momo.data.bridge import fetch_price_data

symbols = ["AAPL", "MSFT", "GOOGL", ...]

# Good: Limit concurrency to avoid NDU overload
with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(fetch_price_data, symbols))

# Bad: Too many concurrent requests may timeout
with ThreadPoolExecutor(max_workers=50) as executor:  # Don't do this
    results = list(executor.map(fetch_price_data, symbols))
```

### Performance Optimization Tips

1. **Batch data fetching** (future enhancement)
   - Fetch multiple symbols in single subprocess call
   - Reduces subprocess overhead from ~50ms to ~7ms per symbol

2. **Cache aggressively** (future stories will implement Parquet caching)
   - Historical data rarely changes (except recent dates)
   - Cache to `/home/frank/momo/data/` for fast access

3. **Use check_ndu_status() once at startup**
   - Don't check status before every data fetch
   - Check once, then rely on exception handling

4. **Profile slow operations**
   ```python
   import time
   import structlog

   logger = structlog.get_logger()

   start = time.time()
   prices_df = fetch_price_data("AAPL")
   elapsed = time.time() - start

   logger.info("fetch_performance", symbol="AAPL", elapsed_ms=elapsed*1000)
   ```

---

## Testing

### Unit Tests (No Windows/NDU Required)

Unit tests mock subprocess calls and validate bridge logic without requiring Windows Python or NDU.

**Run all unit tests:**
```bash
pytest tests/stories/1.2/unit/ -v
```

**Run specific unit test:**
```bash
pytest tests/stories/1.2/unit/test_1_2_unit_001.py -v
```

**Run with coverage:**
```bash
pytest tests/stories/1.2/unit/ --cov=src/momo/data.bridge --cov-report=term-missing
```

**Unit test coverage:**
- Subprocess call construction (1.2-UNIT-002)
- JSON parsing from stdout (1.2-UNIT-003)
- INFO message handling (1.2-UNIT-004)
- Error handling (1.2-UNIT-005, 1.2-UNIT-006, 1.2-UNIT-010)
- Logging validation (1.2-UNIT-007)
- Helper function logic (1.2-UNIT-008, 1.2-UNIT-009, 1.2-UNIT-011)

### Integration Tests (Require Windows + NDU)

Integration tests validate actual bridge communication with Windows Python and NDU. These tests will be skipped if NDU is not available.

**Run all integration tests:**
```bash
pytest tests/stories/1.2/integration/ -v
```

**Run specific integration test:**
```bash
pytest tests/stories/1.2/integration/test_1_2_int_001.py -v
```

**Integration test coverage:**
- norgatedata package import (1.2-INT-001)
- Version validation (1.2-INT-002)
- Basic bridge communication (1.2-INT-003)
- Concurrent requests (1.2-INT-004)
- Price data retrieval (1.2-INT-005)
- Schema validation (1.2-INT-006)
- Adjustment types (1.2-INT-007)
- Error message quality (1.2-INT-008)

### Environment Setup for Integration Testing

**Prerequisites:**
1. Windows environment with WSL
2. NDU running and authenticated
3. Windows Python 3.11+ with norgatedata 1.0.74

**Verification:**
```bash
# Check Windows Python accessible
python.exe --version

# Check norgatedata installed
python.exe -c "import norgatedata; print(norgatedata.version())"

# Check NDU running
python.exe -c "import norgatedata; print(norgatedata.databases())"
```

**Skip integration tests if NDU not available:**
Integration tests use `check_ndu_status()` to automatically skip when NDU is unavailable:

```python
import pytest
from momo.data.bridge import check_ndu_status

@pytest.mark.skipif(not check_ndu_status(), reason="NDU not available")
def test_1_2_int_005():
    """Test price data retrieval via bridge."""
    # Test implementation
```

---

## Limitations

### Known Issues and Workarounds

#### 1. norgatedata INFO Messages

**Issue:**
The norgatedata package prints INFO messages to stdout, which can interfere with JSON parsing:
```
INFO: Norgate Data Updater connection established
{"result": "data"}
```

**Workaround:**
Bridge implementation parses only the **last line** of stdout, ignoring INFO messages. This is handled automatically by `execute_norgate_code()`.

**Status:** ✅ Mitigated (no user action required)

---

#### 2. Windows-Only Constraint

**Issue:**
The bridge requires Windows Python with NDU, which is Windows-only. Cannot run from pure Linux environment.

**Workaround:**
- Use WSL on Windows host (recommended development setup)
- Use Windows VM if running Linux host (performance overhead)
- Cache data to Parquet files for Linux-only environments (future story)

**Status:** ⚠️ Architectural constraint (no workaround for pure Linux)

---

#### 3. Subprocess Overhead

**Issue:**
Each bridge call spawns a subprocess, adding ~50ms overhead per call. This is significant compared to ~7ms NDU lookup time.

**Impact:**
- Single symbol fetch: ~57ms total (50ms subprocess + 7ms NDU)
- 1000 symbols fetched individually: ~57 seconds

**Workaround:**
- Batch multiple symbols in single subprocess call (future enhancement)
- Cache aggressively to minimize repeated fetches (future story)

**Status:** ⚠️ Performance limitation (future optimization planned)

---

#### 4. No Historical Market Cap

**Issue:**
Norgate Data API does not provide historical market cap data. This is required for size-based portfolio construction.

**Workaround:**
- Use index membership as proxy for size (Russell 1000 = large cap, Russell 2000 = small cap)
- Use point-in-time index constituent data (`norgatedata.index_constituent_timeseries()`)

**Status:** ⚠️ Data limitation (workaround available via index membership)

---

#### 5. Windows Python Version Mismatch

**Issue:**
WSL Python and Windows Python may have different versions, causing compatibility issues (e.g., type hints, f-strings).

**Workaround:**
- Use compatible Python syntax in code passed to Windows Python (avoid Python 3.13+ features)
- Ensure Windows Python is 3.11+ (matches project requirement)

**Status:** ⚠️ Development consideration (ensure compatible syntax)

---

### Future Enhancements

**Planned improvements** (tracked in future stories):

1. **Batch symbol fetching** (Story 1.x)
   - Fetch multiple symbols in single subprocess call
   - Reduce overhead from 50ms/symbol to 7ms/symbol

2. **Parquet caching** (Story 1.x)
   - Cache fetched data to Parquet files in `/home/frank/momo/data/`
   - Eliminate repeated bridge calls for historical data

3. **Connection pooling** (Story 1.x)
   - Reuse subprocess/NDU connections
   - Reduce per-call overhead

4. **Async support** (Story 1.x)
   - Async versions of bridge functions (`async def fetch_price_data_async()`)
   - Better integration with async workflows

---

## Related Documentation

- **Implementation**: [`src/momo/data/bridge.py`](../../src/momo/data/bridge.py) - Bridge source code
- **Story**: [`docs/stories/1.2.story.md`](../stories/1.2.story.md) - Story 1.2 details
- **Research**: [`docs/research/norgate-api-exploration.md`](../research/norgate-api-exploration.md) - Story 1.0 spike findings
- **External APIs**: [`docs/architecture/external-apis.md`](external-apis.md) - Norgate Data API reference
- **Data Models**: [`docs/architecture/data-models.md`](data-models.md) - Price data schema
- **Exceptions**: [`src/momo/utils/exceptions.py`](../../src/momo/utils/exceptions.py) - Bridge exception classes

---

**Document Version:** 1.0
**Last Updated:** 2025-12-04
**Story:** 1.2 - Integrate Norgate Data API via Windows Python Bridge
