# Norgate Data Index Constituents API Exploration

**Date:** 2025-12-05
**Story:** 1.4 - Point-in-Time Index Constituent Retrieval
**Purpose:** Document findings from systematic exploration of `norgatedata.index_constituent_timeseries()` API

---

## Overview

This document captures our investigation into how to retrieve point-in-time index constituents using the Norgate Data API through our Windows Python bridge. The goal is to determine if a stock was a member of an index (e.g., Russell 3000) at a specific date to avoid survivorship bias in backtests.

---

## API Function Signature

```python
norgatedata.index_constituent_timeseries(
    symbol: str,
    indexname: str,
    timeseriesformat: str = "numpy-recarray",
    start_date: str | None = None,
    end_date: str | None = None
)
```

---

## Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `symbol` | str | Yes | Stock ticker symbol | `"AAPL"` |
| `indexname` | str | Yes | Name of index/watchlist | `"Russell 3000"`, `"Russell 3000 Current & Past"` |
| `timeseriesformat` | str | No | Output format (default: "numpy-recarray") | `"pandas-dataframe"`, `"numpy-recarray"` |
| `start_date` | str | No | Start date for timeseries | `"2020-01-01"` |
| `end_date` | str | No | End date for timeseries | `"2020-12-31"` |

---

## Return Format (pandas-dataframe)

**Structure:**
- **Type:** `pandas.DataFrame`
- **Index:** DatetimeIndex with name `'Date'` (dtype: `datetime64[ns]`)
- **Columns:** Single column `'Index Constituent'` (dtype: `int64`)
- **Values:** `0` = not a member, `1` = member

**Example Output:**
```
            Index Constituent
Date
2020-01-02                  1
2020-01-03                  1
2020-01-06                  1
2020-01-07                  1
2020-01-08                  1
```

**Date Range:**
- Without `start_date`/`end_date`: Returns full history from earliest available to present (~9,050 days for stocks from 1990)
- With date limits: Returns only specified range
- Only includes trading days (weekends/holidays excluded)

---

## Test Results

### Test 1: Basic Call (AAPL in Russell 3000)

**Command:**
```python
result = norgatedata.index_constituent_timeseries(
    'AAPL',
    'Russell 3000',
    timeseriesformat='pandas-dataframe',
)
```

**Result:**
- Shape: `(9050, 1)` (trading days from 1990-01-02 to 2025-12-05)
- AAPL was NOT a member in 1990 (value = 0)
- AAPL IS a member in 2025 (value = 1)

---

### Test 2: Date Range Filtering

**Command:**
```python
result = norgatedata.index_constituent_timeseries(
    'AAPL',
    'Russell 3000',
    timeseriesformat='pandas-dataframe',
    start_date='2020-01-01',
    end_date='2020-12-31'
)
```

**Result:**
- Shape: `(253, 1)` (253 trading days in 2020)
- Date range: 2020-01-02 to 2020-12-31 (note: Jan 1 was a holiday, series starts Jan 2)
- Successfully filters to requested range

**Key Insight:** Date filtering works and significantly reduces data size for bridge transfer.

---

### Test 3: Checking Specific Date Membership

**Command:**
```python
target_date = date(2010, 1, 1)
result = norgatedata.index_constituent_timeseries(
    'AAPL',
    'Russell 3000',
    timeseriesformat='pandas-dataframe',
)

# Check if date exists
target_timestamp = pd.Timestamp(target_date)
if target_timestamp in result.index:
    is_member = bool(result.loc[target_timestamp, 'Index Constituent'])
```

**Result:**
- 2010-01-01 was not a trading day (New Year's Day)
- Nearest trading day: 2009-12-31
- AAPL was a member (value = 1)

**Key Insight:** Must handle non-trading days (weekends/holidays). Use nearest trading day or filter to valid business days.

---

### Test 4: Edge Cases

#### 4a. Invalid Index Name

**Command:**
```python
result = norgatedata.index_constituent_timeseries(
    'AAPL',
    'NotARealIndex',
    timeseriesformat='pandas-dataframe',
)
```

**Result:**
- Raises: `ValueError` (with empty message)
- NDU logs: `ERROR: Norgate Data: index_constituent_timeseries: NotARealIndex not found`

#### 4b. Invalid Symbol

**Command:**
```python
result = norgatedata.index_constituent_timeseries(
    'ZZZZ',
    'Russell 3000',
    timeseriesformat='pandas-dataframe',
)
```

**Result:**
- Raises: `ValueError` (with empty message)
- NDU logs: `ERROR: Norgate Data: index_constituent_timeseries: ZZZZ not found`

**Key Insight:** Both invalid index and invalid symbol raise the same `ValueError` with no message. Must rely on NDU stderr logging to distinguish error type.

---

### Test 5: JSON Serialization for Bridge

**Command:**
```python
result = norgatedata.index_constituent_timeseries(
    'AAPL',
    'Russell 3000',
    timeseriesformat='pandas-dataframe',
    start_date='2020-01-01',
    end_date='2020-01-10'
)

# Serialize for bridge transfer
result_dict = result.reset_index().to_dict('records')
json_str = json.dumps(result_dict, default=str)
```

**Result:**
```json
[
  {"Date": "2020-01-02 00:00:00", "Index Constituent": 1},
  {"Date": "2020-01-03 00:00:00", "Index Constituent": 1},
  {"Date": "2020-01-06 00:00:00", "Index Constituent": 1}
]
```

**Key Insight:**
- Use `.reset_index().to_dict('records')` pattern (same as `fetch_price_data()`)
- Dates serialize as ISO-like strings with time component
- Compatible with existing bridge pattern

---

### Test 6: Available Watchlists

**Command:**
```python
watchlists = norgatedata.watchlists()
russell_lists = [w for w in watchlists if 'Russell' in w]
```

**Result:** 22 Russell-related watchlists including:
- `Russell 3000`
- `Russell 3000 Current & Past`
- `Russell 1000`
- `Russell 1000 Current & Past`
- `Russell 2000`
- `Russell 2000 Current & Past`
- etc.

**Key Insight:** "Current & Past" versions should be used to include delisted securities for survivorship-bias-free backtesting.

---

### Test 7: Getting All Index Constituents

**Alternative Approach - Watchlist Symbols:**

**Command:**
```python
symbols = norgatedata.watchlist_symbols('Russell 3000')
```

**Result:**
- Returns: List of 2,952 symbols currently in Russell 3000
- First 10: `['A', 'AA', 'AAL', 'AAMI', 'AAOI', 'AAON', 'AAP', 'AAPL', 'AARD', 'AAT']`

**Key Insight:**
- `watchlist_symbols()` returns CURRENT constituents only
- To get historical constituents at a specific date, must:
  1. Get all symbols from "Current & Past" watchlist, OR
  2. Use cached universe of symbols to check, OR
  3. Iterate through `index_constituent_timeseries()` for each known symbol

---

## Recommended Implementation Strategy

### For Story 1.4: `get_index_constituents_at_date()`

**Function Signature:**
```python
def get_index_constituents_at_date(
    index_name: str,
    target_date: date,
    symbols: list[str] | None = None,
) -> list[str]:
    """Get list of symbols that were index members at specific date.

    Args:
        index_name: Name of index (e.g., "Russell 3000 Current & Past")
        target_date: Date to check membership
        symbols: Optional list of symbols to check (if None, checks all from watchlist)

    Returns:
        List of symbols that were members at target_date
    """
```

**Implementation Approach:**

**Option A: Check Provided Symbols (Recommended for Story 1.4)**
```python
# When symbols list is provided (typical backtest scenario)
constituents = []
for symbol in symbols:
    # Use bridge to get timeseries for narrow date range (e.g., +/- 5 days)
    timeseries = fetch_index_constituent_timeseries(
        symbol=symbol,
        index_name=index_name,
        start_date=target_date - timedelta(days=5),
        end_date=target_date + timedelta(days=5),
    )
    # Check if symbol was member on target_date
    if timeseries.loc[target_date, 'Index Constituent'] == 1:
        constituents.append(symbol)
return constituents
```

**Option B: Get All Constituents (Future Enhancement)**
```python
# When symbols=None, need to discover all historical members
# This requires getting watchlist and checking each symbol
all_symbols = norgatedata.watchlist_symbols(f"{index_name} Current & Past")
# Then proceed as Option A
```

**Performance Considerations:**
- 1000 symbols × ~7ms/call = ~7 seconds per date
- Use narrow date windows (±5 days) to minimize data transfer
- Consider caching constituent data similar to price data
- Bridge timeout: use 300s for full universe checks

---

## Bridge Integration Pattern

**New Bridge Function to Add:**

```python
def fetch_index_constituent_timeseries(
    symbol: str,
    index_name: str,
    start_date: date | None = None,
    end_date: date | None = None,
    timeout: int = 30,
) -> pd.DataFrame:
    """Fetch index constituent timeseries via Windows Python bridge.

    Returns DataFrame with DatetimeIndex and 'Index Constituent' column (0 or 1).

    Schema:
        Index: date (datetime64[ns])
        Columns:
            - Index Constituent (int64): 1 if member, 0 if not
    """

    # Construct norgatedata API call
    code_parts = [
        "(lambda: (",
        "norgatedata.index_constituent_timeseries(",
        f'"{symbol}"',
        f', "{index_name}"',
        ', timeseriesformat="pandas-dataframe"',
    ]

    if start_date:
        code_parts.append(f', start_date="{start_date.isoformat()}"')
    if end_date:
        code_parts.append(f', end_date="{end_date.isoformat()}"')

    code_parts.append(")")

    # Serialize DataFrame for JSON transfer
    code_parts.append(".reset_index()")
    code_parts.append(".assign(Date=lambda x: x['Date'].astype(str))")
    code_parts.append(".to_dict('records')")
    code_parts.append("))()")

    code = "".join(code_parts)

    # Execute via bridge
    result = execute_norgate_code(code, timeout=timeout)

    # Parse result into DataFrame
    df = pd.DataFrame(result)
    df.columns = df.columns.str.lower()
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df.index.name = 'date'

    return df
```

---

## Error Handling

**Expected Errors:**

1. **Invalid Index Name:** `ValueError` (empty message)
   - Check: NDU stderr contains "not found"
   - Solution: Validate index_name against `norgatedata.watchlists()` first

2. **Invalid Symbol:** `ValueError` (empty message)
   - Check: NDU stderr contains "not found"
   - Solution: Skip symbol and log warning, continue with others

3. **Date Out of Range:** No error raised
   - If start_date is before listing, returns data from listing date forward
   - If end_date is after delisting, returns data up to delisting

4. **Non-Trading Day:** No error raised
   - Only trading days appear in result
   - Use pandas `DatetimeIndex` slicing or `.get_indexer()` with `method='nearest'`

**Recommended Error Handling Strategy:**
```python
from momo.utils.exceptions import ValidationError, NorgateBridgeError

try:
    timeseries = fetch_index_constituent_timeseries(symbol, index_name, ...)
except ValueError as e:
    # Could be invalid symbol or invalid index
    logger.warning("constituent_check_failed", symbol=symbol, index=index_name)
    # Skip this symbol, continue with others
    continue
except NorgateBridgeError as e:
    # Bridge communication error
    logger.error("bridge_error", error=str(e))
    raise ValidationError(f"Failed to retrieve constituent data: {e}")
```

---

## Testing Recommendations

### Unit Tests (Mock Bridge)

**Test ID: 1.4-UNIT-014**
```python
@pytest.mark.p0
@pytest.mark.unit
def test_1_4_unit_014(mocker):
    """Test get_index_constituents_at_date with mocked bridge response."""
    # Mock bridge to return sample timeseries
    mock_bridge = mocker.patch('momo.data.validation.fetch_index_constituent_timeseries')
    mock_bridge.return_value = pd.DataFrame({
        'Index Constituent': [1, 1, 1]
    }, index=pd.DatetimeIndex(['2020-01-02', '2020-01-03', '2020-01-06'], name='date'))

    # Test function
    constituents = get_index_constituents_at_date(
        index_name='Russell 3000',
        target_date=date(2020, 1, 3),
        symbols=['AAPL', 'MSFT']
    )

    assert 'AAPL' in constituents
```

### Integration Tests (Real Bridge)

**Test ID: 1.4-INT-001**
```python
@pytest.mark.p1
@pytest.mark.integration
def test_1_4_int_001():
    """Test real bridge call for AAPL Russell 3000 membership."""
    # Requires NDU running
    from momo.data.validation import get_index_constituents_at_date

    constituents = get_index_constituents_at_date(
        index_name='Russell 3000',
        target_date=date(2020, 1, 3),
        symbols=['AAPL']
    )

    assert 'AAPL' in constituents  # AAPL was definitely in R3000 in 2020
```

---

## Key Takeaways

1. **API is Simple:** `index_constituent_timeseries()` returns a 0/1 timeseries for a single symbol
2. **Date Filtering Works:** Use `start_date`/`end_date` to minimize data transfer (critical for bridge efficiency)
3. **JSON Serialization:** Same pattern as `fetch_price_data()` - works perfectly
4. **Error Handling:** `ValueError` for both invalid index and symbol (distinguish via stderr logging)
5. **Current & Past:** Use "Current & Past" watchlists to avoid survivorship bias
6. **Performance:** ~7ms per symbol-index check, scalable to 1000+ symbols with proper timeout
7. **Bridge Ready:** Can implement using existing `execute_norgate_code()` pattern

---

## Next Steps for Story 1.4

1. ✅ Add `fetch_index_constituent_timeseries()` to `src/momo/data/bridge.py`
2. ✅ Implement `get_index_constituents_at_date()` in `src/momo/data/validation.py`
3. ✅ Add unit tests with mocked bridge responses (tests/stories/1.4/unit/)
4. ✅ Add integration test with real NDU call (tests/stories/1.4/integration/)
5. ✅ Update ValidationReport to include constituent validation results
6. ✅ Document usage in module docstrings

---

## References

- **Norgate Documentation:** `docs/research/norgatedata-python.pdf` (pages 8-10: Index Constituents)
- **Story Document:** `docs/stories/1.4.story.md`
- **Bridge Implementation:** `src/momo/data/bridge.py`
- **ADR-002:** Windows Python Bridge for Norgate Data
