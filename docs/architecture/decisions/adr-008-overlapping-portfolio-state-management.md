# ADR-008: Overlapping Portfolio State Management

## Status

Accepted

## Context

The PRD (Story 2.3) requires implementing overlapping portfolios to replicate the Jegadeesh & Titman (1993) methodology. This mechanism maintains K active sub-portfolios formed at different rebalance dates, with the final portfolio being an equal-weighted average of all active sub-portfolios.

**Key Requirements:**
- At each rebalance date t, maintain K active sub-portfolios (formed at months t, t-1, ..., t-K+1)
- Default holding period K=6 months reduces turnover from 100% to ~17% monthly
- Support configurable K values (1, 3, 6, 12) for experimentation
- Preserve reproducibility and testability

**Architectural Challenge:**
Overlapping portfolios require temporal state management (tracking K sub-portfolios across time), but our existing architecture (ADR-004) mandates pure functions in the Signal and Portfolio layers. We need to decide where this stateful logic belongs.

**Options Considered:**

1. **Portfolio Layer Manages State** - Add stateful `OverlappingPortfolioManager` class to `portfolio/construction.py`
   - ❌ Violates pure function principle (ADR-004)
   - ❌ Makes portfolio construction non-deterministic
   - ❌ Breaks independent testability of portfolio functions

2. **Backtest Engine Manages State** - Engine maintains K sub-portfolios, calls pure portfolio functions
   - ✅ Preserves pure function architecture
   - ✅ State management is temporal execution concern (belongs in Backtest layer)
   - ✅ Portfolio construction remains independently testable
   - ✅ Overlapping logic is backtest-specific, not portfolio-specific

3. **New Intermediate Layer** - Create "Portfolio Management" layer between Portfolio and Backtest
   - ❌ Adds unnecessary complexity
   - ❌ Violates YAGNI (we only need this for one use case)
   - ❌ Blurs responsibility boundaries

## Decision

**The backtest engine (`src/backtest/engine.py`) will manage overlapping portfolio state.**

Implementation approach:

1. **Portfolio Layer remains stateless:**
   - `equal_weight_portfolio()` generates weights for a single rebalance date (pure function)
   - Returns: `pd.DataFrame` with weights for one sub-portfolio

2. **Backtest Engine manages temporal composition:**
   - Engine maintains `active_subportfolios: dict[date, pd.DataFrame]` during backtest execution
   - At each rebalance date:
     - Calls pure `equal_weight_portfolio()` to create new sub-portfolio
     - Adds new sub-portfolio to active collection
     - Prunes sub-portfolios older than K months
     - Averages remaining K sub-portfolios to produce composite weights
   - Uses composite weights for return calculation

3. **Configuration:**
   - Add `holding_months: int = 6` to `StrategyConfig` dataclass
   - K=1 produces simple monthly rebalance (no overlapping)
   - K>1 activates overlapping portfolio logic

4. **New Engine Functions:**
   ```python
   def run_backtest_with_overlapping(
       signal_generator: Callable,
       portfolio_constructor: Callable,
       prices: pd.DataFrame,
       config: StrategyConfig
   ) -> BacktestResults:
       """Run backtest with K-month overlapping portfolios"""
       ...

   def _average_subportfolios(
       active_subportfolios: dict[date, pd.DataFrame]
   ) -> pd.DataFrame:
       """Compute equal-weighted average of active sub-portfolios"""
       ...

   def _prune_expired_subportfolios(
       active: dict[date, pd.DataFrame],
       current_date: date,
       holding_months: int
   ) -> dict[date, pd.DataFrame]:
       """Remove sub-portfolios older than holding period"""
       ...
   ```

## Consequences

**Positive:**
- Preserves pure function architecture in Portfolio layer (maintains ADR-004)
- Portfolio construction functions remain independently testable with fixed inputs
- Overlapping logic centralized in one place (backtest engine)
- Easy to test: K=1 (no overlap) vs K=6 (overlap) produces measurably different turnover
- Supports parameter sweeps on `holding_months` without touching Portfolio layer code

**Negative:**
- Backtest engine becomes slightly more complex (manages state)
- Engine must maintain sub-portfolio history during execution (memory overhead)
- Developers must understand that "weights" in engine are composite, not direct portfolio output

**Neutral:**
- Overlapping portfolio mechanism is invisible to Signal and Portfolio layers
- Notebooks can choose simple `run_backtest()` (K=1 implied) or explicit `run_backtest_with_overlapping()`
- Test coverage required: unit tests for averaging/pruning helpers, integration tests for full backtest with K=6

**Testing Implications:**
- Unit test `_average_subportfolios()` with known sub-portfolio DataFrames
- Unit test `_prune_expired_subportfolios()` with various date ranges and K values
- Integration test: verify K=6 produces ~17% monthly turnover vs ~100% for K=1
- Validation test: compare results against academic benchmarks (J&T 1993)

**Performance Considerations:**
- Minimal memory overhead: K=6 sub-portfolios × ~100 positions each = ~600 weight records in memory
- Averaging operation is O(K × N) where N = number of unique symbols across sub-portfolios
- Well within NFR1 performance target (<1 minute for 30 years × 500 securities)
