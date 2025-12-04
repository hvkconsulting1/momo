# ADR-009: Point-in-Time Universe Construction

## Status

Accepted

## Context

The PRD (Story 1.5) requires point-in-time universe construction to eliminate both survivorship bias and look-ahead bias in backtests. This is foundational to implementing the Jegadeesh & Titman (1993) baseline methodology with academic rigor.

**Key Requirements:**
- Construct investable universe at each rebalance date using point-in-time index constituents
- Default universe: Russell 1000 Current & Past (~1000 large/mid-cap stocks)
- Apply minimum history filter: only include securities with ≥12 months of price data
- Handle delisted securities correctly (include until delisting, exclude after)
- Cache universe snapshots for performance and reproducibility
- Support configurable universe selection (Russell 1000, Russell 3000, S&P 500)

**Bias Elimination:**
1. **Survivorship Bias:** Using Norgate "Current & Past" watchlists includes delisted securities (e.g., Lehman Brothers pre-2008)
2. **Look-Ahead Bias:** Point-in-time universe ensures only historically available stocks are candidates (no future information leak)
3. **Insufficient Data Bias:** Minimum history filter prevents using securities with incomplete momentum lookback

**Architectural Questions:**
- Where does universe construction fit in the data layer?
- How do we efficiently query "What were Russell 1000 constituents on 2010-06-30?"
- How do we cache universe snapshots for fast backtest iteration?
- What interfaces does this expose to downstream layers?

## Decision

**Create a new `src/data/universe.py` module in the Data Layer for point-in-time universe construction.**

Implementation approach:

1. **New Module: `src/data/universe.py`**
   - Sits between `cache.py` and signal generation
   - Depends on `norgate.py` (for constituent queries) and `cache.py` (for snapshot storage)
   - Provides pure function interface for universe construction

2. **Core Function:**
   ```python
   def get_point_in_time_universe(
       index_name: str,
       as_of_date: date,
       min_history_months: int = 12,
       force_refresh: bool = False
   ) -> list[str]:
       """
       Get eligible securities for the universe at specific date.

       Returns symbols that:
       1. Were index members as of as_of_date (point-in-time constituents)
       2. Have >= min_history_months of price data before as_of_date
       3. Were not delisted before as_of_date

       Results cached to Parquet for fast retrieval.
       """
   ```

3. **Supporting Functions:**
   ```python
   def get_index_constituents_at_date(
       index_name: str,
       as_of_date: date
   ) -> list[str]:
       """Query Norgate for point-in-time index membership"""
       # Uses norgate.get_index_constituents()
       ...

   def filter_minimum_history(
       symbols: list[str],
       min_months: int,
       as_of_date: date
   ) -> list[str]:
       """Remove symbols with insufficient price history"""
       # Queries cache for price data availability
       ...

   def cache_universe_snapshot(
       symbols: list[str],
       index_name: str,
       as_of_date: date,
       metadata: dict
   ) -> Path:
       """Save universe snapshot to Parquet"""
       # Stored at: data/cache/universes/{index_name}/{YYYY-MM-DD}.parquet
       ...

   def load_universe_snapshot(
       index_name: str,
       as_of_date: date
   ) -> list[str] | None:
       """Load cached universe snapshot if exists"""
       ...
   ```

4. **Data Flow Integration:**
   - **Before signals:** Universe construction happens during backtest initialization
   - **Per rebalance date:** Engine calls `get_point_in_time_universe()` to determine eligible securities
   - **Price loading:** Only fetch/cache prices for universe-valid tickers
   - **Signal calculation:** Only calculate signals for securities in point-in-time universe

5. **Caching Strategy:**
   - Universe snapshots stored as Parquet: `data/cache/universes/{index_name}/{YYYY-MM-DD}.parquet`
   - Schema: `symbol: str, added_date: date, removed_date: date | None, history_months: int`
   - Cache invalidation: Manual only (universe membership rarely changes retroactively)
   - Performance: Single read per rebalance date vs hundreds of API calls

6. **Configuration:**
   - Add `universe: str = "Russell 1000 Current & Past"` to `StrategyConfig`
   - Add `min_history_months: int = 12` to `StrategyConfig`
   - Supports easy parameter sweeps: different universes or history requirements

## Consequences

**Positive:**
- **Eliminates look-ahead bias:** Only historically available securities are candidates
- **Eliminates survivorship bias:** Norgate "Current & Past" includes delistings
- **Modular design:** Isolated in dedicated module with clear responsibility
- **Performance:** Caching prevents repeated API calls (NFR1 compliance)
- **Reproducibility:** Cached snapshots ensure identical universe across backtest runs
- **Extensibility:** Easy to add new universes (Russell 3000, NASDAQ 100) without touching core logic
- **Testability:** Pure functions with known inputs/outputs (e.g., verify LEH in Russell 1000 pre-2008)

**Negative:**
- **Cold-start cost:** First backtest run requires fetching constituent history (one-time ~1-2 minutes)
- **Storage overhead:** Universe snapshots add ~100KB per rebalance date (~30MB for 30 years monthly)
- **API dependency:** Requires Norgate constituent time series (available in Platinum subscription)
- **Complexity:** Additional module and data flow step to understand

**Neutral:**
- **12-month minimum history:** Matches momentum signal lookback; automatically excludes IPOs/recent listings
- **Russell 1000 default:** Matches J&T (1993) large/mid-cap universe; ~1000 stocks balances diversification and liquidity
- **Configurable universe:** Enables experimentation (small-cap with Russell 3000) without architecture changes

**Implementation Notes:**

1. **Norgate API Integration:**
   - Use `norgate.get_index_constituents(symbol, index, start_date, end_date)` (already in components.md)
   - Returns DataFrame with constituent membership over time
   - Bridge pattern handles WSL → Windows NDU communication

2. **Edge Cases:**
   - **Newly added constituents:** Included only after they meet min_history requirement
   - **Delisted securities:** Included up to delisting date, excluded after (Norgate provides delisting dates)
   - **Gaps in membership:** Stock delisted and relisted → treat as separate inclusion periods
   - **IPOs:** Automatically excluded until min_history_months of data available

3. **Testing Strategy:**
   - **Unit tests:** Verify filtering logic with synthetic constituent/price data
   - **Integration tests:** Query real Norgate data for known historical date (e.g., 2008-09-15 should include LEH)
   - **Validation tests:** Compare universe counts to published index statistics
   - **Edge case tests:** Delisting handling, insufficient history, newly added stocks

4. **Performance Optimization:**
   - Batch-load constituent time series once per backtest (not per rebalance date)
   - Cache price data availability lookup (avoid repeated filesystem checks)
   - Pre-compute universe for all rebalance dates during backtest initialization
   - Target: Universe construction for 30 years monthly rebalances in <30 seconds (Story 1.5 AC#12)

**Relationship to Other ADRs:**
- **ADR-003 (Parquet Storage):** Universe snapshots use Parquet for consistency
- **ADR-004 (Pure Functions):** `get_point_in_time_universe()` is pure (deterministic given inputs)
- **ADR-002 (Windows Bridge):** Norgate constituent queries routed through bridge pattern
