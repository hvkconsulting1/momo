# Epic 1: Foundation & Data Infrastructure

**Epic Goal:** Establish project setup with proper repository structure and dependency management, integrate Norgate Data API via Windows Python bridge, implement data loading and caching to Parquet files, build data quality validation pipeline, and create end-to-end verification demonstrating the complete data flow works correctly. This epic delivers the foundational data infrastructure required for all subsequent strategy development.

## Story 1.0: Norgate Data API Exploration Spike (Research)

**Status:** COMPLETE (2025-11-25)
**Decision:** GO - Proceed with architecture design
**Findings:** [docs/research/norgate-api-exploration.md](../research/norgate-api-exploration.md)

**As a** quantitative researcher,
**I want** to systematically explore the Norgate Data Python API capabilities and limitations,
**so that** I can validate the technical feasibility of building a survivorship bias-free dataset and inform architectural decisions before committing to implementation.

### Background

This is a time-boxed research spike that must complete before architecture design. The Norgate Data API is the foundation of the entire data layer, and key questions about index availability, delisted stock handling, and performance characteristics will directly impact architectural decisions. The exploration follows the structured plan in `docs/norgate-data-exploration-plan.md`.

### Acceptance Criteria

**Phase 1: Connectivity & Subscription Audit**
1. Verify NDU (Norgate Data Updater) is running and accessible via `norgatedata.status()`
2. Document all available databases using `norgatedata.databases()` - confirm "US Equities Delisted" is present
3. Document all available watchlists using `norgatedata.watchlists()` - identify Russell-related watchlists (e.g., "Russell 1000 Current & Past", "Russell 3000 Current & Past")
4. Record exact watchlist names available for universe construction

**Phase 2: Index Constituent Capabilities**
5. Test which index names are recognized by `index_constituent_timeseries()`: 'Russell 1000', 'Russell 3000', 'S&P 500', 'S&P 1500'
6. Examine the structure of index constituent time series data (column names, value format 0/1, date range coverage)
7. Verify index constituent data can be retrieved for at least one known delisted stock (e.g., LEH, YHOO, or similar)
8. Document how far back historical index constituent data extends

**Phase 3: Universe Construction Feasibility**
9. Retrieve symbol list from appropriate "Current & Past" watchlist and categorize by status (current vs delisted)
10. Demonstrate point-in-time universe reconstruction for a sample date (e.g., 2020-01-01) using a subset of 50 symbols
11. Document the approach needed for full universe reconstruction and estimated complexity

**Phase 4: Price Data Validation**
12. Verify price data retrieval with different adjustment types (NONE, CAPITAL, TOTALRETURN) and document differences
13. Confirm full price history is retrievable for at least one delisted stock up to its delisting date
14. Document price DataFrame structure (columns: Open, High, Low, Close, Volume, etc.)

**Phase 5: Fundamental Data Assessment**
15. Test fundamental data retrieval (`norgatedata.fundamental()`) for fields: 'mktcap', 'sharesoutstanding', 'sharesfloat'
16. Confirm whether historical market cap time series exists (expected: NO - only current point-in-time values)
17. Document implications: Russell index membership serves as market cap ranking proxy

**Phase 6: Performance Profiling**
18. Time price data retrieval for 100 symbols sequentially and calculate average ms/symbol
19. Test parallel retrieval using ThreadPoolExecutor (4 workers) and measure speedup
20. Estimate total time required to fetch full Russell 3000 Current & Past universe (~5000 symbols)

**Phase 7: Documentation & Decision**
21. Complete the Decision Matrix in `docs/norgate-data-exploration-plan.md` with all findings
22. Create `docs/norgate-api-findings.md` summarizing:
    - Confirmed capabilities and limitations
    - Recommended universe approach (Russell 1000 vs 3000 vs S&P combination)
    - Performance characteristics and caching recommendations
    - Data schema implications for architecture
23. Provide clear GO/NO-GO recommendation with rationale
24. If GO: Document any constraints or workarounds the architecture must accommodate

### Go/No-Go Criteria (Blockers)

The spike results in **GO** only if ALL of the following are confirmed:
- [x] Access to delisted securities database (8,377 delisted in Russell 3000 C&P)
- [x] Historical index constituent time series works for target index (verified 1990-present)
- [x] Can retrieve index membership for delisted stocks (verified with LEH, MER, BSC)
- [x] Full price history available for delisted stocks up to delisting date (verified)

### Deliverables

1. ~~**Exploration notebook**: `notebooks/00_norgate_api_exploration.ipynb` with executed code for all phases~~ (executed interactively via Windows Python bridge)
2. **Findings document**: `docs/research/norgate-api-exploration.md` with structured summary ✅
3. **Updated decision matrix**: Completed in findings document ✅
4. **Architecture input**: Clear recommendations for data layer design ✅

### Notes

- This story requires a Windows environment with NDU running and active Norgate Platinum subscription
- **For WSL development**: Use Windows Python bridge pattern (execute code via `python.exe` subprocess) - see Story 1.0 findings
- **For Windows development**: Direct norgatedata package usage
- Time-box: This spike should complete within 1 working day
- If NO-GO: Document blockers and alternative data source options before proceeding

---

## Story 1.1: Initialize Project Structure and Development Environment

**As a** developer,
**I want** the project structure and dependencies set up following the specified monorepo layout,
**so that** I can begin development with proper tooling and organization in place.

### Acceptance Criteria

1. Repository follows the specified structure with directories: `data/`, `src/` (with subdirs: `data/`, `signals/`, `portfolio/`, `backtest/`, `risk/`, `utils/`), `notebooks/`, `docs/`, `tests/`, and `results/`
2. Python 3.10+ environment is configured with uv (Astral) for dependency management
3. `.gitignore` is configured to exclude `data/` directory and common Python artifacts (__pycache__, .pyc, .env, etc.)
4. Initial `pyproject.toml` or `requirements.txt` includes core dependencies: pandas, numpy, scipy, matplotlib, seaborn, jupyter, pytest
5. `README.md` provides basic project overview and setup instructions
6. `docs/research-log.md` template is created with structure for documenting experiments (date, hypothesis, parameters, results, insights)
7. Basic package structure allows `import src` from project root
8. All directory structures can be verified via automated test or script

## Story 1.2: Integrate Norgate Data API via Windows Python Bridge

**As a** developer,
**I want** to connect to Norgate Data API via the Windows Python bridge,
**so that** I can retrieve historical price data for backtesting.

### Acceptance Criteria

1. `norgatedata` Python package is installed in Windows Python and accessible via bridge (not required in WSL Python)
2. Windows Python bridge module (`src/momo/data/bridge.py`) implements subprocess-based NDU communication following the pattern from Story 1.0 exploration
3. Basic connection test successfully retrieves a sample ticker's price data via the bridge
4. Error handling provides clear messages if NDU is not running or accessible
5. Documentation in `docs/` explains the Windows Python bridge architecture and NDU prerequisites (Windows environment with NDU running and authenticated)
6. Unit test verifies bridge communication using mock subprocess responses

## Story 1.3: Implement Data Loading and Parquet Caching

**As a** developer,
**I want** to load historical price data from Norgate and cache it to local Parquet files,
**so that** backtests can run quickly and reproducibly without repeated API calls.

### Acceptance Criteria

1. `src/data/loader.py` module implements function to fetch OHLCV data for a list of tickers over a date range using norgatedata API
2. Fetched data includes adjustment factors for splits and dividends (adjusted prices)
3. Data is cached to Parquet files in `data/` directory with organized naming scheme (e.g., by universe or date range)
4. Cache loading function checks if local Parquet exists before querying Norgate API
5. Force-refresh option allows re-fetching data even if cache exists
6. Loading a cached dataset is significantly faster than API query (measurable performance difference)
7. Cached Parquet files can be read back into pandas DataFrames with correct dtypes and index
8. Unit tests verify caching logic (write → read → validate equality)

## Story 1.4: Build Data Quality Validation Pipeline

**As a** developer,
**I want** automated data quality checks for missing prices, corporate actions, and point-in-time constituents,
**so that** backtest integrity is ensured and survivorship bias is eliminated.

### Acceptance Criteria

1. `src/data/validation.py` module implements data quality check functions
2. Validation detects missing price data (NaN or gaps in expected date ranges) and reports affected tickers
3. Validation checks for adjustment factor consistency (splits/dividends properly applied)
4. Function retrieves point-in-time index constituents for a specified date using Norgate API (e.g., S&P 500 constituents as of 2010-01-01)
5. Delisting data is accessible and can be queried to identify when tickers were removed from the universe
6. Validation report summarizes: total tickers, date range, missing data counts, delisting events
7. Tests verify validation functions correctly identify synthetic missing data and corporate action issues
8. Documentation explains how to interpret validation reports and handle common data quality issues

## Story 1.5: Implement Point-in-Time Universe Construction

**As a** quantitative researcher,
**I want** to construct the investable universe at each rebalance date using point-in-time index constituents with proper history requirements,
**so that** backtests eliminate both survivorship bias and look-ahead bias.

### Acceptance Criteria

1. `src/data/universe.py` module implements function `get_point_in_time_universe()` that accepts index name, date, and minimum history months
2. Function retrieves index constituent time series from Norgate API for target index (Russell 1000 Current & Past)
3. For each rebalance date, returns list of tickers that were actual index members at that time
4. Applies minimum history filter: only include securities with ≥N months of price data prior to rebalance date (default N=12)
5. Handles delisted securities correctly: include up to delisting date, exclude after delisting
6. Function caches universe snapshots to Parquet files to avoid repeated API calls during backtesting
7. Edge case handling: stocks with gaps in membership (delisted and relisted), newly added constituents
8. Configuration parameter for index selection: default Russell 1000 Current & Past (matches Jegadeesh & Titman large/mid-cap universe)
9. Unit tests verify universe at known historical dates matches expected constituents (e.g., verify LEH in Russell 1000 pre-2008, excluded post-delisting)
10. Integration with Story 1.3 data loading: pipeline fetches price data only for universe-valid tickers at each rebalance date
11. Documentation explains rationale: Russell 1000 C&P provides ~1000 large/mid-cap stocks matching academic baseline, excludes micro-cap liquidity issues
12. Performance requirement: Universe construction for 20 years of monthly rebalances completes in under 30 seconds

### Notes

- **Index Choice Rationale:** Russell 1000 Current & Past provides ~1000 large/mid-cap stocks, matching the Jegadeesh & Titman (1993) universe size and implicitly excluding very small/illiquid stocks. This can be configured to Russell 3000 C&P for future small-cap momentum experiments.
- **Minimum History:** 12-month requirement ensures all securities have sufficient data for momentum signal calculation (12-1 lookback). IPOs and recently listed stocks are automatically excluded until they have adequate history.
- This story delivers the foundation for survivorship-bias-free AND look-ahead-bias-free backtesting.

## Story 1.6: Create End-to-End Data Pipeline Verification

**As a** researcher,
**I want** an end-to-end test demonstrating the complete data pipeline from Norgate API to cached Parquet to validation,
**so that** I can verify data infrastructure is working correctly before building momentum strategies.

### Acceptance Criteria

1. Integration test or notebook (`notebooks/01_data_pipeline_verification.ipynb`) demonstrates full pipeline
2. Pipeline uses point-in-time universe construction from Story 1.5 for a test index over at least 5 years
3. Data is cached to Parquet files in `data/` directory
4. Cached data is reloaded and validated using quality checks from Story 1.4
5. Validation report is generated showing data completeness and any issues
6. Simple visualization (e.g., price chart for 2-3 tickers) confirms data looks reasonable
7. Pipeline completes successfully with clear logging indicating each step (fetch → cache → validate → report)
8. Documentation in `docs/` or notebook explains how to run the verification and interpret results
9. Test can be run locally by any developer on Windows environment with NDU installed, running, and authenticated with valid Norgate subscription
