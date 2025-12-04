# External APIs

## Norgate Data API

| Item | Value |
|------|-------|
| **Purpose** | Market data source - historical prices, index constituents, corporate actions |
| **Documentation** | https://norgatedata.com/python.php |
| **Base URL(s)** | Local IPC (Windows COM/pipe) - no network calls |
| **Authentication** | NDU desktop application must be running with valid subscription |
| **Rate Limits** | None (local API); ~7ms/symbol per exploration findings |

**Key Endpoints Used:**

| Function | Purpose |
|----------|---------|
| `norgatedata.price_timeseries(symbol, ...)` | Fetch OHLCV data with adjustment options |
| `norgatedata.watchlist_symbols(watchlist)` | Get symbols in a watchlist |
| `norgatedata.index_constituent_timeseries(symbol, index)` | Point-in-time index membership |
| `norgatedata.status()` | Check if NDU is running |

**Integration Notes:**
1. Windows-only constraint - use `python.exe` bridge from WSL
2. Use `StockPriceAdjustmentType.TOTALRETURN` for backtesting
3. Use `PaddingType.NONE` to avoid forward-filling delisted securities
4. Use `*Current & Past` watchlists for survivorship-bias-free universe
5. No historical market cap available - use index membership as size proxy

---
