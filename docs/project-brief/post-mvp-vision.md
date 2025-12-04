# Post-MVP Vision

## Phase 2 Features

After MVP demonstrates V1 cross-sectional momentum works end-to-end, the next phase focuses on **making the framework reusable and adding sophistication**:

**Framework Generalization (Stage 3):**
- Parameterize backtest engine to accept arbitrary signal and weight functions
- Expose tunable parameters: lookback length (3/6/12 months), skip-month on/off, decile vs quintile selection, equal-weight vs rank-weight
- Add transaction cost modeling (fixed bps per trade × turnover) with configurable cost assumptions
- Build reporting utilities: monthly return distributions, rolling performance windows, drawdown analysis
- Implement parameter sweep infrastructure for systematic robustness testing

**Time-Series Momentum Implementation (Stage 4):**
- TSMOM signal function: sign-based positioning (+1 if 12-month return > 0, -1 otherwise)
- Volatility scaling module: estimate realized volatility and size positions inversely to vol
- Support simplified universe (ETF proxies for futures across asset classes)
- Generate comparative analysis: cross-sectional vs time-series performance, correlation, drawdown offset
- Demonstrate architecture reusability by plugging TSMOM into existing framework

**Basic Transaction Costs & Risk Controls:**
- Apply cost model to backtests and compare gross vs net performance
- Implement simple position limits (max % per security)
- Add basic leverage constraint checking
- Build turnover tracking and reporting

## Long-Term Vision

**A comprehensive "momentum lab"** where you can:

- Rapidly test any momentum-based strategy idea (cross-sectional, time-series, dual momentum, combinations)
- Understand strategy behavior through systematic exploration: parameter sensitivity, regime analysis, correlation structure
- Validate strategies through multi-stage progression: backtest → robustness checks → paper trading → selective live deployment
- Build institutional knowledge via research notebook documenting what works, what doesn't, and why
- Deploy multiple low-correlation momentum strategies simultaneously with portfolio-level risk management
- Operate confidently with real capital based on thoroughly validated, well-understood strategies

**The framework becomes your personal quantitative research platform**—optimized for depth in momentum strategies rather than breadth across all possible approaches.

## Expansion Opportunities

**Strategy Variants (Stage 5):**
- Cross-sectional variants: different lookbacks (3/6/12 months), overlapping J/K portfolios, rank/volatility weighting
- Time-series variants: multi-horizon blends (1/3/12 month average), different rebalancing frequencies
- Dual momentum: Antonacci-style relative + absolute momentum with defensive asset allocation
- ETF rotation: top-N momentum-selected ETFs, long-only with monthly rebalancing
- Combined strategies: cross-sectional + time-series overlay, multi-strategy portfolio allocation

**Production Capabilities (Stage 6):**
- Automated paper trading: daily signal generation, position tracking, performance attribution
- Live data integration: real-time price feeds for signal calculation
- Operational risk controls: max drawdown triggers, volatility targeting at portfolio level
- Portfolio construction across multiple strategies: correlation-aware allocation, risk parity weighting
- Performance monitoring dashboard: track live vs backtest, regime detection, alert systems

**Advanced Research Tools:**
- Factor exposure analysis: regression against market, size, value factors
- Regime classification: identify bull/bear, high/low vol periods and analyze strategy behavior
- Monte Carlo simulation for drawdown and return distribution estimation
- Walk-forward optimization frameworks
- Strategy stress testing against historical crises
