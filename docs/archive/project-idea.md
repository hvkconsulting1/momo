## 0. Project Frame: What you’re really building

**Working name:** `portfolio-momentum`

**High-level goal:**
A **modular research + trading framework** that:

1. Starts with **cross-sectional equity momentum (Jegadeesh & Titman style)** – rank assets by 12-1 month returns, long winners, short losers. 
2. Can later plug in:

   * **Time-series momentum (trend-following)** – Moskowitz/Ooi/Pedersen style. 
   * **Dual momentum, ETF rotation, risk overlays** etc. 
3. Is robust enough that, if backtests look good, you can:

   * Forward-test (paper trade)
   * Then run **small, real capital** with clear guardrails.

Think of it as building a **momentum lab**, not just “one strategy.”

---

## 1. Pick the first concrete target

You said: start with **“the first, base strategy by jegedessh, the cross sectional momentum.”** Perfect.

Let’s define your **Version 1 Strategy** very concretely:

> **Strategy V1 – Classic 12–1 Cross-Sectional Momentum**
>
> * Universe: liquid equities (e.g., top N by market cap)
> * Signal: 12-month return **excluding last month** (months t-12 to t-2). 
> * Ranking: sort all stocks by that signal
> * Portfolio:
>
>   * Long: top decile (or top 20%)
>   * Short: bottom decile (or bottom 20%)
>   * Equal-weight within long and short legs
> * Rebalance: monthly
> * Holding: 1-month holding (no overlapping portfolios in V1, keep it simple)

Later, you can upgrade to J/K overlapping portfolios and more nuanced weighting like in the original papers, but this is enough to get a full pipeline working. 

---

## 2. Architecture: How to make this extensible

Before timeline, let’s sketch the **shape of the codebase** so future strategies “snap in” instead of requiring rewrites.

Think in **layers**:

1. **Data Layer**

   * Handles:

     * Price history (OHLCV + dividends/adjustments if you want total return)
     * Metadata: ticker, sector, delistings, etc.
   * Abstracted so that later you can plug different universes (stocks, ETFs, futures proxies).

2. **Signal Layer**

   * Functions that take a price series and output **signals**:

     * `cross_sectional_momentum_12_1(prices)`
     * `time_series_momentum_12m(prices)` (sign of own last 12m return) 
     * `dual_momentum_signal(...)`, etc.
   * No portfolio construction here, just per-asset numbers like “momentum score” or “+1/-1”.

3. **Portfolio Construction Layer**

   * Takes signals across all assets at time t and produces **weights**:

     * Cross-sectional decile weighting (long top X%, short bottom X%) 
     * Volatility-scaled positions (for time-series)
     * Rank-weighting or equal-weighting.

4. **Backtest Engine**

   * Given weights and price data:

     * Computes P&L, turnover, drawdown, factor exposures, etc.
   * Should be generic enough to backtest both:

     * Long-short cross-sectional strategies
     * Long/flat absolute momentum, trend-following, dual momentum ETF strategies. 

5. **Risk & Execution Layer (later)**

   * Slippage / fees model
   * Volatility targeting
   * Maybe basic position limits and max leverage

If you keep these **separate**, adding time-series and dual momentum later is mostly a matter of dropping in new signal + portfolio-construction functions.

---

## 3. Roadmap: staged progression

I’ll give you a set of **stages**, each with concrete outcomes. You can think of these as “sprints,” but without dates attached.

---

### Stage 1 – Understand & rephrase the base strategy

**Objective:** Be able to explain Jegadeesh/Titman momentum and your exact variant in your own words and in pseudocode.

**Tasks:**

1. Re-read the cross-sectional sections from your notes:

   * Jegadeesh & Titman 1993 summary and blueprint 
   * The general cross-sectional algorithm section 
2. Write a **one-page spec** for “Strategy V1”:

   * Inputs (data needed; e.g., adjusted monthly prices for N stocks)
   * Exact formulas for:

     * 12-1 momentum signal (how you’re computing returns)
     * Ranking and portfolio selection
     * Weighting and rebalancing rules
   * Backtest assumptions (no transaction costs to start, then add simple costs).

**Output of Stage 1:**
A short markdown doc in your repo: `docs/strategy-v1-jegadeesh-cross-sectional.md`.

---

### Stage 2 – Minimal backtest engine + V1 strategy

**Objective:** Have a **working backtest** for your V1 cross-sectional momentum.

**Tasks:**

1. **Data ingestion:**

   * Pick a single universe (e.g., a few hundred large caps) and format:

     * Monthly price series
     * Adjusted for splits/dividends if possible.
   * Normalize into a simple table like:

     * `date, asset_id, price` (plus optional shares_outstanding for value weighting later).

2. **Signal computation (Signal Layer):**

   * Implement 12-1 momentum:

     * For each month t, for each asset:

       * Compute cumulative return from t-12 to t-2.
       * Store as `momentum_12_1[asset, t]`.

3. **Portfolio construction (Portfolio Layer):**

   * For each month t:

     * Rank assets by `momentum_12_1`.
     * Select:

       * Long set = top 20% by rank.
       * Short set = bottom 20%.
     * Assign equal weights:

       * Long leg: +1 / (#long) each.
       * Short leg: –1 / (#short) each.
     * Normalize so that long and short gross each sum to 1 (2x gross, 0 net).

4. **Backtesting (Backtest Engine):**

   * Each month, use weights at end of month t to hold through t+1.
   * Compute portfolio return from t to t+1:

     * Weighted sum of asset returns.
   * Build full performance series:

     * Cumulative return
     * Annualized return & volatility
     * Max drawdown
     * Simple Sharpe.

**Output of Stage 2:**

* A script/notebook that produces:

  * Equity curve of V1 long-short strategy.
  * Basic stats (CAGR, vol, Sharpe, max DD).
* At this point you have your **foundation**.

---

### Stage 3 – Make the engine reusable & add knobs

Now you harden the framework so it supports future strategies.

**Objective:** Turn your single V1 script into a **reusable mini-library**.

**Tasks:**

1. Generalize your backtest engine:

   * Accept an arbitrary:

     * `signal_function(data, params)` → signal matrix
     * `weight_function(signals, params)` → weight matrix
   * Keep the portfolio evaluation generic.

2. Expose tunable parameters:

   * Lookback length J (3, 6, 12 months).
   * Skip-month on/off.
   * Top/bottom % (10%, 20%, 30%).
   * Equal-weight vs rank-weight.

3. Add **basic transaction cost modeling**:

   * E.g., fixed bps per trade × turnover
   * At least compute turnover each period; then apply a simple cost model.

4. Add **reporting utilities**:

   * Summary metrics
   * Distribution of monthly returns
   * Maybe a factor regression later if you want (to see exposure to market).

**Output of Stage 3:**

* A small, composable backtesting framework that can be reused for:

  * Cross-sectional momentum variants
  * Time series momentum
  * Dual momentum, etc.

---

### Stage 4 – Add Time-Series Momentum (trend-following)

Now you’re ready to plug in **time-series momentum** using same infrastructure.

**Objective:** Implement a simple Moskowitz/Ooi/Pedersen-style TSMOM strategy in your framework. 

**Tasks:**

1. Implement **TSMOM signal**:

   * For each asset & month t:

     * Compute 12-month return (t-12 to t).
     * Signal = `+1` if > 0, `-1` if < 0. 

2. Add **volatility scaling** option:

   * Estimate σ (e.g., 3- or 6-month realized vol).
   * Position size = `signal * (target_vol / σ)`.

3. Use a **simplified universe to start**:

   * You can use ETFs that proxy futures (equity, bond, commodity, FX) if that’s easier.
   * The underlying math is identical; the asset form doesn’t matter at first.

4. Compare:

   * Cross-sectional vs time-series momentum curves
   * Their correlations and drawdowns (your notes show their diversification benefits). 

**Output of Stage 4:**

* A TSMOM strategy living alongside your cross-sectional V1, proving your architecture is reusable.

---

### Stage 5 – Strategy variants & combinations

Once both cores exist, you can have fun with **variants**:

Ideas sourced from your notes:  

1. **Cross-sectional variants**

   * Vary lookbacks (3, 6, 12 months).
   * Try overlapping J/K portfolios (e.g., form and hold for 6 months with overlapping cohorts).
   * Try rank-weighting or volatility-weighting of cross-sectional positions.

2. **Time-series variants**

   * Multi-horizon blend (1, 3, 12-month signals averaged).
   * Different rebal frequency (weekly vs monthly) and cost impact.

3. **Dual momentum**

   * Implement Gary Antonacci-style:

     * Relative momentum to pick leader between two or more assets.
     * Absolute momentum filter vs T-bills or 0% return.
     * All-in winner vs defensive asset when trend is negative. 

4. **ETF rotation strategies**

   * Use your “top N ETFs by 6- or 12-month momentum” approach.
   * Long-only, simple equal-weight, rebalance monthly. 

---

### Stage 6 – From backtest to “live candidate”

**Objective:** Turn a simulation into something you’d trust with real money (even small).

**Tasks:**

1. **Robustness checks**

   * Parameter sweeps: ensure performance isn’t dependent on a narrow parameter slice.
   * Sub-period performance (e.g., different decades/market regimes).
   * Stress tests: what happens in crisis regimes (as described for momentum & TSMOM in your notes)? 

2. **Paper trading setup**

   * Export daily (or monthly) target weights to CSV / DB.
   * Track hypothetical trades and P&L vs backtest.

3. **Risk rules (very important for live)**

   * Max leverage.
   * Max position size per name / sector / asset class.
   * Volatility target for the whole portfolio.
   * Max drawdown level where you auto-de-risk or stop.

4. **Operational “go live” checklist**

   * Data quality checks.
   * Slippage & fees assumptions.
   * Clear doc on: “what makes me turn this off or de-risk?”

> ⚠️ Quick note: nothing here is financial advice. Treat all strategies as research experiments unless/until you’re fully comfortable with the risks and have sized them appropriately.

---

## 4. How to work day-to-day

Since you also want to **learn**, not just code, I’d run this as three parallel streams:

1. **Reading stream**

   * Keep working through:

     * Cross-sectional momentum papers
     * Time-series momentum & trend-following papers
     * Dual momentum / ETF rotation strategies
       (which your uploaded notes already nicely summarize). 

2. **Coding stream**

   * Always be building toward the next stage: first V1, then generalization, then TSMOM, etc.

3. **Research notebook**

   * Keep a log (markdown or Jupyter) with:

     * What you tried
     * Params
     * Performance summaries
     * “What I learned” bullets

That notebook becomes your personal **momentum playbook**.
