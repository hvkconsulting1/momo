# portfolio-momentum Product Requirements Document (PRD)

## Goals and Background Context

### Goals

- **Implement V1 Cross-Sectional Momentum Strategy** with complete backtest demonstrating the classic Jegadeesh & Titman 12-1 momentum approach
- **Establish Modular Framework Architecture** with clear separation between Data, Signal, Portfolio Construction, Backtest, and Risk layers
- **Enable Rapid Strategy Experimentation** allowing new momentum variants to be tested in hours rather than days
- **Achieve Paper Trading Readiness** with automated signal generation and position calculation for forward validation
- **Build Deep Understanding** of momentum strategy behavior across different market regimes through systematic implementation and research
- **Create Production-Ready System** with clear progression path from research → backtest → paper trading → live deployment

### Background Context

Momentum strategies are among the most well-documented market anomalies in academic finance, with decades of empirical evidence supporting their effectiveness (Jegadeesh & Titman 1993, Moskowitz et al. 2012). However, a significant gap exists between understanding these strategies conceptually and implementing them in a practical, robust manner. Individual quantitative traders and researchers face fragmented learning experiences, inflexible architectures that don't support experimentation, and unclear paths from backtest to production deployment.

This PRD addresses these challenges by specifying a **modular research and trading framework** optimized for depth in momentum strategies. Unlike commercial platforms that impose vendor lock-in or academic code that lacks production quality, this framework treats extensibility and scientific rigor as first-class requirements. The system serves as a personal "momentum lab" where strategies can be systematically validated, thoroughly understood through building, and confidently deployed with real capital under clearly defined risk controls. The framework leverages Norgate Data for survivorship-bias-free backtesting and follows a staged progression from simple implementations to sophisticated multi-strategy portfolios.

### Change Log

| Date | Version | Description | Author |
|------|---------|-------------|--------|
| 2025-11-23 | 0.1 | Initial PRD draft from project brief | PM Agent |
| 2025-11-25 | 0.2 | Added Story 1.0: Norgate Data API Exploration Spike to validate data layer feasibility before architecture | PM Agent |

## Requirements

### Functional

**FR1:** The system shall ingest historical price data (OHLCV) from Norgate Data for a defined equity universe with adjustments for splits, dividends, and delistings

**FR2:** The system shall calculate cross-sectional momentum signals using the 12-1 methodology (cumulative return from t-12 to t-2 months)

**FR3:** The system shall rank securities based on momentum signals and construct portfolios using decile-based selection (top 10% long, bottom 10% short)

**FR4:** The system shall apply equal-weight allocation within each portfolio leg, normalized to 1x gross exposure per leg (2x total gross, 0 net)

**FR5:** The system shall execute backtests computing monthly returns, cumulative portfolio value, CAGR, volatility, Sharpe ratio, maximum drawdown, and monthly turnover

**FR6:** The system shall generate equity curve visualizations and summary statistics tables from backtest results

**FR7:** The system shall track point-in-time index constituents to eliminate survivorship bias in backtests

**FR8:** The system shall validate data quality including checks for missing prices, adjustment factors, and delisting events

**FR9:** The system shall support modification of strategy parameters (lookback periods, decile vs quintile selection, skip months) and re-run backtests in under 5 minutes

**FR10:** The system shall provide a research notebook structure for documenting experiments with date, hypothesis, parameters, results, and insights

**FR11:** The system shall expose composable signal and portfolio construction functions that can be combined independently

**FR12:** The system shall cache Norgate data locally to Parquet files for reproducible backtests and faster iteration

**FR13:** The system shall export backtest results to standard formats (CSV/JSON) for external analysis

### Non Functional

**NFR1:** Backtest execution for 30+ years of monthly data across 500+ securities must complete in under 1 minute

**NFR2:** The architecture must maintain clear separation of concerns across Data, Signal, Portfolio Construction, Backtest, and Risk layers

**NFR3:** Adding new momentum strategy variants (time-series, dual momentum) must not require changes to the backtest engine or data layer

**NFR4:** Signal calculation functions must be pure (deterministic, no side effects) to ensure reproducible results

**NFR5:** The codebase must remain comprehensible and maintainable with clear interfaces between modules

**NFR6:** Unit tests must cover signal calculations and portfolio construction logic with validation against known results

**NFR7:** The system must support offline operation with locally cached Norgate data for reproducible backtests

**NFR8:** Data ingestion must leverage Norgate's survivorship-bias-free historical constituents to ensure backtest integrity

**NFR9:** Parameter sweep testing (10+ variants) must complete in under 10 minutes to support robustness analysis

**NFR10:** The system must handle corporate actions (splits, dividends, delistings) without manual intervention

## User Interface Design Goals

### Overall UX Vision

The framework provides a **code-first research environment** where quantitative traders interact primarily through Jupyter notebooks and Python scripts. The user experience emphasizes clarity, reproducibility, and rapid iteration. Users should be able to explore data, run backtests, visualize results, and document findings within an integrated notebook environment. The interface prioritizes simplicity and transparency—users can see exactly what the code is doing at each step, with clear separation between data loading, signal calculation, portfolio construction, and performance analysis.

### Key Interaction Paradigms

- **Interactive Notebook Exploration:** Jupyter notebooks serve as the primary interface for research, allowing step-by-step execution, inline visualization, and markdown documentation
- **Functional Pipeline Pattern:** Users compose strategies by chaining pure functions (data → signals → weights → backtest → results)
- **Configuration via Python Objects/Dicts:** Strategy parameters are specified as simple Python dictionaries or dataclass configurations rather than GUI controls
- **Immediate Visual Feedback:** Equity curves, drawdown charts, and performance statistics render inline immediately after backtest execution
- **Markdown Research Log:** Users maintain a markdown-based research notebook alongside code notebooks for high-level insights and decision documentation

### Core Screens and Views

Since this is not a screen-based application, these represent the key "conceptual views" or notebook sections:

- **Data Exploration View:** Inspect loaded price data, check for missing values, visualize universe composition over time
- **Signal Analysis View:** Calculate and visualize momentum signals, examine cross-sectional rankings, validate signal distributions
- **Backtest Results Dashboard:** Equity curve, drawdown chart, monthly returns heatmap, and summary statistics table
- **Performance Comparison View:** Side-by-side comparison of multiple strategy variants or parameter settings
- **Research Log Entry Template:** Structured markdown template for documenting each experiment

### Accessibility

**None** - This is a personal research tool used in Jupyter notebooks with primarily visual outputs (charts, tables). Standard accessibility features of the Jupyter environment apply, but no specific accessibility requirements beyond that.

### Branding

**Minimal/Academic Aesthetic** - Visualizations should use clean, professional styling suitable for research documentation. Default matplotlib/seaborn styles are acceptable for MVP. Emphasis on clarity and readability over visual flair. Charts should be publication-quality (clear labels, legends, appropriate color schemes for colorblind-friendly differentiation).

### Target Device and Platforms

**Desktop/Laptop Only - Jupyter Notebook Environment**

- Primary platform: Linux/macOS local development machines
- Jupyter notebooks run locally or in local Jupyter Lab/Notebook server
- No mobile or tablet support required
- Assumes standard developer workstation with Python 3.10+ environment

## Technical Assumptions

### Repository Structure

**Monorepo** - Single repository containing all components of the portfolio-momentum framework with the following structure:

```
portfolio-momentum/
├── data/               # Cached price data (gitignored)
├── src/
│   ├── data/          # Norgate data access, caching, preprocessing
│   ├── signals/       # Signal calculation functions
│   ├── portfolio/     # Portfolio construction logic
│   ├── backtest/      # Backtesting engine
│   ├── risk/          # Risk management and execution modeling
│   └── utils/         # Shared utilities and helpers
├── notebooks/         # Jupyter notebooks for research
├── docs/              # Documentation, strategy specs, research log
├── tests/             # Unit and integration tests
└── results/           # Backtest outputs, performance reports
```

**Rationale:** A monorepo keeps all layers (Data/Signal/Portfolio/Backtest/Risk) together for easier development, testing, and ensuring version consistency across components. This is appropriate for a personal research project where coordination overhead is minimal.

### Service Architecture

**Monolithic Python Package** - The framework is structured as a single Python package with modular internal architecture following the layered design pattern (Data → Signal → Portfolio → Backtest → Risk). Each layer is implemented as a separate subpackage with well-defined interfaces.

**Rationale:** For a research framework processing batch computations locally, a monolithic architecture is simpler and more appropriate than microservices. The modular internal structure provides the necessary separation of concerns without distributed systems complexity.

**Key Architectural Principles:**
- **Separation of concerns:** Each layer is independently testable
- **Pure functions:** Signal calculations are deterministic with no side effects
- **Composability:** Mix and match signals, portfolio construction methods, and risk overlays
- **Data pipeline flow:** Clear progression from Norgate → cleaned data → signals → weights → performance

### Testing Requirements

**Unit + Integration Testing** focused on correctness and reproducibility:

- **Unit tests:** pytest-based tests for signal calculation functions, portfolio construction logic, and performance metric calculations
- **Validation tests:** Compare backtest results against known benchmarks or academic paper results where possible
- **Data quality tests:** Validate Norgate data loading, corporate action handling, and survivorship bias elimination
- **Integration tests:** End-to-end backtest runs with fixed seeds/data to ensure reproducibility
- **Test coverage target:** Priority on critical calculation paths (signals, returns, metrics) rather than 100% coverage

**Rationale:** For a research framework, correctness is paramount. Unit tests ensure signal calculations are bug-free, while integration tests validate the full pipeline produces reproducible results. Manual testing in Jupyter notebooks will supplement automated tests for exploratory analysis.

### Additional Technical Assumptions and Requests

**Primary Language & Version:**
- Python 3.10+ (modern Python with type hints support, standard for quantitative finance)

**Core Data Stack:**
- **pandas** - Time series manipulation and tabular data operations
- **numpy** - Numerical computations and array operations
- **scipy/statsmodels** - Statistical analysis and performance metrics calculation

**Visualization Libraries:**
- **matplotlib** - Equity curves, performance charts, distribution plots
- **seaborn** - Statistical visualizations with better default aesthetics
- **plotly** - Optional for interactive visualizations
- **Jupyter notebooks** - Interactive research and experimentation environment

**Rationale:** Both matplotlib and plotly are available as options. Matplotlib provides publication-quality static charts, while plotly enables interactive exploration when beneficial.

**Data Source & Access:**
- **Norgate Data** (Platinum US Stocks subscription) - Primary data source
  - Historical data from 1990+ (30+ years coverage)
  - Point-in-time index constituents (eliminates look-ahead bias)
  - Delisting data (eliminates survivorship bias)
  - Adjusted prices for splits/dividends
- **norgatedata Python package** - API access to Norgate data
- **Data caching strategy:** Cache to local Parquet files by default for faster iteration and reproducible backtests
- **Universe definition:** Historical S&P 500 constituents, Russell 1000, or custom market-cap filters

**Development Tools:**
- **Version control:** Git (already in use)
- **Dependency management:** uv (Astral) for fast, reliable Python package management
- **Code quality:** ruff or pylint for linting, type hints where beneficial
- **Testing framework:** pytest for all automated tests

**Security & Configuration:**
- **Norgate credentials:** Store securely via environment variables or gitignored config file
- **Data directory:** .gitignore data/ folder to avoid committing large price datasets
- **No PII/sensitive data:** Framework handles only public market data

**Performance Targets (from NFR):**
- Backtest for 30 years × 500 securities in <1 minute
- Parameter sweeps (10 variants) in <10 minutes
- Leverage pandas vectorization and numpy optimizations; consider numba/Cython only if bottlenecks emerge

**No External Backtesting Framework Dependency:**
- Custom-built backtest engine (core requirement for learning and control)
- Potential integration with zipline, backtrader, or vectorbt for comparison/validation only (not dependencies)

**Deployment Target:**
- Local development on personal machine for MVP
- Potential cloud deployment (AWS/GCP) for paper trading phase (post-MVP)

## Epic List

**Epic 1: Foundation & Data Infrastructure**
Establish project setup, Norgate Data integration, and basic data pipeline with end-to-end smoke test demonstrating data can be loaded, cached, and validated.

**Epic 2: Momentum Signal & Portfolio Construction**
Implement 12-1 cross-sectional momentum signal calculation and decile-based portfolio construction with equal-weight allocation.

**Epic 3: Backtest Engine & Performance Analytics**
Build the core backtesting engine that processes portfolios, computes returns, and generates performance metrics (CAGR, Sharpe, drawdown, turnover) with visualization capabilities.

**Epic 4: Research Workflow & Experimentation Tools**
Create research notebook templates, parameter modification interface, and documentation structure to support systematic strategy exploration.

## Epic 1: Foundation & Data Infrastructure

**Epic Goal:** Establish project setup with proper repository structure and dependency management, integrate Norgate Data API with secure authentication, implement data loading and caching to Parquet files, build data quality validation pipeline, and create end-to-end verification demonstrating the complete data flow works correctly. This epic delivers the foundational data infrastructure required for all subsequent strategy development.

### Story 1.0: Norgate Data API Exploration Spike (Research)

**As a** quantitative researcher,
**I want** to systematically explore the Norgate Data Python API capabilities and limitations,
**so that** I can validate the technical feasibility of building a survivorship bias-free dataset and inform architectural decisions before committing to implementation.

#### Background

This is a time-boxed research spike that must complete before architecture design. The Norgate Data API is the foundation of the entire data layer, and key questions about index availability, delisted stock handling, and performance characteristics will directly impact architectural decisions. The exploration follows the structured plan in `docs/norgate-data-exploration-plan.md`.

#### Acceptance Criteria

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

#### Go/No-Go Criteria (Blockers)

The spike results in **GO** only if ALL of the following are confirmed:
- [ ] Access to delisted securities database
- [ ] Historical index constituent time series works for target index
- [ ] Can retrieve index membership for delisted stocks
- [ ] Full price history available for delisted stocks up to delisting date

#### Deliverables

1. **Exploration notebook**: `notebooks/00_norgate_api_exploration.ipynb` with executed code for all phases
2. **Findings document**: `docs/norgate-api-findings.md` with structured summary
3. **Updated decision matrix**: Completed table in `docs/norgate-data-exploration-plan.md`
4. **Architecture input**: Clear recommendations for data layer design

#### Notes

- This story requires a Windows environment with NDU running and active Norgate Platinum subscription
- Time-box: This spike should complete within 1 working day
- If NO-GO: Document blockers and alternative data source options before proceeding

---

### Story 1.1: Initialize Project Structure and Development Environment

**As a** developer,
**I want** the project structure and dependencies set up following the specified monorepo layout,
**so that** I can begin development with proper tooling and organization in place.

#### Acceptance Criteria

1. Repository follows the specified structure with directories: `data/`, `src/` (with subdirs: `data/`, `signals/`, `portfolio/`, `backtest/`, `risk/`, `utils/`), `notebooks/`, `docs/`, `tests/`, and `results/`
2. Python 3.10+ environment is configured with uv (Astral) for dependency management
3. `.gitignore` is configured to exclude `data/` directory and common Python artifacts (__pycache__, .pyc, .env, etc.)
4. Initial `pyproject.toml` or `requirements.txt` includes core dependencies: pandas, numpy, scipy, matplotlib, seaborn, jupyter, pytest
5. `README.md` provides basic project overview and setup instructions
6. `docs/research-log.md` template is created with structure for documenting experiments (date, hypothesis, parameters, results, insights)
7. Basic package structure allows `import src` from project root
8. All directory structures can be verified via automated test or script

### Story 1.2: Integrate Norgate Data API with Secure Authentication

**As a** developer,
**I want** to connect to Norgate Data API with secure credential handling,
**so that** I can retrieve historical price data for backtesting.

#### Acceptance Criteria

1. `norgatedata` Python package is installed and importable
2. Norgate credentials are loaded from environment variables or gitignored config file (never hardcoded)
3. A configuration module (`src/data/config.py`) provides centralized access to Norgate credentials
4. Basic connection test successfully authenticates and retrieves a sample ticker's price data
5. Error handling provides clear messages if credentials are missing or invalid
6. Documentation in `docs/` explains how to set up Norgate credentials for local development
7. Unit test verifies configuration loading (using mock credentials)

### Story 1.3: Implement Data Loading and Parquet Caching

**As a** developer,
**I want** to load historical price data from Norgate and cache it to local Parquet files,
**so that** backtests can run quickly and reproducibly without repeated API calls.

#### Acceptance Criteria

1. `src/data/loader.py` module implements function to fetch OHLCV data for a list of tickers over a date range using norgatedata API
2. Fetched data includes adjustment factors for splits and dividends (adjusted prices)
3. Data is cached to Parquet files in `data/` directory with organized naming scheme (e.g., by universe or date range)
4. Cache loading function checks if local Parquet exists before querying Norgate API
5. Force-refresh option allows re-fetching data even if cache exists
6. Loading a cached dataset is significantly faster than API query (measurable performance difference)
7. Cached Parquet files can be read back into pandas DataFrames with correct dtypes and index
8. Unit tests verify caching logic (write → read → validate equality)

### Story 1.4: Build Data Quality Validation Pipeline

**As a** developer,
**I want** automated data quality checks for missing prices, corporate actions, and point-in-time constituents,
**so that** backtest integrity is ensured and survivorship bias is eliminated.

#### Acceptance Criteria

1. `src/data/validation.py` module implements data quality check functions
2. Validation detects missing price data (NaN or gaps in expected date ranges) and reports affected tickers
3. Validation checks for adjustment factor consistency (splits/dividends properly applied)
4. Function retrieves point-in-time index constituents for a specified date using Norgate API (e.g., S&P 500 constituents as of 2010-01-01)
5. Delisting data is accessible and can be queried to identify when tickers were removed from the universe
6. Validation report summarizes: total tickers, date range, missing data counts, delisting events
7. Tests verify validation functions correctly identify synthetic missing data and corporate action issues
8. Documentation explains how to interpret validation reports and handle common data quality issues

### Story 1.5: Create End-to-End Data Pipeline Verification

**As a** researcher,
**I want** an end-to-end test demonstrating the complete data pipeline from Norgate API to cached Parquet to validation,
**so that** I can verify data infrastructure is working correctly before building momentum strategies.

#### Acceptance Criteria

1. Integration test or notebook (`notebooks/01_data_pipeline_verification.ipynb`) demonstrates full pipeline
2. Pipeline fetches historical data for a small test universe (e.g., 10 tickers) covering at least 5 years
3. Data is cached to Parquet files in `data/` directory
4. Cached data is reloaded and validated using quality checks from Story 1.4
5. Validation report is generated showing data completeness and any issues
6. Simple visualization (e.g., price chart for 2-3 tickers) confirms data looks reasonable
7. Pipeline completes successfully with clear logging indicating each step (fetch → cache → validate → report)
8. Documentation in `docs/` or notebook explains how to run the verification and interpret results
9. Test can be run locally by any developer with valid Norgate credentials

## Epic 2: Momentum Signal & Portfolio Construction

**Epic Goal:** Implement the 12-1 cross-sectional momentum signal calculation following Jegadeesh & Titman methodology, build cross-sectional ranking system that handles edge cases and missing data, create decile-based portfolio construction with equal-weight allocation normalized to target exposure levels, and validate the complete signal-to-weights pipeline produces sensible outputs. This epic delivers the core strategy logic that transforms price data into portfolio positions.

### Story 2.1: Implement 12-1 Momentum Signal Calculation

**As a** quantitative researcher,
**I want** to calculate 12-1 momentum signals (cumulative return from t-12 to t-2 months) for all securities in the universe,
**so that** I can rank securities by their momentum characteristics.

#### Acceptance Criteria

1. `src/signals/momentum.py` module implements a pure function `calculate_momentum_signal()` that accepts price data and returns momentum values
2. Function calculates cumulative return from 12 months ago to 2 months ago (skipping most recent month) for each security
3. Return calculation properly handles the lookback period: signal at month t uses returns from t-12 to t-2
4. Function handles missing data gracefully: returns NaN for securities with insufficient history (less than 12 months)
5. Signal calculation is vectorized using pandas/numpy for performance (no explicit loops over tickers)
6. Function is deterministic (same inputs always produce same outputs) with no side effects
7. Unit tests validate calculation against hand-computed examples for known price series
8. Unit tests verify edge cases: insufficient data, all NaN prices, single-ticker scenarios
9. Function accepts configurable parameters: lookback_months (default 12), skip_months (default 1) for future experimentation

### Story 2.2: Implement Cross-Sectional Ranking and Decile Selection

**As a** quantitative researcher,
**I want** to rank securities by momentum signals and select top/bottom deciles at each rebalance date,
**so that** I can identify long and short portfolio candidates.

#### Acceptance Criteria

1. `src/signals/ranking.py` module implements function `rank_cross_sectional()` that accepts signals and returns percentile ranks
2. Ranking is performed within each time period (cross-sectional ranking at each month)
3. Function handles NaN values by excluding them from ranking (securities with insufficient data are not ranked)
4. Function implements `select_deciles()` that identifies top 10% (long candidates) and bottom 10% (short candidates) based on ranks
5. Decile selection is configurable (e.g., quintiles = top/bottom 20%, tertiles = top/bottom 33%)
6. Edge case handling: if universe has fewer than 10 securities, function uses absolute thresholds or minimum counts
7. Output format clearly identifies long/short candidates with their ranks for each rebalance date
8. Unit tests validate ranking logic with synthetic data (verify top/bottom selections are correct)
9. Unit tests verify edge cases: all equal signals, mostly NaN signals, very small universes

### Story 2.3: Implement Equal-Weight Portfolio Construction

**As a** quantitative researcher,
**I want** to construct equal-weighted portfolios from long/short candidates with normalized exposure,
**so that** I can generate target portfolio weights for backtesting.

#### Acceptance Criteria

1. `src/portfolio/construction.py` module implements function `equal_weight_portfolio()` that accepts long/short candidates and returns weights
2. Long leg: Each selected security receives equal weight, normalized to 1.0 total long exposure (e.g., 50 longs → 2% each)
3. Short leg: Each selected security receives equal negative weight, normalized to -1.0 total short exposure (e.g., 50 shorts → -2% each)
4. Total portfolio has 2.0 gross exposure (1.0 long + 1.0 short) and 0.0 net exposure (market neutral)
5. Function handles edge cases: different numbers of longs vs shorts, empty long or short legs (returns zero weights)
6. Weights sum correctly within floating-point precision: sum(long_weights) ≈ 1.0, sum(short_weights) ≈ -1.0
7. Output format is a DataFrame with tickers as index, weights as values, suitable for backtest engine consumption
8. Function is pure and deterministic with configurable exposure targets (e.g., 1.5x long, 0.5x short)
9. Unit tests verify weight calculations for various portfolio sizes and validate sum constraints

### Story 2.4: Create Signal-to-Weights Pipeline Validation

**As a** quantitative researcher,
**I want** an end-to-end demonstration of the signal calculation → ranking → portfolio construction pipeline,
**so that** I can verify the complete strategy logic produces sensible portfolio weights.

#### Acceptance Criteria

1. Integration test or notebook (`notebooks/02_signal_portfolio_validation.ipynb`) demonstrates full signal-to-weights pipeline
2. Pipeline uses cached data from Epic 1 (e.g., S&P 500 constituents over 5+ years)
3. For each monthly rebalance date: calculate signals → rank → select deciles → construct equal-weight portfolio
4. Validation checks confirm: weights sum to zero (net neutral), gross exposure is 2.0, no individual weight exceeds reasonable threshold
5. Visualization shows time series of long/short counts (how many securities in each leg over time)
6. Visualization displays sample portfolio weights for 2-3 rebalance dates (top 10 longs, top 10 shorts)
7. Output saves portfolio weights to `results/` directory in CSV format for inspection
8. Documentation or notebook commentary explains the pipeline steps and validates outputs look reasonable
9. Pipeline completes for 5+ years of monthly rebalancing in under 30 seconds

## Epic 3: Backtest Engine & Performance Analytics

**Epic Goal:** Build the core backtesting engine that processes portfolio weights and price data to compute portfolio returns over time, implement comprehensive performance metrics calculation including CAGR, volatility, Sharpe ratio, maximum drawdown, and turnover, create publication-quality visualizations of equity curves and performance analytics, and deliver an end-to-end backtest demonstrating the complete V1 cross-sectional momentum strategy with validated results. This epic transforms portfolio weights into actionable performance insights.

### Story 3.1: Implement Portfolio Return Calculation Engine

**As a** quantitative researcher,
**I want** to calculate portfolio returns from target weights and historical price data,
**so that** I can measure strategy performance over time.

#### Acceptance Criteria

1. `src/backtest/engine.py` module implements function `calculate_portfolio_returns()` that accepts portfolio weights and price data, returns time series of portfolio returns
2. For each rebalance period: apply portfolio weights to subsequent period returns until next rebalance
3. Return calculation properly handles monthly rebalancing: weights set at month-end apply to next month's returns
4. Function computes both individual position returns and aggregated portfolio return for each period
5. Handling of rebalancing mechanics: assumes trades execute at rebalance date closing prices (no slippage for MVP)
6. Function handles missing price data: if a position has missing return data, it contributes zero return and logs a warning
7. Output includes period-by-period returns, cumulative portfolio value (starting from 1.0), and position-level attribution
8. Function is deterministic and uses vectorized operations for performance
9. Unit tests validate return calculations against hand-computed examples with known weights and returns
10. Unit tests verify edge cases: no rebalancing (static portfolio), monthly rebalancing, missing data handling

### Story 3.2: Implement Performance Metrics Calculation

**As a** quantitative researcher,
**I want** comprehensive performance metrics calculated from portfolio returns,
**so that** I can evaluate strategy quality and compare across variants.

#### Acceptance Criteria

1. `src/backtest/metrics.py` module implements performance metric functions
2. Function `calculate_cagr()` computes annualized return from cumulative portfolio value and time period
3. Function `calculate_volatility()` computes annualized standard deviation of returns
4. Function `calculate_sharpe_ratio()` computes risk-adjusted return (default risk-free rate = 0 or configurable)
5. Function `calculate_max_drawdown()` computes peak-to-trough maximum drawdown percentage and identifies drawdown periods
6. Function `calculate_turnover()` computes average monthly turnover (sum of absolute weight changes / 2)
7. Function `calculate_summary_stats()` aggregates all metrics into a single report: CAGR, volatility, Sharpe, max drawdown, turnover, number of periods
8. All functions handle edge cases: zero returns, negative cumulative values, insufficient data
9. Unit tests validate each metric against known benchmarks or hand-calculated examples
10. Metrics match common industry definitions (annualization using 12 periods/year for monthly data)

### Story 3.3: Create Performance Visualization Suite

**As a** quantitative researcher,
**I want** publication-quality visualizations of backtest results,
**so that** I can quickly assess strategy performance and communicate findings.

#### Acceptance Criteria

1. `src/backtest/visualization.py` module implements visualization functions using matplotlib/seaborn
2. Function `plot_equity_curve()` creates line chart of cumulative portfolio value over time with clear axis labels and title
3. Function `plot_drawdown()` creates area chart showing drawdown percentage over time, highlighting maximum drawdown period
4. Function `plot_monthly_returns()` creates heatmap or bar chart of monthly returns (optional: year-by-year breakdown)
5. Function `plot_performance_summary()` creates multi-panel figure combining equity curve, drawdown, and returns distribution
6. All visualizations follow consistent styling: colorblind-friendly colors, readable fonts, clear legends, professional appearance
7. Charts are configurable for save-to-file (PNG/PDF) or inline display in Jupyter notebooks
8. Function `generate_summary_table()` creates formatted text or DataFrame displaying key performance metrics
9. Visualizations handle long time series (10+ years) without overcrowding
10. Tests verify plots can be generated without errors (visual inspection for quality)

### Story 3.4: Build End-to-End Backtest Integration

**As a** quantitative researcher,
**I want** a complete end-to-end backtest running the V1 cross-sectional momentum strategy from data to results,
**so that** I can validate the framework produces accurate, reproducible performance analysis.

#### Acceptance Criteria

1. Integration test or notebook (`notebooks/03_full_backtest_v1.ipynb`) demonstrates complete backtest pipeline
2. Pipeline executes: load cached data → calculate signals → rank → construct portfolios → compute returns → calculate metrics → visualize results
3. Backtest runs on historical S&P 500 or Russell 1000 data covering at least 10 years (ideally 1990-2020+)
4. Results display equity curve showing cumulative performance over full period
5. Summary statistics report shows: CAGR, volatility, Sharpe ratio, max drawdown, average turnover
6. Performance metrics are within reasonable ranges for momentum strategies (e.g., Sharpe > 0, positive CAGR over long periods)
7. Backtest execution time meets NFR1: completes in under 1 minute for 30 years × 500 securities
8. Results are reproducible: running backtest twice with same parameters produces identical outputs
9. Output saves results to `results/backtest_v1/` directory: metrics CSV, equity curve CSV, visualization PNGs
10. Documentation explains how to run the backtest, interpret results, and modify parameters
11. Notebook includes commentary validating results look reasonable compared to academic literature on momentum

### Story 3.5: Implement Parameter Modification and Re-run Capability

**As a** quantitative researcher,
**I want** to easily modify strategy parameters and re-run backtests quickly,
**so that** I can explore robustness and test alternative momentum configurations.

#### Acceptance Criteria

1. Strategy configuration is externalized to a config dictionary or dataclass (not hardcoded in pipeline)
2. Config includes: lookback_months, skip_months, decile_selection (or quintile), rebalance_frequency, date_range, universe
3. Notebook or script (`notebooks/04_parameter_sweep.ipynb`) demonstrates modifying parameters and re-running
4. Parameter sweep example: test lookback periods of 3, 6, 9, 12 months and compare results side-by-side
5. Results comparison shows multiple equity curves overlaid on single chart
6. Summary table displays performance metrics for each parameter variant in rows
7. Parameter sweep for 10 variants completes in under 10 minutes (NFR9 requirement)
8. Clear documentation explains which parameters can be modified and their expected impact
9. Config validation ensures parameters are within reasonable ranges (e.g., lookback > skip)
10. Results are organized by parameter set for easy comparison: `results/sweep_lookback/` with subdirectories per variant

## Epic 4: Research Workflow & Experimentation Tools

**Epic Goal:** Create structured research notebook templates that guide systematic strategy exploration, implement experiment tracking to automatically log parameters and results, build comparison tools for analyzing multiple backtest variants, and produce comprehensive documentation enabling efficient use of the framework. This epic transforms the working backtest system into a research-ready platform optimized for learning and discovery.

### Story 4.1: Create Research Notebook Template Library

**As a** quantitative researcher,
**I want** structured Jupyter notebook templates for common research tasks,
**so that** I can document experiments consistently and avoid starting from scratch.

#### Acceptance Criteria

1. Template notebook `notebooks/templates/strategy_experiment_template.ipynb` provides structure for documenting a single strategy experiment
2. Template includes sections: Hypothesis, Parameters, Data/Universe, Signal Logic, Results, Insights, Next Steps
3. Template demonstrates loading data, running backtest, displaying results, and documenting findings with markdown commentary
4. Template notebook `notebooks/templates/parameter_robustness_template.ipynb` provides structure for parameter sweep experiments
5. Robustness template includes: parameter grid definition, loop over variants, results collection, comparative visualization
6. Template notebook `notebooks/templates/regime_analysis_template.ipynb` provides structure for analyzing strategy performance across different market regimes (bull/bear, high/low vol)
7. All templates include example code (using the framework modules) that can be copied and modified
8. Templates use consistent styling and markdown formatting for professional documentation
9. Documentation (`docs/research-workflow-guide.md`) explains when to use each template and how to customize them
10. Templates are saved in `notebooks/templates/` and excluded from research log tracking

### Story 4.2: Implement Automated Experiment Tracking

**As a** quantitative researcher,
**I want** experiments to automatically log parameters, results, and metadata,
**so that** I can track what I've tested without manual record-keeping.

#### Acceptance Criteria

1. `src/utils/experiment_tracker.py` module implements `ExperimentTracker` class for logging experiments
2. Tracker captures: experiment ID, timestamp, strategy config (parameters), performance metrics, data universe, notes
3. Function `log_experiment()` saves experiment metadata to structured format (JSON or SQLite) in `results/experiments/`
4. Function `load_experiment()` retrieves past experiment by ID for comparison or reproduction
5. Function `list_experiments()` displays summary table of all logged experiments with key metrics
6. Tracker automatically generates unique experiment IDs (e.g., timestamp-based or incremental)
7. Integration example in notebook shows wrapping backtest execution with tracker logging
8. Tracker handles concurrent experiments (no file locking issues if running multiple notebooks)
9. Unit tests verify tracker correctly saves and retrieves experiment metadata
10. Documentation explains how to use tracker in notebooks and query past experiments

### Story 4.3: Build Multi-Backtest Comparison Tools

**As a** quantitative researcher,
**I want** to compare multiple backtest results side-by-side with visualizations and statistics,
**so that** I can evaluate which strategy variants perform best.

#### Acceptance Criteria

1. `src/backtest/comparison.py` module implements comparison functions
2. Function `compare_equity_curves()` accepts multiple backtest results and plots overlaid equity curves with legend
3. Function `compare_metrics_table()` generates summary table with each variant as a row and metrics as columns
4. Function `compare_drawdowns()` plots multiple drawdown series overlaid for comparison
5. Function `compare_distributions()` creates histogram or violin plot comparing return distributions across variants
6. Comparison functions handle different date ranges gracefully (align to common periods or mark missing data)
7. Notebook example (`notebooks/05_strategy_comparison.ipynb`) demonstrates loading multiple experiment results and comparing them
8. Comparison visualizations support 2-10 variants without becoming unreadable
9. Export function saves comparison report (tables + charts) to PDF or HTML for sharing
10. Documentation explains how to interpret comparison outputs and make strategy selection decisions

### Story 4.4: Create Comprehensive Framework Documentation

**As a** developer or researcher,
**I want** clear documentation explaining the framework architecture, module APIs, and research workflow,
**so that** I can use the system effectively and extend it for new strategies.

#### Acceptance Criteria

1. `README.md` provides: project overview, quick start guide, installation instructions, basic usage example
2. `docs/architecture-overview.md` documents the layered architecture (Data/Signal/Portfolio/Backtest/Risk) with module responsibilities
3. `docs/api-reference.md` provides function signatures and docstrings for key modules: signals, portfolio, backtest, metrics
4. `docs/research-workflow-guide.md` explains recommended workflow: data setup → signal testing → backtest → analysis → documentation
5. `docs/extending-strategies.md` explains how to add new signal types or portfolio construction methods
6. `docs/troubleshooting.md` covers common issues: Norgate connection errors, data quality problems, performance bottlenecks
7. All public functions in `src/` modules include docstrings with: description, parameters, returns, examples
8. Documentation includes example code snippets that are tested/verified to work
9. `docs/research-log.md` template is populated with guidance on how to maintain the research log
10. Documentation is well-organized, easy to navigate, and suitable for onboarding a new user

### Story 4.5: Validate Complete Research Workflow End-to-End

**As a** quantitative researcher,
**I want** to execute a complete research workflow from initial hypothesis through multiple experiments to final analysis,
**so that** I can validate the framework supports systematic strategy exploration.

#### Acceptance Criteria

1. End-to-end validation notebook (`notebooks/06_complete_research_workflow.ipynb`) demonstrates full research cycle
2. Workflow starts with hypothesis: "Does shorter lookback improve Sharpe ratio?"
3. Notebook uses strategy experiment template to document the hypothesis and approach
4. Multiple experiments are run with different lookback periods (3, 6, 9, 12 months) using experiment tracker
5. Results are compared using multi-backtest comparison tools showing equity curves and metrics table
6. Insights are documented in markdown: which lookback performed best, why, trade-offs observed
7. Research log (`docs/research-log.md`) is updated with summary entry for this investigation
8. Entire workflow from hypothesis to documented insights takes under 30 minutes to execute
9. Workflow demonstrates reproducibility: re-running notebook produces identical results
10. Documentation or notebook commentary explains each step and how it demonstrates the framework's research capabilities
11. Validation confirms all Epic 4 tools work together cohesively

## Checklist Results Report

### Executive Summary

**Overall PRD Completeness:** 81% (Strong PASS)

**MVP Scope Appropriateness:** ✅ **Just Right** - Focused on single strategy variant with clear learning objectives and appropriate complexity deferral.

**Readiness for Architecture Phase:** ✅ **READY** - Sufficient technical guidance, clear requirements, comprehensive epic structure.

**Most Critical Observations:**
- Excellent epic/story structure with logical sequencing and appropriate sizing
- Strong technical foundation with clear architectural principles
- Minor improvements recommended: timeline, quantitative success metrics, visual diagrams

### Category Analysis

| Category                         | Status    | Critical Issues                                                               |
| -------------------------------- | --------- | ----------------------------------------------------------------------------- |
| 1. Problem Definition & Context  | PARTIAL   | No quantitative KPIs; missing explicit timeline                               |
| 2. MVP Scope Definition          | PARTIAL   | No consolidated "Post-MVP" section; MVP success criteria could be clearer     |
| 3. User Experience Requirements  | PASS      | Minor: No explicit error handling UX guidance                                 |
| 4. Functional Requirements       | PASS      | Minor: Feature dependencies not explicitly stated in FR section               |
| 5. Non-Functional Requirements   | PARTIAL   | Some operational NFRs undefined (monitoring, alerting) - acceptable for MVP   |
| 6. Epic & Story Structure        | PASS      | Excellent structure, clear sequencing, appropriate sizing                     |
| 7. Technical Guidance            | PASS      | Strong architecture direction; minor: no explicit technical risk callouts     |
| 8. Cross-Functional Requirements | PARTIAL   | Some operational requirements undefined (acceptable for personal MVP)         |
| 9. Clarity & Communication       | PASS      | Well-written; would benefit from architecture/flow diagrams                   |

### Key Strengths

1. **Excellent Epic/Story Breakdown**
   - Clear sequential flow with logical dependencies
   - Stories sized appropriately for AI agent execution ("2-4 hour" units)
   - Each epic delivers testable, incremental value
   - Comprehensive acceptance criteria

2. **Strong Technical Foundation**
   - Clear architectural principles (layered design, pure functions, composability)
   - Well-justified technology choices (Python, pandas, uv, Norgate)
   - Performance targets specified (NFR1, NFR9)
   - Appropriate emphasis on reproducibility and correctness

3. **Appropriate MVP Scope**
   - Single strategy focus (12-1 cross-sectional momentum)
   - Clear deferral of complexity (transaction costs, time-series variants)
   - Balance between learning objectives and practical outcomes

4. **Research-Focused Design**
   - Epic 4 dedicated to experimentation workflow
   - Emphasis on documentation and reproducibility
   - Jupyter notebook integration central to UX

### Recommendations for Improvement

#### Optional Enhancements (Non-Blocking)

1. **Add Success Metrics Section**
   ```markdown
   ## Success Metrics
   - Complete 10+ backtest experiments within first 3 months of usage
   - Parameter modification to new backtest in <5 minutes (FR9)
   - Backtest performance: Sharpe ratio > 0.5 on historical S&P 500 data
   - Framework extensibility: Add new signal type in <2 hours
   ```

2. **Add Timeline/Milestones**
   - Estimated effort: 18-20 stories at 1 story/day = 4-5 weeks full-time
   - Suggest phased approach if desired

3. **Create Architecture Diagram** (can be done during architecture phase)
   - Layered architecture visualization
   - Data flow: Norgate → Parquet → Signals → Portfolio → Backtest → Results

4. **Consolidate Post-MVP Features**
   ```markdown
   ## Post-MVP Roadmap
   - Transaction costs and slippage modeling
   - Time-series momentum strategies
   - Rank-weighted portfolio construction
   - Sector neutrality
   - Real-time paper trading
   ```

### Final Assessment

✅ **READY FOR ARCHITECT**

The PRD provides comprehensive, well-structured guidance for architectural design. The epic/story breakdown is exemplary with clear sequencing, appropriate sizing, and detailed acceptance criteria. Technical assumptions are well-documented, and the MVP scope appropriately balances learning objectives with practical outcomes.

**Confidence Level:** High - This PRD demonstrates thorough product thinking and is ready for the next phase.

## Next Steps

### UX Expert Prompt

The portfolio-momentum framework is a code-first research environment, so traditional UI/UX design is minimal. However, the "user experience" centers on Jupyter notebook workflows and data visualization. If UX architecture is needed, use this prompt:

---

**UX/Design Expert - Create UI/UX Architecture**

Using the attached Product Requirements Document (PRD) for the **portfolio-momentum** research framework, please create a comprehensive UI/UX architecture focused on the Jupyter notebook-based research workflow.

**Context:**
This is not a traditional GUI application - it's a Python research framework where users interact through Jupyter notebooks, visualizations, and markdown documentation. The "UX" is the research workflow experience.

**Key Focus Areas:**

1. **Research Workflow Design**
   - Map out the user journey from hypothesis → experiment → analysis → insights
   - Define notebook template structures (already outlined in Epic 4, Story 4.1)
   - Design visual language for charts (matplotlib/seaborn styling guidelines)

2. **Visualization Standards**
   - Define consistent chart styling (colors, fonts, layouts) for publication-quality outputs
   - Create examples of equity curves, drawdown charts, performance comparisons
   - Ensure colorblind-friendly palettes

3. **Information Architecture**
   - Document directory structure and file organization
   - Design research log structure (markdown format)
   - Define naming conventions for experiments and results

4. **Interaction Patterns**
   - Define configuration patterns (dataclasses vs dicts for strategy parameters)
   - Design error message and logging patterns
   - Specify how users navigate between data exploration, backtesting, and comparison

**Deliverables:**
- Research workflow diagram (user journey from hypothesis to insights)
- Visualization style guide (chart templates, color schemes, typography)
- Notebook template wireframes (showing structure and interaction patterns)
- File organization and naming conventions guide

**Reference PRD Sections:**
- User Interface Design Goals (code-first research environment vision)
- Epic 4: Research Workflow & Experimentation Tools
- Technical Assumptions (Jupyter notebooks, matplotlib/seaborn/plotly)

---

### Architect Prompt

**Software Architect - Create Technical Architecture**

Using the attached Product Requirements Document (PRD) for the **portfolio-momentum** quantitative research framework, please create a comprehensive technical architecture document that will guide development.

**Project Overview:**
A modular Python framework for researching and backtesting momentum trading strategies, starting with V1 cross-sectional momentum (12-1 Jegadeesh & Titman). The framework emphasizes learning through implementation, reproducibility, and extensibility.

**Your Task:**
Design the complete technical architecture covering:

1. **System Architecture**
   - Detailed layered architecture design (Data, Signal, Portfolio, Backtest, Risk layers)
   - Module responsibilities and interfaces between layers
   - Data flow from Norgate API → cached Parquet → signals → portfolio weights → backtest results
   - Dependency injection and composition patterns for extensibility

2. **Data Architecture**
   - Pandas DataFrame structures for price data, signals, portfolio weights, returns
   - Parquet file organization and naming conventions for caching
   - Handling of point-in-time constituents and corporate actions
   - Data validation pipeline design

3. **Key Module Design**
   - **Data Layer:** Norgate API integration, caching strategy, validation pipeline
   - **Signal Layer:** Pure function design for momentum calculations, ranking, selection
   - **Portfolio Layer:** Weight calculation, exposure normalization, rebalancing logic
   - **Backtest Layer:** Return calculation engine, performance metrics, visualization suite
   - **Utils Layer:** Experiment tracking, configuration management, logging

4. **Testing Strategy**
   - Unit test approach for pure functions (signal calculations, portfolio construction)
   - Integration test design for end-to-end backtests
   - Validation test approach (compare against known benchmarks)
   - Test data strategies (synthetic data, fixtures)

5. **Performance Optimization**
   - Pandas/numpy vectorization patterns to meet NFR1 (<1 min for 30yr × 500 securities)
   - Parquet caching strategy for fast iteration
   - Memory management for large datasets
   - Profiling and optimization approach

6. **Configuration & Extensibility**
   - Strategy configuration design (dataclasses, YAML, or dict-based)
   - Plugin architecture for new signal types
   - Template pattern for portfolio construction methods
   - Adding new performance metrics

7. **Error Handling & Logging**
   - Exception handling patterns (data quality issues, missing API credentials, calculation errors)
   - Logging strategy (Python logging module configuration)
   - User-facing error messages in notebooks

8. **Development Workflow**
   - Package structure enabling `import src` from project root
   - uv (Astral) dependency management setup
   - pytest configuration and test discovery
   - Code quality tools (ruff/pylint configuration)

**Critical Requirements to Address:**
- **NFR1:** Backtest performance <1 minute for 30 years × 500 securities
- **NFR2:** Clear separation of concerns across layers
- **NFR3:** Extensibility - new strategies without modifying core engine
- **NFR4:** Pure functions for reproducibility (deterministic, no side effects)
- **NFR7:** Offline operation with cached data
- **NFR8:** Survivorship bias elimination via point-in-time constituents

**Key Technical Decisions Needed:**
1. Pandas DataFrame index design (datetime index? MultiIndex for tickers × dates?)
2. Parquet file organization (single file vs sharded? by date range? by universe?)
3. Configuration approach (dataclass vs YAML vs dict) - recommend with rationale
4. Experiment tracking storage (JSON files vs SQLite) - recommend with rationale
5. Pure function enforcement (static type checking? runtime validation?)

**Deliverables:**
1. **Architecture Overview Document** with layered architecture diagram
2. **Module Design Specifications** for each layer (Data, Signal, Portfolio, Backtest, Utils)
3. **Data Structures & Schemas** (DataFrame formats, Parquet organization, config schemas)
4. **API/Interface Definitions** (function signatures for key modules with docstring examples)
5. **Technical Decision Log** (rationale for key architecture choices)
6. **Development Setup Guide** (package structure, dependency management, testing configuration)

**Reference PRD Sections:**
- Technical Assumptions (repository structure, architecture, tech stack, performance targets)
- All Epic/Story Acceptance Criteria (especially Epic 1 for data infrastructure)
- Requirements (FR1-FR13, NFR1-NFR10)

**Note:** This is a personal research project, so avoid over-engineering. Prioritize clarity, simplicity, and extensibility over enterprise-scale patterns. The architecture should support learning and experimentation.
