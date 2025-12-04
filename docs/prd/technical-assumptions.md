# Technical Assumptions

## Repository Structure

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

## Service Architecture

**Monolithic Python Package** - The framework is structured as a single Python package with modular internal architecture following the layered design pattern (Data → Signal → Portfolio → Backtest → Risk). Each layer is implemented as a separate subpackage with well-defined interfaces.

**Rationale:** For a research framework processing batch computations locally, a monolithic architecture is simpler and more appropriate than microservices. The modular internal structure provides the necessary separation of concerns without distributed systems complexity.

**Key Architectural Principles:**
- **Separation of concerns:** Each layer is independently testable
- **Pure functions:** Signal calculations are deterministic with no side effects
- **Composability:** Mix and match signals, portfolio construction methods, and risk overlays
- **Data pipeline flow:** Clear progression from Norgate → cleaned data → signals → weights → performance

## Strategy Implementation Methodology

**Baseline Strategy: Jegadeesh & Titman (1993) Cross-Sectional Momentum**

The MVP implementation replicates the classic academic momentum strategy with the following design choices:

**Signal Calculation:**
- **12-1 Momentum:** Cumulative return from t-12 months to t-2 months (skip most recent month)
- **Rationale:** Skip-month avoids short-term reversal effects documented in literature

**Portfolio Construction:**
- **Selection:** Top decile (10%) long, bottom decile (10%) short
- **Weighting:** Equal-weight within each leg (normalized to 1x exposure per leg, 2x gross, 0 net)
- **Overlapping Portfolios:** K=6 month holding period with monthly formation
  - At each rebalance date t, maintain K active sub-portfolios (formed at months t, t-1, ..., t-K+1)
  - Final portfolio = equal-weighted average of all K active sub-portfolios
  - **Turnover impact:** ~17% monthly (1/K) vs 100% for simple monthly rebalance
  - **Default K=6:** Matches typical J&T implementation, balances signal freshness vs transaction costs
  - **Configurable:** Support K=1 (no overlap), K=3, K=12 for experimentation

**Rebalancing:**
- **Frequency:** Monthly (end-of-month)
- **Universe refresh:** Point-in-time constituents retrieved each month from Norgate

**Bias Elimination:**
- **Survivorship bias:** Norgate "Current & Past" watchlists include delisted securities
- **Look-ahead bias:** Point-in-time universe construction ensures only historically available stocks are candidates
- **Data snooping:** Implementation follows published academic methodology exactly

**Rationale:** This methodology exactly replicates the academic baseline, enabling direct comparison to published results. The overlapping portfolio mechanism is critical for matching J&T performance characteristics and transaction cost profiles.

## Testing Requirements

**Unit + Integration Testing** focused on correctness and reproducibility:

- **Unit tests:** pytest-based tests for signal calculation functions, portfolio construction logic, and performance metric calculations
- **Validation tests:** Compare backtest results against known benchmarks or academic paper results where possible
- **Data quality tests:** Validate Norgate data loading, corporate action handling, and survivorship bias elimination
- **Integration tests:** End-to-end backtest runs with fixed seeds/data to ensure reproducibility
- **Test coverage target:** Priority on critical calculation paths (signals, returns, metrics) rather than 100% coverage

**Rationale:** For a research framework, correctness is paramount. Unit tests ensure signal calculations are bug-free, while integration tests validate the full pipeline produces reproducible results. Manual testing in Jupyter notebooks will supplement automated tests for exploratory analysis.

## Additional Technical Assumptions and Requests

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
- **Universe definition:**
  - **Default:** Russell 1000 Current & Past (~1000 large/mid-cap stocks)
  - **Rationale:** Matches Jegadeesh & Titman (1993) universe size and market-cap range, implicitly excludes micro-cap liquidity/cost issues
  - **Configurable:** Can switch to Russell 3000 C&P for small-cap momentum experiments
  - **Minimum history requirement:** ≥12 months of price data required for inclusion in backtest universe at any given time

**Development Tools:**
- **Version control:** Git (already in use)
- **Dependency management:** uv (Astral) for fast, reliable Python package management
- **Code quality:** ruff or pylint for linting, type hints where beneficial
- **Testing framework:** pytest for all automated tests

**Security & Configuration:**
- **Norgate credentials:** Pre-configured in NDU Windows application; Python code accesses NDU via Windows Python bridge without handling credentials directly
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
