# Project Brief: portfolio-momentum

## Executive Summary

**portfolio-momentum** is a modular research and trading framework designed to systematically implement, backtest, and analyze momentum-based investment strategies. Starting with classic cross-sectional equity momentum (Jegadeesh & Titman 1993), the framework provides a robust, extensible architecture that can accommodate time-series momentum (trend-following), dual momentum, and ETF rotation strategies. The primary goal is to create a "momentum lab" rather than a single-strategy system—enabling rigorous research, parameter exploration, and eventual forward-testing with real capital under clearly defined risk controls. The framework serves quantitative traders and researchers who want to move beyond academic papers into practical implementation while maintaining scientific rigor and extensibility for future strategy development.

## Problem Statement

**Current State & Pain Points:**

Momentum strategies are well-documented in academic research with decades of empirical evidence supporting their effectiveness (Jegadeesh & Titman 1993, Moskowitz et al. 2012, among others). However, there exists a significant gap between understanding these strategies conceptually and implementing them in a practical, robust manner. Individual traders and researchers face several critical challenges:

1. **Research-to-Implementation Gap:** Academic papers provide theoretical frameworks but lack production-ready code, leaving practitioners to reinvent the wheel with inconsistent methodologies and potential implementation errors.

2. **Fragmented Learning:** Building momentum strategies typically involves scattered attempts—one-off backtests that don't build on each other, making it difficult to develop deep intuition about how these strategies behave across different market conditions.

3. **Inflexible Architectures:** Most initial implementations are hardcoded for a single strategy variant, making it prohibitively expensive to explore related strategies (time-series vs. cross-sectional, different lookback periods, combined approaches) without complete rewrites.

4. **Uncertain Path to Production:** Without clear progression from backtest → paper trading → live trading with appropriate risk controls, promising research remains theoretical and never reaches practical application.

**Impact:**

This gap prevents quantitatively-minded individuals from systematically validating momentum strategies, understanding their nuances through experimentation, and confidently deploying capital based on evidence-based approaches. Time is wasted on infrastructure rather than insight generation, and valuable learning opportunities are lost due to the friction of exploration.

**Why Existing Solutions Fall Short:**

- **Commercial platforms** (QuantConnect, Quantopian) offer infrastructure but impose vendor lock-in and may not support the specific strategy variants or research workflows needed
- **Academic code repositories** are typically proof-of-concept quality, not designed for extensibility or production use
- **From-scratch implementations** require significant upfront time investment and often sacrifice modularity for expedience

**Urgency:**

The knowledge exists, the data is accessible, and computational resources are available—but without a systematic, modular framework, this remains an unrealized opportunity to build evidence-based trading strategies with proper risk management.

## Proposed Solution

**Core Concept & Approach:**

The portfolio-momentum framework solves the research-to-implementation gap through a **layered, modular architecture** that separates concerns and enables strategy composition. The system is designed around five distinct layers:

1. **Data Layer** - Handles price history (OHLCV + adjustments), metadata (ticker, sector, delistings), abstracting data sources so different universes (stocks, ETFs, futures) can plug in seamlessly

2. **Signal Layer** - Pure functions that transform price series into signals (e.g., `cross_sectional_momentum_12_1()`, `time_series_momentum_12m()`), with no portfolio logic—just per-asset scores

3. **Portfolio Construction Layer** - Transforms signals into position weights using strategies like decile ranking, volatility scaling, equal-weighting, or rank-weighting

4. **Backtest Engine** - Generic evaluation engine that computes P&L, turnover, drawdown, factor exposures for any signal/weight combination

5. **Risk & Execution Layer** - Models slippage, transaction costs, volatility targeting, position limits, and leverage constraints

This separation means adding a new momentum variant (time-series, dual momentum, ETF rotation) is simply a matter of adding new signal and portfolio-construction functions—the data layer and backtest engine remain unchanged.

**Key Differentiators:**

- **Research-First Architecture:** Built to support learning through systematic experimentation, not just running a single strategy
- **Progressive Complexity:** Start simple (V1 cross-sectional momentum) and add sophistication incrementally without architectural rewrites
- **Evidence-Based Progression:** Clear path from backtest → robustness checks → paper trading → live deployment with documented risk controls
- **Composability:** Mix and match signals, portfolio construction methods, and risk overlays to explore strategy space efficiently

**Why This Will Succeed:**

Unlike commercial platforms that optimize for breadth, this framework optimizes for **depth** in momentum strategies specifically. Unlike academic code that proves concepts, this framework is designed for **production use** from the start. Unlike one-off implementations, this framework treats **extensibility as a first-class requirement**, enabling compound learning where each new strategy builds on proven infrastructure.

**High-Level Vision:**

A personal "momentum lab" where you can rapidly test ideas, understand behavior across market regimes, validate through paper trading, and confidently deploy capital to strategies you've thoroughly understood through building and experimentation.

## Target Users

### Primary User Segment: Quantitative Trader/Researcher (Individual)

**Demographic/Profile:**
- Individual with quantitative background (finance, economics, mathematics, computer science, or engineering)
- Comfortable with programming and data analysis
- Has read or is familiar with academic finance literature on momentum strategies
- May be currently employed in tech/finance or pursuing this as a serious side project
- Has access to capital for eventual live trading (even if starting small)

**Current Behaviors & Workflows:**
- Reading academic papers on momentum and factor investing
- Experimenting with backtests using tools like Python/pandas, R, or commercial platforms
- Likely has tried one-off strategy implementations that become hard to maintain or extend
- Spending time on data wrangling and infrastructure instead of strategy research
- May be paper trading or manually tracking ideas without systematic validation

**Specific Needs & Pain Points:**
- **Learning through doing:** Wants to deeply understand momentum strategies by building them from scratch, not just reading about them
- **Systematic experimentation:** Needs to test variants (different lookbacks, universes, weighting schemes) without rewriting everything
- **Confidence to deploy capital:** Requires robust backtesting, paper trading validation, and clear risk controls before committing real money
- **Personal control:** Prefers owning the full stack rather than depending on commercial platforms that may change pricing, features, or shut down
- **Research notebook:** Wants to document what works, what doesn't, and build institutional knowledge over time

**Goals They're Trying to Achieve:**
1. **Deep understanding** of how momentum strategies work across different market regimes
2. **Build a production-ready system** that can go from research idea → validated backtest → paper trading → live trading
3. **Develop an edge** through systematic research and disciplined implementation
4. **Create passive income potential** through evidence-based, risk-controlled trading strategies
5. **Compound learning** where each new strategy builds on proven infrastructure and accumulated knowledge

## Goals & Success Metrics

### Business Objectives

- **Complete V1 Cross-Sectional Momentum Implementation:** Build a working backtest of the classic Jegadeesh & Titman 12-1 momentum strategy with documented equity curve, Sharpe ratio, max drawdown, and turnover statistics

- **Establish Reusable Framework Infrastructure:** Create modular architecture (Data → Signal → Portfolio → Backtest → Risk layers) capable of supporting multiple strategy variants without requiring architectural rewrites

- **Validate Time-Series Momentum Strategy:** Successfully implement TSMOM (Moskowitz/Ooi/Pedersen style) using existing framework, demonstrating architecture reusability and generating comparative performance analysis

- **Achieve Paper Trading Readiness:** Build automated signal generation and position calculation system that can run on current data and produce daily/monthly target portfolios for forward validation

- **Document Learning & Research Process:** Maintain comprehensive research notebook tracking all experiments, parameter sensitivities, regime-specific performance, and accumulated insights about momentum strategy behavior

### User Success Metrics

- **Understanding Depth:** Ability to explain momentum strategies from first principles, including why they work, when they fail, and how different variants compare—measured by quality of written strategy specifications and research notes

- **Experimentation Velocity:** Time from "I want to test X variant" to "I have backtest results" decreases significantly as framework matures—targeting ability to run new strategy variants in hours rather than days

- **Confidence Level:** Subjective assessment of readiness to deploy real capital based on robustness of backtests, understanding of risk controls, and successful paper trading validation period

- **Code Quality & Maintainability:** Framework remains comprehensible and extensible over time, with clear separation of concerns enabling easy debugging and enhancement

- **Research Compound Effect:** Each new strategy implementation teaches insights applicable to future work, captured in research notebook and reflected in improved framework design

### Key Performance Indicators (KPIs)

- **V1 Strategy Performance:** Annualized Sharpe ratio >0.5 in backtest (academic literature suggests 0.7-1.0+ is achievable; starting conservatively)

- **Framework Reusability:** Number of strategy variants implemented using same core infrastructure (Target: 3+ variants including cross-sectional, time-series, and at least one combination/rotation strategy)

- **Backtest Coverage:** Historical period tested spans at least 10+ years including different market regimes (bull markets, bear markets, high/low volatility periods)

- **Parameter Robustness:** Strategy performance remains positive across reasonable parameter ranges (e.g., 6-month vs 12-month lookbacks, different decile cutoffs, various rebalancing frequencies)

- **Paper Trading Validation:** Live forward-testing period of 3-6 months showing strategy behaves as expected compared to backtest (not necessarily profitable in short period, but consistent with expectations)

- **Research Documentation:** Comprehensive markdown-based research notebook with minimum 20+ documented experiments including what was tested, results, and key learnings

- **Risk Control Implementation:** Clearly defined and tested risk rules including max position sizes, leverage limits, volatility targeting, and drawdown-based de-risking triggers

## MVP Scope

The MVP focuses on building **Strategy V1 (Classic 12-1 Cross-Sectional Momentum)** with a working backtest engine and foundational architecture—proving the core concept works before expanding to additional strategies.

### Core Features (Must Have)

- **Strategy V1 Specification Document:** Written markdown specification (`docs/strategy-v1-jegadeesh-cross-sectional.md`) that defines exact formulas for 12-1 momentum signal, ranking/selection rules, weighting approach, rebalancing logic, and initial backtest assumptions

- **Data Ingestion Module:** Code to load and normalize monthly price data for a defined equity universe (e.g., top 500 stocks by market cap), handling adjustments for splits/dividends, with simple data validation and quality checks

- **Cross-Sectional Momentum Signal Function:** Implementation of 12-1 momentum calculation (cumulative return from t-12 to t-2 for each asset at each month t), producing a clean signal matrix

- **Portfolio Construction Module:** Ranking logic that selects top decile (top 10%, long) and bottom decile (bottom 10%, short) based on momentum signals, with equal-weight allocation within each leg, normalized to 1x gross exposure per leg (2x total, 0 net)

- **Minimal Backtest Engine:** Generic backtesting framework that takes weights and prices, computes monthly returns, tracks cumulative portfolio value, and calculates core statistics: CAGR, volatility, Sharpe ratio, max drawdown, and monthly turnover

- **Performance Visualization:** Basic equity curve plot and summary statistics table that can be generated from backtest results (can use simple matplotlib/similar tools)

- **Research Notebook Setup:** Initial markdown-based research log structure for documenting experiments, with template for recording: date, hypothesis tested, parameters used, results, and key insights

### Out of Scope for MVP

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

### MVP Success Criteria

**The MVP is considered successful when:**

1. You can explain the V1 cross-sectional momentum strategy from first principles and have a written specification document
2. The backtest engine produces a complete equity curve for V1 strategy over 10+ years of historical data
3. Backtest statistics are reasonable (positive Sharpe ratio, drawdown characteristics consistent with momentum literature)
4. The code architecture clearly separates Data, Signal, Portfolio Construction, and Backtest layers
5. You can modify a parameter (e.g., top/bottom quintile instead of decile) and re-run the backtest in under 5 minutes
6. Performance metrics and equity curve can be generated and saved for comparison
7. First research notebook entry is complete documenting the V1 baseline implementation

## Post-MVP Vision

### Phase 2 Features

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

### Long-Term Vision

**A comprehensive "momentum lab"** where you can:

- Rapidly test any momentum-based strategy idea (cross-sectional, time-series, dual momentum, combinations)
- Understand strategy behavior through systematic exploration: parameter sensitivity, regime analysis, correlation structure
- Validate strategies through multi-stage progression: backtest → robustness checks → paper trading → selective live deployment
- Build institutional knowledge via research notebook documenting what works, what doesn't, and why
- Deploy multiple low-correlation momentum strategies simultaneously with portfolio-level risk management
- Operate confidently with real capital based on thoroughly validated, well-understood strategies

**The framework becomes your personal quantitative research platform**—optimized for depth in momentum strategies rather than breadth across all possible approaches.

### Expansion Opportunities

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

## Technical Considerations

These represent initial technical thoughts and preferences. Final technology decisions will be made during implementation based on practical experience and emerging requirements.

### Platform Requirements

- **Target Platforms:** Linux/macOS for primary development; Windows compatibility desirable but not required for MVP
- **Computing Environment:** Local development on personal machine for MVP; potential cloud deployment (AWS/GCP) for paper trading and live operations in later stages
- **Performance Requirements:**
  - Backtest execution for 30+ years of monthly data across 500+ securities should complete in under 1 minute
  - Parameter sweep testing (10+ variants) should complete in under 10 minutes
  - Research notebook operations should be interactive (sub-second response for data exploration)

### Technology Preferences

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

### Architecture Considerations

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

## Constraints & Assumptions

### Constraints

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

### Key Assumptions

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

## Risks & Open Questions

### Key Risks

- **Strategy Decay:** Momentum effects may have weakened over time due to increased competition/capital pursuing these strategies. Risk that backtested performance significantly exceeds achievable live performance even with proper execution.

- **Implementation Errors:** Risk of bugs in signal calculation, portfolio construction, or backtest engine that produce misleading results. Without external validation, subtle errors could go undetected and lead to false confidence.

- **Market Regime Change:** Historical backtests may not predict future performance if market structure has fundamentally changed (e.g., algorithmic trading dominance, different correlation structures, policy regime shifts).

- **Transaction Costs Underestimated:** Initial simple cost models (fixed bps) may not capture real-world costs including market impact, short borrow costs, funding costs for leverage, and slippage during volatile periods.

- **Execution Challenges:** Difference between backtest assumptions and live execution reality—liquidity constraints, inability to short certain securities, extreme market conditions affecting fills.

- **Momentum Crashes:** Known phenomenon where momentum strategies can experience severe, rapid drawdowns (especially during market reversals). Risk that live trading coincides with crash period, leading to significant losses and psychological difficulty maintaining the strategy.

- **Time Commitment Sustainability:** Risk that other priorities reduce available time for the project, leading to incomplete implementation or inability to monitor live strategies adequately.

- **Overfitting Through Iteration:** Risk of unconsciously fitting strategy parameters to historical data through repeated testing and refinement, leading to overstated expected performance.

- **Capital Inadequacy:** Even with strategies ready, may not have sufficient capital to deploy at scale where transaction costs are reasonable and diversification is adequate.

### Open Questions

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

### Areas Needing Further Research

- **Academic Literature Deep Dive:** Need to read original Jegadeesh & Titman (1993) paper carefully and compare their exact methodology to proposed implementation—ensure no critical details are missed.

- **Recent Momentum Research:** Review post-2010 momentum literature for insights on implementation details, common pitfalls, and recent findings about strategy evolution.

- **Crisis Period Behavior:** Study how cross-sectional momentum behaved during 2000 tech crash, 2008 financial crisis, 2020 COVID crash to set realistic expectations for drawdowns.

- **Norgate Data API:** Learn norgatedata package API thoroughly—how to query historical constituents, handle delistings, retrieve adjusted prices, optimize query patterns.

- **Backtest Engine Design Patterns:** Research best practices for building backtest engines—common pitfalls like look-ahead bias, proper handling of corporate actions, vectorized computation approaches.

- **Cost Models:** Research realistic transaction cost estimates for equity momentum strategies—look for practitioner literature or broker cost structures.

- **Python Performance Optimization:** If backtest performance becomes bottleneck, need to research pandas optimization, numpy vectorization, or potential use of numba/Cython.

- **Risk Management Frameworks:** Study approaches to position sizing, volatility targeting, and drawdown-based de-risking used in practitioner implementations.

## Appendices

### A. Research Summary

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

### B. References

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

## Next Steps

### Immediate Actions

**1. Review and finalize this Project Brief**
   - Read through the complete brief to ensure alignment with vision and goals
   - Confirm technical choices (Norgate Data, Python stack, repository structure)
   - Validate MVP scope is appropriately focused vs. over/under-scoped

**2. Read Jegadeesh & Titman (1993) paper in detail**
   - Understand exact methodology for 12-1 cross-sectional momentum
   - Note specific implementation details: return calculations, portfolio formation, rebalancing rules
   - Document any differences between their approach and planned implementation

**3. Create Strategy V1 specification document**
   - Write `docs/strategy-v1-jegadeesh-cross-sectional.md` as outlined in MVP scope
   - Define precise formulas, universe selection criteria, and backtest assumptions
   - This becomes the blueprint for implementation (Stage 1 deliverable)

**4. Set up development environment**
   - Create Python virtual environment (3.10+)
   - Install core dependencies: pandas, numpy, scipy, matplotlib, jupyter, norgatedata
   - Initialize repository structure as outlined in Technical Considerations
   - Set up Norgate Data credentials securely

**5. Explore Norgate Data API**
   - Write exploratory Jupyter notebook to understand norgatedata package
   - Test querying historical prices, index constituents, and delisting data
   - Experiment with caching strategies (query vs. local storage trade-offs)
   - Document API patterns and best practices learned

**6. Begin data layer implementation**
   - Start with simple module to fetch and normalize price data
   - Implement basic data quality checks
   - Create reproducible data loading process
   - This is the foundation for all subsequent work

**7. Set up research notebook structure**
   - Create `docs/research-log.md` with template for experiment documentation
   - Make first entry documenting project initialization and environment setup
   - Establish habit of documenting learnings as you go

**8. (Optional) Connect with Product Manager for PRD development**
   - If transitioning to formal PRD process, handoff this brief to PM
   - Collaborate on converting high-level vision into detailed product requirements
   - Work section-by-section to create comprehensive PRD

---

### PM Handoff

This Project Brief provides the full context for **portfolio-momentum**. If you're ready to move forward with creating a detailed Product Requirements Document (PRD), please start in **'PRD Generation Mode'**. Review the brief thoroughly, understand the staged approach (MVP → Phase 2 → Long-term vision), and work with the user to create the PRD section by section as the template indicates, asking for any necessary clarification or suggesting improvements.

**Key Context for PRD Development:**
- This is a personal research + trading framework, not a commercial product
- The user is both the developer and end user (solo project)
- Success is measured by both working code AND deep understanding of momentum strategies
- MVP focuses narrowly on V1 cross-sectional momentum to prove architecture works
- Extensibility is critical—the framework must support future strategy variants
- Data quality is paramount (Norgate Data chosen specifically for survivorship-bias-free backtesting)
