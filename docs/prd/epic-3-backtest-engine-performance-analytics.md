# Epic 3: Backtest Engine & Performance Analytics

**Epic Goal:** Build the core backtesting engine that processes portfolio weights and price data to compute portfolio returns over time, implement comprehensive performance metrics calculation including CAGR, volatility, Sharpe ratio, maximum drawdown, and turnover, create publication-quality visualizations of equity curves and performance analytics, and deliver an end-to-end backtest demonstrating the complete V1 cross-sectional momentum strategy with validated results. This epic transforms portfolio weights into actionable performance insights.

## Story 3.1: Implement Portfolio Return Calculation Engine

**As a** quantitative researcher,
**I want** to calculate portfolio returns from target weights and historical price data,
**so that** I can measure strategy performance over time.

### Acceptance Criteria

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

## Story 3.2: Implement Performance Metrics Calculation

**As a** quantitative researcher,
**I want** comprehensive performance metrics calculated from portfolio returns,
**so that** I can evaluate strategy quality and compare across variants.

### Acceptance Criteria

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

## Story 3.3: Create Performance Visualization Suite

**As a** quantitative researcher,
**I want** publication-quality visualizations of backtest results,
**so that** I can quickly assess strategy performance and communicate findings.

### Acceptance Criteria

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

## Story 3.4: Build End-to-End Backtest Integration

**As a** quantitative researcher,
**I want** a complete end-to-end backtest running the V1 cross-sectional momentum strategy from data to results,
**so that** I can validate the framework produces accurate, reproducible performance analysis.

### Acceptance Criteria

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

## Story 3.5: Implement Parameter Modification and Re-run Capability

**As a** quantitative researcher,
**I want** to easily modify strategy parameters and re-run backtests quickly,
**so that** I can explore robustness and test alternative momentum configurations.

### Acceptance Criteria

1. Strategy configuration is externalized to a config dictionary or dataclass (not hardcoded in pipeline)
2. Config includes: lookback_months, skip_months, holding_months (K for overlapping portfolios), decile_selection (or quintile), rebalance_frequency, date_range, universe
3. Notebook or script (`notebooks/04_parameter_sweep.ipynb`) demonstrates modifying parameters and re-running
4. Parameter sweep examples: test lookback periods of 3, 6, 9, 12 months OR holding periods K=1, 3, 6, 12 and compare results side-by-side
5. Results comparison shows multiple equity curves overlaid on single chart
6. Summary table displays performance metrics for each parameter variant in rows
7. Parameter sweep for 10 variants completes in under 10 minutes (NFR9 requirement)
8. Clear documentation explains which parameters can be modified and their expected impact
9. Config validation ensures parameters are within reasonable ranges (e.g., lookback > skip)
10. Results are organized by parameter set for easy comparison: `results/sweep_lookback/` with subdirectories per variant
