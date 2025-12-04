# Epic 2: Momentum Signal & Portfolio Construction

**Epic Goal:** Implement the 12-1 cross-sectional momentum signal calculation following Jegadeesh & Titman methodology, build cross-sectional ranking system that handles edge cases and missing data, create decile-based portfolio construction with equal-weight allocation normalized to target exposure levels, and validate the complete signal-to-weights pipeline produces sensible outputs. This epic delivers the core strategy logic that transforms price data into portfolio positions.

## Story 2.1: Implement 12-1 Momentum Signal Calculation

**As a** quantitative researcher,
**I want** to calculate 12-1 momentum signals (cumulative return from t-12 to t-2 months) for all securities in the universe,
**so that** I can rank securities by their momentum characteristics.

### Acceptance Criteria

1. `src/signals/momentum.py` module implements a pure function `calculate_momentum_signal()` that accepts price data and returns momentum values
2. Function calculates cumulative return from 12 months ago to 2 months ago (skipping most recent month) for each security
3. Return calculation properly handles the lookback period: signal at month t uses returns from t-12 to t-2
4. Function handles missing data gracefully: returns NaN for securities with insufficient history (less than 12 months)
5. Signal calculation is vectorized using pandas/numpy for performance (no explicit loops over tickers)
6. Function is deterministic (same inputs always produce same outputs) with no side effects
7. Unit tests validate calculation against hand-computed examples for known price series
8. Unit tests verify edge cases: insufficient data, all NaN prices, single-ticker scenarios
9. Function accepts configurable parameters: lookback_months (default 12), skip_months (default 1) for future experimentation

## Story 2.2: Implement Cross-Sectional Ranking and Decile Selection

**As a** quantitative researcher,
**I want** to rank securities by momentum signals and select top/bottom deciles at each rebalance date,
**so that** I can identify long and short portfolio candidates.

### Acceptance Criteria

1. `src/signals/ranking.py` module implements function `rank_cross_sectional()` that accepts signals and returns percentile ranks
2. Ranking is performed within each time period (cross-sectional ranking at each month)
3. Function handles NaN values by excluding them from ranking (note: securities with insufficient history should already be filtered from universe in Story 1.5; NaN handling here is for edge cases like data gaps)
4. Function implements `select_deciles()` that identifies top 10% (long candidates) and bottom 10% (short candidates) based on ranks
5. Decile selection is configurable (e.g., quintiles = top/bottom 20%, tertiles = top/bottom 33%)
6. Edge case handling: if universe has fewer than 10 securities, function uses absolute thresholds or minimum counts
7. Output format clearly identifies long/short candidates with their ranks for each rebalance date
8. Unit tests validate ranking logic with synthetic data (verify top/bottom selections are correct)
9. Unit tests verify edge cases: all equal signals, mostly NaN signals, very small universes

## Story 2.3: Implement Equal-Weight Portfolio Construction with Overlapping Portfolios

**As a** quantitative researcher,
**I want** to construct equal-weighted portfolios from long/short candidates with overlapping holding periods,
**so that** I can replicate the classic Jegadeesh & Titman methodology with reduced turnover and transaction costs.

### Acceptance Criteria

**Basic Portfolio Construction:**
1. `src/portfolio/construction.py` module implements function `equal_weight_portfolio()` that accepts long/short candidates and returns weights
2. Long leg: Each selected security receives equal weight, normalized to 1.0 total long exposure (e.g., 50 longs → 2% each)
3. Short leg: Each selected security receives equal negative weight, normalized to -1.0 total short exposure (e.g., 50 shorts → -2% each)
4. Total portfolio has 2.0 gross exposure (1.0 long + 1.0 short) and 0.0 net exposure (market neutral)
5. Function handles edge cases: different numbers of longs vs shorts, empty long or short legs (returns zero weights)
6. Weights sum correctly within floating-point precision: sum(long_weights) ≈ 1.0, sum(short_weights) ≈ -1.0

**Overlapping Portfolio Logic:**
7. Function implements `overlapping_portfolio()` that accepts `holding_months` parameter (default K=6)
8. For each rebalance date t, maintains K active sub-portfolios (formed at months t, t-1, ..., t-K+1)
9. Final portfolio weights = equal-weighted average of all K active sub-portfolios
10. With K=6 holding period, approximately 1/6 of portfolio positions turn over each month (vs 100% for K=1)
11. Function handles initialization period: for months 1 through K-1, fewer than K sub-portfolios are active
12. Configuration supports K=1 (simple monthly rebalance, no overlap) for testing and comparison

**Output & Testing:**
13. Output format is a DataFrame with tickers as index, weights as values, suitable for backtest engine consumption
14. Function is pure and deterministic with configurable exposure targets (e.g., 1.5x long, 0.5x short)
15. Unit tests verify weight calculations for various portfolio sizes and validate sum constraints
16. Unit tests verify overlapping logic: with K=6, portfolio at month 6 correctly averages weights from 6 sub-portfolios formed at months 1-6
17. Unit tests verify turnover reduction: measure position changes month-to-month with K=6 vs K=1

### Notes

- **Overlapping Portfolio Rationale:** Jegadeesh & Titman (1993) used overlapping portfolios with typical holding periods of 3-12 months. This smooths returns, reduces transaction costs (turnover drops from 100% to ~17% monthly with K=6), and matches the academic baseline methodology.
- **Performance Impact:** At typical transaction costs of 5-10 bps per side, the turnover reduction from overlapping portfolios is critical for strategy profitability.
- **Flexibility:** The `holding_months` parameter enables experimentation (K=1, 3, 6, 12) to study holding period effects on strategy performance.

## Story 2.4: Create Signal-to-Weights Pipeline Validation

**As a** quantitative researcher,
**I want** an end-to-end demonstration of the signal calculation → ranking → portfolio construction pipeline,
**so that** I can verify the complete strategy logic produces sensible portfolio weights.

### Acceptance Criteria

1. Integration test or notebook (`notebooks/02_signal_portfolio_validation.ipynb`) demonstrates full signal-to-weights pipeline
2. Pipeline uses point-in-time universe from Story 1.5 (Russell 1000 C&P) with cached data from Epic 1 over 5+ years
3. For each monthly rebalance date: get universe → calculate signals → rank → select deciles → construct overlapping portfolio (K=6)
4. Validation checks confirm: weights sum to zero (net neutral), gross exposure is 2.0, no individual weight exceeds reasonable threshold
5. Visualization shows time series of long/short counts (how many securities in each leg over time)
6. Visualization displays sample portfolio weights for 2-3 rebalance dates (top 10 longs, top 10 shorts)
7. Output saves portfolio weights to `results/` directory in CSV format for inspection
8. Documentation or notebook commentary explains the pipeline steps and validates outputs look reasonable
9. Pipeline completes for 5+ years of monthly rebalancing in under 30 seconds
