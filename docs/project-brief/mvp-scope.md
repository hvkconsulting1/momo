# MVP Scope

The MVP focuses on building **Strategy V1 (Classic 12-1 Cross-Sectional Momentum)** with a working backtest engine and foundational architecture—proving the core concept works before expanding to additional strategies.

## Core Features (Must Have)

- **Strategy V1 Specification Document:** Written markdown specification (`docs/strategy-v1-jegadeesh-cross-sectional.md`) that defines exact formulas for 12-1 momentum signal, ranking/selection rules, weighting approach, rebalancing logic, and initial backtest assumptions

- **Data Ingestion Module:** Code to load and normalize monthly price data for a defined equity universe (e.g., top 500 stocks by market cap), handling adjustments for splits/dividends, with simple data validation and quality checks

- **Cross-Sectional Momentum Signal Function:** Implementation of 12-1 momentum calculation (cumulative return from t-12 to t-2 for each asset at each month t), producing a clean signal matrix

- **Portfolio Construction Module:** Ranking logic that selects top decile (top 10%, long) and bottom decile (bottom 10%, short) based on momentum signals, with equal-weight allocation within each leg, normalized to 1x gross exposure per leg (2x total, 0 net)

- **Minimal Backtest Engine:** Generic backtesting framework that takes weights and prices, computes monthly returns, tracks cumulative portfolio value, and calculates core statistics: CAGR, volatility, Sharpe ratio, max drawdown, and monthly turnover

- **Performance Visualization:** Basic equity curve plot and summary statistics table that can be generated from backtest results (can use simple matplotlib/similar tools)

- **Research Notebook Setup:** Initial markdown-based research log structure for documenting experiments, with template for recording: date, hypothesis tested, parameters used, results, and key insights

## Out of Scope for MVP

- Time-series momentum (TSMOM) strategies
- Dual momentum or ETF rotation variants
- Overlapping J/K portfolio implementation
- Transaction cost modeling (compute turnover but don't apply costs yet)
- Volatility targeting or dynamic position sizing
- Risk overlays or drawdown-based de-risking
- Rank-weighting (equal-weight only for MVP)
- Value-weighting by market cap
- Sector neutrality or factor exposure controls
- Multiple universe support (focus on single equity universe)
- Paper trading automation or live data feeds
- Comprehensive parameter sweep infrastructure
- Factor regression analysis
- Web interface or dashboard
- Database storage (flat files acceptable for MVP)

## MVP Success Criteria

**The MVP is considered successful when:**

1. You can explain the V1 cross-sectional momentum strategy from first principles and have a written specification document
2. The backtest engine produces a complete equity curve for V1 strategy over 10+ years of historical data
3. Backtest statistics are reasonable (positive Sharpe ratio, drawdown characteristics consistent with momentum literature)
4. The code architecture clearly separates Data, Signal, Portfolio Construction, and Backtest layers
5. You can modify a parameter (e.g., top/bottom quintile instead of decile) and re-run the backtest in under 5 minutes
6. Performance metrics and equity curve can be generated and saved for comparison
7. First research notebook entry is complete documenting the V1 baseline implementation
