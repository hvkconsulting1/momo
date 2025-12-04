# Risks & Open Questions

## Key Risks

- **Strategy Decay:** Momentum effects may have weakened over time due to increased competition/capital pursuing these strategies. Risk that backtested performance significantly exceeds achievable live performance even with proper execution.

- **Implementation Errors:** Risk of bugs in signal calculation, portfolio construction, or backtest engine that produce misleading results. Without external validation, subtle errors could go undetected and lead to false confidence.

- **Market Regime Change:** Historical backtests may not predict future performance if market structure has fundamentally changed (e.g., algorithmic trading dominance, different correlation structures, policy regime shifts).

- **Transaction Costs Underestimated:** Initial simple cost models (fixed bps) may not capture real-world costs including market impact, short borrow costs, funding costs for leverage, and slippage during volatile periods.

- **Execution Challenges:** Difference between backtest assumptions and live execution reality—liquidity constraints, inability to short certain securities, extreme market conditions affecting fills.

- **Momentum Crashes:** Known phenomenon where momentum strategies can experience severe, rapid drawdowns (especially during market reversals). Risk that live trading coincides with crash period, leading to significant losses and psychological difficulty maintaining the strategy.

- **Time Commitment Sustainability:** Risk that other priorities reduce available time for the project, leading to incomplete implementation or inability to monitor live strategies adequately.

- **Overfitting Through Iteration:** Risk of unconsciously fitting strategy parameters to historical data through repeated testing and refinement, leading to overstated expected performance.

- **Capital Inadequacy:** Even with strategies ready, may not have sufficient capital to deploy at scale where transaction costs are reasonable and diversification is adequate.

## Open Questions

- **Universe Selection:** Should MVP use S&P 500 constituents, Russell 1000, top N by market cap, or some other universe definition? What's the trade-off between universe size and data quality/liquidity?

- **Rebalancing Day:** Should rebalancing happen on fixed day of month (e.g., last trading day) or relative to signal formation date? Does timing within month materially affect results?

- **Signal Calculation Details:** For 12-1 momentum, should the return calculation use close-to-close monthly returns or specific calendar dates? How to handle partial months at data boundaries?

- **Portfolio Sizing:** Beyond equal-weight within deciles, should some weighting by liquidity/market cap be considered even for MVP to be more realistic?

- **Transaction Cost Model:** What's a reasonable estimate for all-in transaction costs (commission + spread + impact) for monthly rebalancing of liquid large-caps? 10bps? 25bps? 50bps?

- **Short Selling Realism:** Are there systematic differences in shorting costs between high vs low momentum stocks that should be modeled? Should MVP assume symmetric long/short costs or add complexity?

- **Benchmark Selection:** What's the right benchmark for evaluating performance—market-neutral zero return, S&P 500, or something else?

- **Data Caching Strategy:** Should Norgate data be cached to local files for reproducibility and speed, or always queried fresh to ensure latest adjustments/delistings are captured?

- **Testing Strategy:** What's the minimum test coverage required for confidence in backtest engine? How to validate signal calculations against known results?

- **Parameter Space:** Beyond 12-1 momentum, what parameter combinations are worth testing in robustness checks (3/6/9/12 month lookbacks, 0/1/2 month skips, decile vs quintile)?

## Areas Needing Further Research

- **Academic Literature Deep Dive:** Need to read original Jegadeesh & Titman (1993) paper carefully and compare their exact methodology to proposed implementation—ensure no critical details are missed.

- **Recent Momentum Research:** Review post-2010 momentum literature for insights on implementation details, common pitfalls, and recent findings about strategy evolution.

- **Crisis Period Behavior:** Study how cross-sectional momentum behaved during 2000 tech crash, 2008 financial crisis, 2020 COVID crash to set realistic expectations for drawdowns.

- **Norgate Data API:** Learn norgatedata package API thoroughly—how to query historical constituents, handle delistings, retrieve adjusted prices, optimize query patterns.

- **Backtest Engine Design Patterns:** Research best practices for building backtest engines—common pitfalls like look-ahead bias, proper handling of corporate actions, vectorized computation approaches.

- **Cost Models:** Research realistic transaction cost estimates for equity momentum strategies—look for practitioner literature or broker cost structures.

- **Python Performance Optimization:** If backtest performance becomes bottleneck, need to research pandas optimization, numpy vectorization, or potential use of numba/Cython.

- **Risk Management Frameworks:** Study approaches to position sizing, volatility targeting, and drawdown-based de-risking used in practitioner implementations.
