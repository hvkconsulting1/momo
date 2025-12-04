# Requirements

## Functional

**FR1:** The system shall ingest historical price data (OHLCV) from Norgate Data for a defined equity universe with adjustments for splits, dividends, and delistings

**FR2:** The system shall calculate cross-sectional momentum signals using the 12-1 methodology (cumulative return from t-12 to t-2 months)

**FR3:** The system shall rank securities based on momentum signals and construct portfolios using decile-based selection (top 10% long, bottom 10% short)

**FR4:** The system shall apply equal-weight allocation within each portfolio leg using overlapping portfolios with K-month holding periods (default K=6), normalized to 1x gross exposure per leg (2x total gross, 0 net)

**FR5:** The system shall execute backtests computing monthly returns, cumulative portfolio value, CAGR, volatility, Sharpe ratio, maximum drawdown, and monthly turnover

**FR6:** The system shall generate equity curve visualizations and summary statistics tables from backtest results

**FR7:** The system shall construct point-in-time investable universes using index constituent time series from Norgate Data (default: Russell 1000 Current & Past) with minimum 12-month history requirement to eliminate both survivorship bias and look-ahead bias in backtests

**FR8:** The system shall validate data quality including checks for missing prices, adjustment factors, and delisting events

**FR9:** The system shall support modification of strategy parameters (lookback periods, decile vs quintile selection, skip months, holding period K) and re-run backtests in under 5 minutes

**FR10:** The system shall provide a research notebook structure for documenting experiments with date, hypothesis, parameters, results, and insights

**FR11:** The system shall expose composable signal and portfolio construction functions that can be combined independently

**FR12:** The system shall cache Norgate data locally to Parquet files for reproducible backtests and faster iteration

**FR13:** The system shall export backtest results to standard formats (CSV/JSON) for external analysis

## Non Functional

**NFR1:** Backtest execution for 30+ years of monthly data across 500+ securities must complete in under 1 minute

**NFR2:** The architecture must maintain clear separation of concerns across Data, Signal, Portfolio Construction, Backtest, and Risk layers

**NFR3:** Adding new momentum strategy variants (time-series, dual momentum) must not require changes to the backtest engine or data layer

**NFR4:** Signal calculation functions must be pure (deterministic, no side effects) to ensure reproducible results

**NFR5:** The codebase must remain comprehensible and maintainable with clear interfaces between modules

**NFR6:** Unit tests must cover signal calculations and portfolio construction logic (including overlapping portfolio mechanics) with validation against known results

**NFR7:** The system must support offline operation with locally cached Norgate data for reproducible backtests

**NFR8:** Data ingestion must leverage Norgate's survivorship-bias-free historical constituents to ensure backtest integrity

**NFR9:** Parameter sweep testing (10+ variants) must complete in under 10 minutes to support robustness analysis

**NFR10:** The system must handle corporate actions (splits, dividends, delistings) without manual intervention
