# Norgate Data API Exploration Spike

**Story 1.0** - Research spike to validate Norgate Data API capabilities before architecture design.

**Date**: 2025-11-25
**Status**: Complete (Full Subscription)
**Decision**: GO - Proceed with architecture design

---

## Executive Summary

Successfully validated Norgate Data API connectivity and core functionality from WSL environment using a Windows Python bridge approach. All critical API functions work correctly with full historical data access.

**Key Findings**:
- Full price history available for all securities (back to 1990)
- 633 delisted stocks in S&P 500 Current & Past, 8,377 in Russell 3000 Current & Past
- Point-in-time index constituent timeseries works (survivorship-bias-free backtesting ✓)
- **No historical market cap** - must use index membership as proxy for size
- API performance: ~7ms/symbol (full Russell 3000 C&P fetch: ~1.4 min)

**Recommendation**: **GO** - Proceed with architecture design using Windows Python bridge pattern.

---

## Environment Configuration

### The Challenge
- Development environment: WSL (Linux)
- NDU (Norgate Data Updater): Runs on Windows host
- norgatedata package: Requires direct communication with NDU process

### The Solution: Windows Python Bridge
The `norgatedata` package cannot connect to NDU from WSL Python because NDU uses Windows-specific IPC. However, WSL can execute Windows executables directly.

**Working approach**:
```python
import subprocess

code = '''
import norgatedata
# ... fetch data ...
'''
result = subprocess.run(['python.exe', '-c', code], capture_output=True, text=True)
```

**Architecture implication**:
- Fetch data via Windows Python (`python.exe`)
- Save to Parquet files in shared filesystem (`/home/frank/momo/data/`)
- Analyze in WSL Python environment

---

## Phase 1: Connectivity & Subscription Audit

### 1.1 NDU Status
```
NDU Status: True
norgatedata version: 1.0.74
```

### 1.2 Available Databases (7 total)
| Database | Present | Notes |
|----------|---------|-------|
| US Equities | Yes | Active securities |
| **US Equities Delisted** | **Yes** | Critical for survivorship-bias-free backtesting |
| US Indices | Yes | Index price data |
| World Indices | Yes | |
| Continuous Futures | Yes | |
| Forex Spot | Yes | |
| Economic | Yes | |

### 1.3 Available Watchlists (64 total)

#### Russell Index Watchlists
| Watchlist | Available |
|-----------|-----------|
| Russell 1000 | Yes |
| Russell 1000 Current & Past | Yes |
| Russell 2000 | Yes |
| Russell 2000 Current & Past | Yes |
| Russell 3000 | Yes |
| Russell 3000 Current & Past | Yes |
| Russell Mid Cap | Yes |
| Russell Mid Cap Current & Past | Yes |
| Russell Top 200 | Yes |
| Russell Top 200 Current & Past | Yes |
| Russell Micro Cap | Yes |
| Russell Micro Cap Current & Past | Yes |

#### S&P Index Watchlists
| Watchlist | Available |
|-----------|-----------|
| S&P 500 | Yes |
| S&P 500 Current & Past | Yes |
| S&P 100 | Yes |
| S&P 100 Current & Past | Yes |
| S&P Composite 1500 | Yes |
| S&P Composite 1500 Current & Past | Yes |
| S&P MidCap 400 | Yes |
| S&P MidCap 400 Current & Past | Yes |
| S&P SmallCap 600 | Yes |
| S&P SmallCap 600 Current & Past | Yes |

### 1.4 Phase 1 Result: **PASS**

---

## Phase 2: Index Constituent Capabilities

### 2.1 Index Constituent Timeseries Test

Tested `norgatedata.index_constituent_timeseries()` for AAPL across multiple indices:

| Index | Success | Rows | Date Range |
|-------|---------|------|------------|
| Russell 1000 | Yes | 9,043 | 1990-01-02 to 2025-11-25 |
| Russell 3000 | Yes | 9,043 | 1990-01-02 to 2025-11-25 |
| S&P 500 | Yes | 9,043 | 1990-01-02 to 2025-11-25 |
| S&P 1500 | Yes | 9,043 | 1990-01-02 to 2025-11-25 |

**Data format**: DataFrame with `Index Constituent` column containing 1 (member) or 0 (not member) for each trading day.

### 2.2 Subscription Status

Full subscription provides:
- **35 years of data** (1990-01-02 to present)
- **Full delisted securities access**
- **Complete "Current & Past" watchlists**: Russell 3000 Current & Past shows 12,225 symbols

### 2.3 Delisted Stock Test

```
LEHMQ-201203 (Lehman Brothers) - delisted March 2012
Result: Full price history 1994-05-11 to 2012-03-05 (4,488 rows)
S&P 500 membership: 1998-01-12 to 2008-09-16
```

### 2.4 Phase 2 Result: **PASS**

---

## Phase 3: Universe Construction Feasibility

### 3.1 Symbol Counts by Watchlist

| Watchlist | Total | Current | Delisted |
|-----------|-------|---------|----------|
| Russell 1000 Current & Past | 3,535 | 1,420 | 2,115 |
| Russell 3000 Current & Past | 12,225 | 3,848 | 8,377 |
| S&P 500 Current & Past | 1,284 | 651 | 633 |
| S&P Composite 1500 Current & Past | 4,174 | 1,749 | 2,425 |

**Delisted symbol format**: `SYMBOL-YYYYMM` (e.g., `LEHMQ-201203` for Lehman Brothers, delisted March 2012)

### 3.2 Point-in-Time Universe Reconstruction

Successfully demonstrated reconstructing S&P 500 membership on 2008-09-15 (day before Lehman collapse):

| Symbol | Company | S&P 500 Status |
|--------|---------|----------------|
| AAPL | Apple Inc | IN |
| MSFT | Microsoft Corp | IN |
| LEHMQ-201203 | Lehman Brothers | IN |
| MER-200812 | Merrill Lynch | IN |
| GE | GE Aerospace | IN |

### 3.3 Phase 3 Result: **PASS**

---

## Phase 4: Price Data Validation

### 4.1 Adjustment Types

Tested AAPL on 2020-01-02 (before 4:1 split in August 2020):

| Adjustment | Close | Unadjusted Close | Notes |
|------------|-------|------------------|-------|
| NONE | 300.35 | 300.35 | Raw price |
| CAPITAL | 75.09 | 300.35 | Split-adjusted (300.35 / 4) |
| TOTALRETURN | 72.47 | 300.35 | Split + dividend adjusted |

### 4.2 Delisted Stock Price History

| Symbol | Company | Date Range | Rows | Final Price |
|--------|---------|------------|------|-------------|
| LEHMQ-201203 | Lehman Brothers | 1994-05-11 to 2012-03-05 | 4,488 | $0.03 |
| MER-200812 | Merrill Lynch | 1990-01-02 to 2008-12-31 | 4,791 | $11.64 |
| BSC-200805 | Bear Stearns | 1990-01-02 to 2008-05-30 | 4,642 | $9.33 |

### 4.3 DataFrame Structure

```python
# Columns: ['Open', 'High', 'Low', 'Close', 'Volume', 'Turnover', 'Unadjusted Close', 'Dividend']
# Index: DatetimeIndex named 'Date'
```

### 4.4 Phase 4 Result: **PASS**

---

## Phase 5: Fundamental Data Assessment

### 5.1 Available Fundamental Data

| Item | Available | Returns |
|------|-----------|---------|
| mktcap | Yes | `(value, date)` tuple - point-in-time only |
| sharesoutstanding | Yes | `(value, date)` tuple - point-in-time only |
| sharesfloat | Yes | `(value, date)` tuple - point-in-time only |
| avgvol20d/50d | No | `(None, None)` |
| eps, pe, revenue | No | `(None, None)` |

### 5.2 Historical Market Cap: NOT AVAILABLE

**Critical Finding**: Historical market cap is **not available** from Norgate. The `fundamental()` function returns only the most recent point-in-time value, not a timeseries.

### 5.3 Architecture Implications

Since historical market cap is unavailable, universe construction must use alternatives:

1. **Index membership as size proxy** (recommended):
   - Russell 1000 / S&P 500 = Large cap
   - Russell 2000 = Small cap
   - Russell 3000 = All cap

2. **ADV (Average Dollar Volume) for liquidity filtering**:
   - Calculate from: `Price × Volume` (available historically)
   - Filter low-liquidity stocks

3. **No market-cap-weighted calculations** possible without external data source

### 5.4 Phase 5 Result: **PASS** (with documented limitations)

---

## Phase 6: Performance Profiling

### 6.1 Sequential Price Retrieval

| Metric | Value |
|--------|-------|
| Symbols tested | 50 |
| Total time | 0.34 seconds |
| Per symbol | **6.7 ms** |

### 6.2 Full Universe Time Estimates

| Watchlist | Symbols | Estimated Time |
|-----------|---------|----------------|
| Russell 1000 | 1,000 | ~7 seconds |
| Russell 3000 | 3,000 | ~20 seconds |
| S&P 500 Current & Past | 1,284 | ~9 seconds |
| Russell 3000 Current & Past | 12,225 | **~82 seconds (1.4 min)** |

### 6.3 Index Constituent Timeseries

- Per symbol: ~5.4 ms
- Full Russell 3000 C&P: ~66 seconds

### 6.4 Phase 6 Result: **PASS** (excellent performance, no parallelization needed)

---

## Phase 7: Final Decision & Recommendations

### Go/No-Go Criteria Final Status

| Criterion | Status | Notes |
|-----------|--------|-------|
| Access to delisted securities database | **PASS** | 8,377 delisted in R3000 C&P |
| Historical index constituent timeseries | **PASS** | Full history back to 1990 |
| Index membership for delisted stocks | **PASS** | Verified with LEH, MER, BSC |
| Full price history for delisted stocks | **PASS** | Up to delisting date |
| Historical market cap | **FAIL** | Point-in-time only |

### Decision: **GO**

Proceed with architecture design. The lack of historical market cap is manageable using index membership as a size proxy.

### Architecture Recommendations

1. **Data Pipeline**:
   - Use Windows Python bridge to fetch from Norgate
   - Save to Parquet files in `/home/frank/momo/data/`
   - Analyze in WSL Python environment

2. **Universe Construction**:
   - Use "Current & Past" watchlists for survivorship-bias-free analysis
   - Filter by index membership for size categories
   - Calculate ADV from price × volume for liquidity screening

3. **Adjustment Setting**:
   - Use `TOTALRETURN` for strategy backtesting (accounts for dividends)
   - Use `CAPITAL` for technical analysis (split-adjusted only)

4. **Refresh Strategy**:
   - Initial full fetch: ~2 minutes for Russell 3000 C&P
   - Incremental daily updates: fetch only new data

---

## Code Reference: Windows Python Bridge Pattern

```python
import subprocess
import json

def fetch_from_norgate(code: str) -> dict:
    """Execute Python code via Windows Python and return JSON result."""
    wrapper = f'''
import json
import norgatedata
result = {code}
print(json.dumps(result))
'''
    result = subprocess.run(
        ['python.exe', '-c', wrapper],
        capture_output=True,
        text=True
    )
    # Parse last line (skip norgatedata INFO messages)
    return json.loads(result.stdout.strip().split('\n')[-1])

# Example: Get watchlists
data = fetch_from_norgate('norgatedata.watchlists()')
```

---

## Next Steps

1. **Begin Story 1.1**: Initialize project structure and development environment
2. **Implement data fetch module** using Windows Python bridge pattern
3. **Design data schema** for Parquet storage
