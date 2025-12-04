# Constraints & Assumptions

## Constraints

- **Budget:** Personal project funded individually; primary cost is Norgate Data subscription (already committed). Additional costs limited to computing resources (local machine for MVP, potential cloud costs for production phase estimated at <$50/month if needed).

- **Timeline:** No hard deadlines, but goal is to make steady progress. MVP (Stage 1-2) targeted for completion within a reasonable exploratory period, allowing time for learning and proper implementation rather than rushing to production.

- **Resources:** Solo developer (you), working on this alongside other commitments. Development happens in available time slots rather than full-time dedication. This is sustainable long-term but means progress is incremental.

- **Technical:**
  - Data limited to US equities initially (Norgate Platinum US Stocks)
  - Monthly rebalancing frequency for MVP (daily/weekly adds complexity)
  - Historical data starts 1990 (30+ years available, but some very long-term studies may require earlier data)
  - No short-selling constraints modeled initially (assumes perfect ability to short at equal cost to going long)
  - Transaction costs will be modeled simplistically initially (fixed bps per trade)

- **Knowledge:** Building knowledge of momentum strategies through implementation—expect learning curve on both the finance theory and the engineering best practices. Some iteration and refactoring expected as understanding deepens.

## Key Assumptions

- **Market data quality:** Norgate Data provides accurate, survivorship-bias-free data suitable for rigorous backtesting

- **Academic research validity:** Momentum effects documented in Jegadeesh & Titman (1993), Moskowitz et al. (2012), and related literature remain relevant and exploitable

- **Implementation capacity:** Python + standard scientific libraries (pandas/numpy) are sufficient for all computational needs without requiring lower-level languages

- **Backtesting as validation:** Robust backtests with proper handling of biases provide meaningful signal about likely future performance (though not guaranteed)

- **Capital availability:** When ready for live trading, sufficient capital will be available to deploy strategies at reasonable scale (e.g., $10K+ to avoid being dominated by fixed transaction costs)

- **Market access:** Standard brokerage accounts provide adequate access to long and short positions in US equities with reasonable transaction costs and borrowing rates for shorts

- **Time consistency:** Dedicating regular time to this project (even if not full-time) will lead to meaningful progress over months

- **Learning compounds:** Each stage builds on previous work; investing time in solid architecture early pays dividends in faster experimentation later

- **Simplicity first works:** Starting with simple implementations (equal-weight, monthly rebalancing, no overlapping portfolios) is adequate for MVP and won't invalidate core insights

- **Personal control value:** Owning the full stack and deeply understanding the strategies is worth the development time investment vs. using black-box commercial solutions
