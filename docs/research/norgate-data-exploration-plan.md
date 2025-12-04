# Norgate Data Exploration Plan

## Objective
Systematically evaluate Norgate Data's Python API to determine if it can support building a **survivorship bias-free dataset** for the top 1000 US stocks by market capitalization.

---

## Prerequisites

### Environment Setup

**For Windows Python:**
```bash
pip install norgatedata pandas numpy
```

**For WSL development:**
- Ensure Windows Python has norgatedata installed
- Use Windows Python bridge pattern (execute code via `python.exe` subprocess)
- See [Norgate API Exploration findings](norgate-api-exploration.md) for bridge implementation

### Requirements
- Active Norgate Data subscription
- Norgate Data Updater (NDU) running on Windows
- Note: NDU is Windows-only; the Python package communicates with NDU
- For WSL: Windows Python (`python.exe`) must be in PATH

---

## Phase 1: Connectivity & Subscription Audit

### 1.1 Verify NDU is Running
```python
import norgatedata

# Check if NDU is running
status = norgatedata.status()
print(f"NDU Running: {status}")
```
**Go/No-Go:** Must return `True`

### 1.2 Inventory Available Databases
```python
databases = norgatedata.databases()
print("Available Databases:")
for db in databases:
    print(f"  - {db}")
```

**Expected (Platinum tier):**
- US Equities
- US Equities Delisted  ← Critical for survivorship bias
- US Indices
- World Indices

**Go/No-Go:** Must have "US Equities Delisted"

### 1.3 Inventory Available Watchlists
```python
watchlists = norgatedata.watchlists()
print("Available Watchlists:")
for wl in sorted(watchlists):
    if 'russell' in wl.lower() or 'r1000' in wl.lower() or 'r3000' in wl.lower():
        print(f"  * {wl}")  # Highlight Russell-related
    else:
        print(f"    {wl}")
```

**Looking for:**
- "Russell 1000 Current & Past" (ideal)
- "Russell 3000 Current & Past" (fallback)
- Any Russell-related watchlists

**Document findings:** Record exact watchlist names available.

---

## Phase 2: Index Constituent Capabilities

### 2.1 Test Index Names
```python
# Test which index names are recognized
test_indices = [
    'Russell 1000',
    'Russell 3000',
    'S&P 500',
    'S&P 1500',
    'Russell 2000',
]

test_symbol = 'AAPL'

for idx_name in test_indices:
    try:
        result = norgatedata.index_constituent_timeseries(
            test_symbol,
            idx_name,
            timeseriesformat='pandas-dataframe'
        )
        print(f"✓ '{idx_name}' - works, {len(result)} records")
    except Exception as e:
        print(f"✗ '{idx_name}' - failed: {e}")
```

**Document findings:** Record which index names work.

### 2.2 Examine Index Constituent Time Series Structure
```python
import pandas as pd

# Use an index that worked from 2.1
index_name = 'Russell 3000'  # or 'Russell 1000' if available
symbol = 'AAPL'

idx_ts = norgatedata.index_constituent_timeseries(
    symbol,
    index_name,
    timeseriesformat='pandas-dataframe'
)

print(f"Columns: {idx_ts.columns.tolist()}")
print(f"Date range: {idx_ts.index.min()} to {idx_ts.index.max()}")
print(f"Sample data:")
print(idx_ts.head(20))
print(f"\nValue counts:")
print(idx_ts.iloc[:, 0].value_counts())
```

**Key questions:**
- What does the constituent column contain? (1/0? True/False?)
- How far back does the data go?
- Are there any gaps?

### 2.3 Test with Delisted Stock
```python
# Find a delisted stock to test
delisted_symbols = norgatedata.database_symbols('US Equities Delisted')
print(f"Total delisted symbols: {len(delisted_symbols)}")

# Pick a well-known delisted stock (if available)
test_delisted = ['YHOO', 'LEH', 'ENRON', 'WB']  # Yahoo, Lehman, Enron, Wachovia

for symbol in test_delisted:
    if symbol in delisted_symbols:
        print(f"\nTesting delisted: {symbol}")
        try:
            idx_ts = norgatedata.index_constituent_timeseries(
                symbol,
                index_name,
                timeseriesformat='pandas-dataframe'
            )
            print(f"  Records: {len(idx_ts)}")
            print(f"  Date range: {idx_ts.index.min()} to {idx_ts.index.max()}")
        except Exception as e:
            print(f"  Error: {e}")
```

**Go/No-Go:** Must be able to retrieve index membership for delisted stocks.

---

## Phase 3: Universe Construction Test

### 3.1 Get All Symbols from Current & Past Watchlist
```python
# Use the Russell watchlist identified in Phase 1
watchlist_name = 'Russell 3000 Current & Past'  # Adjust based on findings

symbols = norgatedata.watchlist_symbols(watchlist_name)
print(f"Total symbols in '{watchlist_name}': {len(symbols)}")

# Categorize by status
current_equities = set(norgatedata.database_symbols('US Equities'))
delisted_equities = set(norgatedata.database_symbols('US Equities Delisted'))

current_count = len(set(symbols) & current_equities)
delisted_count = len(set(symbols) & delisted_equities)
unknown_count = len(symbols) - current_count - delisted_count

print(f"  Currently trading: {current_count}")
print(f"  Delisted: {delisted_count}")
print(f"  Unknown/Other: {unknown_count}")
```

### 3.2 Point-in-Time Universe Reconstruction
```python
import pandas as pd
from datetime import datetime

def get_index_members_at_date(symbols, index_name, target_date):
    """
    Reconstruct which stocks were in the index on a specific date.
    """
    members = []
    target_ts = pd.Timestamp(target_date)

    for symbol in symbols:
        try:
            idx_ts = norgatedata.index_constituent_timeseries(
                symbol,
                index_name,
                timeseriesformat='pandas-dataframe'
            )

            # Find the value at or before target_date
            valid_data = idx_ts[idx_ts.index <= target_ts]
            if len(valid_data) > 0:
                last_value = valid_data.iloc[-1, 0]
                if last_value == 1:  # Assuming 1 = in index
                    members.append(symbol)
        except:
            pass

    return members

# Test with a small sample first
sample_symbols = symbols[:50]
test_date = '2020-01-01'

print(f"Testing point-in-time reconstruction for {test_date}...")
members = get_index_members_at_date(sample_symbols, index_name, test_date)
print(f"Members found in sample: {len(members)}")
```

**Performance note:** This will be slow for 1000+ symbols. Phase 5 addresses optimization.

---

## Phase 4: Price Data Validation

### 4.1 Basic Price Retrieval
```python
symbol = 'AAPL'

price_df = norgatedata.price_timeseries(
    symbol,
    stock_price_adjustment_setting=norgatedata.StockPriceAdjustmentType.TOTALRETURN,
    padding_setting=norgatedata.PaddingType.NONE,
    timeseriesformat='pandas-dataframe'
)

print(f"Columns: {price_df.columns.tolist()}")
print(f"Date range: {price_df.index.min()} to {price_df.index.max()}")
print(f"Sample:")
print(price_df.tail())
```

### 4.2 Price Adjustment Options
```python
# Compare adjustment types
adjustments = [
    ('NONE', norgatedata.StockPriceAdjustmentType.NONE),
    ('CAPITAL', norgatedata.StockPriceAdjustmentType.CAPITAL),
    ('CAPITALSPECIAL', norgatedata.StockPriceAdjustmentType.CAPITALSPECIAL),
    ('TOTALRETURN', norgatedata.StockPriceAdjustmentType.TOTALRETURN),
]

symbol = 'AAPL'
test_date = '2020-01-02'

print(f"Close prices for {symbol} on {test_date} with different adjustments:")
for name, adj_type in adjustments:
    df = norgatedata.price_timeseries(
        symbol,
        stock_price_adjustment_setting=adj_type,
        timeseriesformat='pandas-dataframe'
    )
    if test_date in df.index.strftime('%Y-%m-%d').values:
        close = df.loc[test_date, 'Close']
        print(f"  {name}: {close:.2f}")
```

### 4.3 Delisted Stock Price History
```python
# Test price retrieval for a delisted stock
delisted_symbol = 'LEH'  # Lehman Brothers (adjust based on availability)

try:
    price_df = norgatedata.price_timeseries(
        delisted_symbol,
        stock_price_adjustment_setting=norgatedata.StockPriceAdjustmentType.TOTALRETURN,
        timeseriesformat='pandas-dataframe'
    )
    print(f"Delisted stock {delisted_symbol}:")
    print(f"  Date range: {price_df.index.min()} to {price_df.index.max()}")
    print(f"  Final prices:")
    print(price_df.tail())
except Exception as e:
    print(f"Error retrieving {delisted_symbol}: {e}")
```

**Go/No-Go:** Must retrieve full price history for delisted stocks up to delisting date.

---

## Phase 5: Market Cap & Fundamental Data

### 5.1 Current Fundamental Data
```python
symbol = 'AAPL'

fields = ['mktcap', 'sharesoutstanding', 'sharesfloat']

print(f"Fundamental data for {symbol}:")
for field in fields:
    try:
        value, date = norgatedata.fundamental(symbol, field)
        print(f"  {field}: {value:,.0f} (as of {date})")
    except Exception as e:
        print(f"  {field}: Error - {e}")
```

### 5.2 Historical Market Cap Investigation
```python
# Check if there's a time series version of market cap
# This is exploratory - the docs suggest fundamentals are point-in-time

# Option A: Check for market cap in price data columns
price_df = norgatedata.price_timeseries(
    'AAPL',
    timeseriesformat='pandas-dataframe'
)
print(f"Price dataframe columns: {price_df.columns.tolist()}")

# Option B: Can we compute from shares outstanding time series?
# (Explore if this function exists)
try:
    shares_ts = norgatedata.shares_outstanding_timeseries('AAPL')
    print("shares_outstanding_timeseries exists!")
except AttributeError:
    print("No shares_outstanding_timeseries function found")
except Exception as e:
    print(f"Other error: {e}")
```

### 5.3 Alternative: Use Index as Market Cap Proxy
If historical market cap isn't available, document this limitation:
- Russell 1000 = top 1000 by market cap (annual reconstitution)
- Russell 3000 = top 3000 by market cap
- These indices ARE the market cap ranking, pre-computed

---

## Phase 6: Performance & Scalability

### 6.1 Bulk Data Retrieval Timing
```python
import time

symbols = norgatedata.watchlist_symbols('Russell 3000 Current & Past')[:100]

# Time price retrieval for 100 symbols
start = time.time()
for symbol in symbols:
    try:
        df = norgatedata.price_timeseries(
            symbol,
            timeseriesformat='pandas-dataframe'
        )
    except:
        pass
elapsed = time.time() - start

print(f"Retrieved price data for {len(symbols)} symbols in {elapsed:.1f}s")
print(f"Average: {elapsed/len(symbols)*1000:.0f}ms per symbol")
print(f"Estimated time for 5000 symbols: {elapsed/len(symbols)*5000/60:.1f} minutes")
```

### 6.2 Parallel Retrieval Test
```python
from concurrent.futures import ThreadPoolExecutor
import time

def fetch_prices(symbol):
    try:
        return norgatedata.price_timeseries(symbol, timeseriesformat='pandas-dataframe')
    except:
        return None

symbols = norgatedata.watchlist_symbols('Russell 3000 Current & Past')[:100]

# Sequential
start = time.time()
results_seq = [fetch_prices(s) for s in symbols]
time_seq = time.time() - start

# Parallel (4 workers)
start = time.time()
with ThreadPoolExecutor(max_workers=4) as executor:
    results_par = list(executor.map(fetch_prices, symbols))
time_par = time.time() - start

print(f"Sequential: {time_seq:.1f}s")
print(f"Parallel (4 workers): {time_par:.1f}s")
print(f"Speedup: {time_seq/time_par:.1f}x")
```

---

## Phase 7: Data Quality Checks

### 7.1 Gap Detection
```python
import pandas as pd

def check_price_gaps(symbol, max_gap_days=5):
    """Check for unexpected gaps in price data."""
    df = norgatedata.price_timeseries(symbol, timeseriesformat='pandas-dataframe')

    # Calculate day differences
    df['day_diff'] = df.index.to_series().diff().dt.days

    # Find gaps > max_gap_days (accounting for weekends/holidays)
    gaps = df[df['day_diff'] > max_gap_days]

    return gaps[['day_diff']]

# Test on a few symbols
test_symbols = ['AAPL', 'MSFT', 'GE']
for symbol in test_symbols:
    gaps = check_price_gaps(symbol, max_gap_days=7)
    if len(gaps) > 0:
        print(f"{symbol}: {len(gaps)} gaps > 7 days")
        print(gaps.head())
    else:
        print(f"{symbol}: No significant gaps")
```

### 7.2 Index Membership Consistency
```python
def check_index_membership_sanity(index_name, sample_date='2020-06-30'):
    """
    Count how many stocks were in the index on a given date.
    Russell 1000 should have ~1000, Russell 3000 should have ~3000.
    """
    watchlist = f'{index_name} Current & Past'
    symbols = norgatedata.watchlist_symbols(watchlist)

    target_ts = pd.Timestamp(sample_date)
    member_count = 0

    for symbol in symbols[:500]:  # Sample for speed
        try:
            idx_ts = norgatedata.index_constituent_timeseries(
                symbol, index_name, timeseriesformat='pandas-dataframe'
            )
            valid = idx_ts[idx_ts.index <= target_ts]
            if len(valid) > 0 and valid.iloc[-1, 0] == 1:
                member_count += 1
        except:
            pass

    print(f"Members in sample on {sample_date}: {member_count}/500 sampled")
    print(f"Extrapolated total: ~{member_count * len(symbols) // 500}")
```

---

## Decision Matrix

After completing all phases, fill in this matrix:

| Requirement | Status | Notes |
|-------------|--------|-------|
| NDU connectivity | ⬜ | |
| US Equities Delisted database | ⬜ | |
| Russell 1000 index available | ⬜ | |
| Russell 3000 index available | ⬜ | |
| Historical index constituent data | ⬜ | |
| Delisted stock price history | ⬜ | |
| Delisted stock index membership | ⬜ | |
| Historical market cap (optional) | ⬜ | |
| Acceptable performance | ⬜ | |
| Data goes back to [year] | ⬜ | |

---

## Go/No-Go Criteria

### Must Have (Blockers)
1. ✅ Access to delisted securities database
2. ✅ Historical index constituent time series works
3. ✅ Can retrieve index membership for delisted stocks
4. ✅ Full price history available for delisted stocks

### Nice to Have
1. Russell 1000 specifically (vs Russell 3000)
2. Historical market cap time series
3. Sub-second per-symbol retrieval

---

## Next Steps Based on Findings

### If Russell 1000 is Available:
→ Proceed with index-based universe construction

### If Only Russell 3000 is Available:
→ Options:
  1. Use Russell 3000 and filter to ~top 1000 by some metric
  2. Use S&P 500 + S&P 400 (MidCap) ≈ 900 stocks
  3. Calculate market cap ranking ourselves (if historical mktcap available)

### If Historical Market Cap is NOT Available:
→ Accept that Russell index membership IS the market cap ranking
→ Use reconstitution dates (typically end of June) as rebalance points

---

## Appendix: Subscription Tier Requirements

Based on documentation:
- **Historical index constituents**: Platinum or Diamond
- **Major exchange listing**: Platinum or Diamond
- **Delisted equities**: Verify tier requirement

Contact Norgate Data support if subscription tier is unclear.
