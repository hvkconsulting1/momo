# ADR-002: Windows Python Bridge for Norgate Data

## Status

Accepted

## Context

Norgate Data Updater (NDU) provides market data through a Python package (`norgatedata`) that only works on Windows. It uses local IPC (COM/pipe) to communicate with the NDU desktop application.

Our development environment is WSL2 (Linux), which cannot directly access Windows IPC mechanisms. We need a way to fetch data from Norgate while developing in WSL.

Options considered:
1. **Develop on Windows** - Abandons WSL tooling and Linux environment
2. **Run NDU in Wine** - Complex, unsupported, likely to fail
3. **Windows Python subprocess** - Call `python.exe` from WSL to execute Norgate code
4. **Shared database** - Have Windows process populate a database WSL reads

## Decision

We will use a **Windows Python bridge pattern** where WSL executes Python code via Windows `python.exe` subprocess.

Implementation:
```python
result = subprocess.run(
    ["python.exe", "-c", norgate_code],
    capture_output=True,
    text=True,
    timeout=30,
)
```

The bridge:
- Executes Python code that imports `norgatedata` and returns JSON
- Is isolated to a single module (`src/momo/data/bridge.py`)
- Includes retry logic with exponential backoff (3 attempts)
- Returns structured data that the rest of the data layer consumes

## Consequences

**Positive:**
- Enables WSL development while accessing Norgate data
- Bridge is isolated - rest of codebase unaware of Windows constraint
- JSON serialization provides clean interface boundary
- Can be replaced if Norgate adds Linux support

**Negative:**
- Performance overhead (~7ms per symbol vs direct API)
- Requires Windows Python in PATH
- Additional failure mode (subprocess, JSON parsing)
- Cannot run data layer tests in CI (no Windows/NDU)

**Mitigations:**
- Parquet caching eliminates bridge calls after initial fetch
- Cache fallback enables offline operation when NDU unavailable
- Integration tests marked and skipped in CI
