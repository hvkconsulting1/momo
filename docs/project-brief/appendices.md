# Appendices

## A. Research Summary

This project brief draws on prior research and planning documented in **`docs/project-idea.md`**, which contains:

- **Detailed 6-stage roadmap:** From understanding the base strategy through production readiness
- **Layered architecture specification:** Data → Signal → Portfolio → Backtest → Risk layers with clear separation of concerns
- **Strategy-specific guidance:** Implementation details for V1 cross-sectional momentum (Jegadeesh & Titman style)
- **Progression framework:** Clear path from simple to sophisticated implementations
- **Working philosophy:** Three parallel streams (reading, coding, research notebook) for compound learning

**Academic Research Foundation:**

The project is grounded in several decades of momentum research, with uploaded papers covering:

- **Cross-sectional equity momentum:** Jegadeesh & Titman (1993) foundational work on ranking stocks by past returns
- **Time-series momentum (TSMOM):** Moskowitz, Ooi & Pedersen framework for trend-following across asset classes
- **Dual momentum:** Antonacci's approach combining relative and absolute momentum
- **ETF rotation strategies:** Applications to practical portfolio construction

**Key Insights from Research:**

- Momentum is a persistent, well-documented anomaly with theoretical and empirical support
- Cross-sectional and time-series momentum have low correlation and can be combined for diversification
- Proper implementation requires careful attention to survivorship bias, look-ahead bias, and transaction costs
- Momentum strategies experience occasional sharp drawdowns ("momentum crashes") requiring risk management
- Multiple parameter choices (lookback periods, skip months, weighting schemes) offer robustness testing opportunities

## B. References

**Internal Documentation:**
- `docs/project-idea.md` - Detailed project planning and staged roadmap
- Research papers on momentum strategies (uploaded to project repository)

**Key Academic Papers:**
- Jegadeesh, N., & Titman, S. (1993). "Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency"
- Moskowitz, T. J., Ooi, Y. H., & Pedersen, L. H. (2012). "Time Series Momentum"
- Antonacci, G. (various). Dual Momentum research and implementations

**Data Source:**
- Norgate Data: https://norgatedata.com/ (Platinum US Stocks subscription)
- norgatedata Python package documentation

**Technical Resources:**
- Python Data Science Stack: pandas, numpy, scipy, matplotlib
- Jupyter Project: https://jupyter.org/
- Potential backtest framework references: zipline, backtrader, vectorbt (for comparison/validation)

**Momentum Research Resources:**
- AQR Capital Management research papers on momentum
- Alpha Architect blog posts on factor investing and momentum implementation
- CXO Advisory Group momentum strategy analysis
