# Technical Considerations

These represent initial technical thoughts and preferences. Final technology decisions will be made during implementation based on practical experience and emerging requirements.

## Platform Requirements

- **Target Platforms:** Linux/macOS for primary development; Windows compatibility desirable but not required for MVP
- **Computing Environment:** Local development on personal machine for MVP; potential cloud deployment (AWS/GCP) for paper trading and live operations in later stages
- **Performance Requirements:**
  - Backtest execution for 30+ years of monthly data across 500+ securities should complete in under 1 minute
  - Parameter sweep testing (10+ variants) should complete in under 10 minutes
  - Research notebook operations should be interactive (sub-second response for data exploration)

## Technology Preferences

- **Primary Language:** Python 3.10+ (standard for quantitative finance, rich ecosystem for data analysis and backtesting)

- **Core Data Stack:**
  - **pandas** for time series manipulation and tabular data operations
  - **numpy** for numerical computations and array operations
  - **scipy/statsmodels** for statistical analysis and performance metrics

- **Visualization & Analysis:**
  - **matplotlib/seaborn** for equity curves, performance charts, distribution plots
  - **Jupyter notebooks** for interactive research and experimentation
  - **plotly** (optional, later) for interactive dashboards

- **Data Sources & Storage:**
  - **Primary data source:** Norgate Data (Platinum US Stocks subscription)
    - Historical data from 1990+ (30+ years of coverage across multiple market regimes)
    - Point-in-time index constituents (eliminates look-ahead bias)
    - Delisting data (eliminates survivorship bias)
    - Adjusted prices for splits/dividends
    - Access via `norgatedata` Python package
  - **Data format:** Query Norgate on-demand or cache to Parquet files for faster iteration
  - **Universe definition:** Can use historical S&P 500 constituents, Russell 1000, or custom filters
  - **Later expansion:** Additional data sources for ETFs, international equities, or futures if needed

- **Backtesting & Quantitative Libraries:**
  - **Custom-built backtest engine** (core requirement for learning and control)
  - **Potential integration:** zipline, backtrader, or vectorbt for comparison/validation (not dependencies)

- **Development Tools:**
  - **Version control:** Git (already in use based on repo structure)
  - **Dependency management:** pip + requirements.txt or poetry for reproducible environments
  - **Code quality:** Basic linting (ruff/pylint), type hints where helpful
  - **Testing:** pytest for unit tests of signal functions and portfolio construction logic

## Architecture Considerations

- **Repository Structure:**
  ```
  portfolio-momentum/
  ├── data/               # Cached price data if needed (gitignored)
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

- **Design Principles:**
  - **Separation of concerns:** Each layer (Data/Signal/Portfolio/Backtest/Risk) is independently testable
  - **Pure functions:** Signal calculations have no side effects, deterministic outputs
  - **Data pipelines:** Clear flow from Norgate → cleaned data → signals → weights → performance
  - **Composability:** Mix and match signals, portfolio construction methods, risk overlays
  - **Survivorship bias awareness:** Leverage Norgate's historical constituents to ensure backtest integrity

- **Integration Requirements:**
  - **Norgate Data integration:** norgatedata package for accessing historical prices and index memberships
  - **Offline capability:** Option to cache Norgate data locally for reproducible backtests
  - **Export capabilities:** Results exportable to CSV/JSON for external analysis or sharing

- **Security & Compliance:**
  - **No PII or sensitive data:** Framework handles only public market data
  - **Norgate credentials:** Store license/credentials securely (environment variables or gitignored config)
  - **Code security:** Standard practices for dependency management, no execution of untrusted code
  - **Financial compliance:** This is personal research/trading; no regulatory requirements for MVP
  - **Risk disclosure:** Clear documentation that this is experimental, not financial advice
