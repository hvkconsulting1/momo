# Architecture Update Summary

**Date:** 2025-12-03
**Trigger:** PRD alignment with Jegadeesh & Titman (1993) baseline methodology (commit `2025b08`)

## Overview

This document summarizes the architecture updates made to align with the revised PRD requirements, specifically the addition of point-in-time universe construction and overlapping portfolios mechanism.

## New Architecture Decision Records

### ADR-008: Overlapping Portfolio State Management

**Decision:** Backtest engine manages overlapping portfolio state, not Portfolio layer.

**Key Points:**
- Engine maintains `active_subportfolios: dict[date, pd.DataFrame]` during backtest execution
- At each rebalance date, engine calls pure `equal_weight_portfolio()` to create new sub-portfolio
- Engine averages K active sub-portfolios to produce composite weights
- Preserves pure function architecture in Portfolio layer (ADR-004 compliance)
- Default K=6 reduces turnover from 100% to ~17% monthly

**Files Created:**
- `docs/architecture/decisions/adr-008-overlapping-portfolio-state-management.md`

### ADR-009: Point-in-Time Universe Construction

**Decision:** Create new `data/universe.py` module for point-in-time universe construction.

**Key Points:**
- Function `get_point_in_time_universe()` returns eligible tickers at specific date
- Default universe: Russell 1000 Current & Past (~1000 large/mid-cap stocks)
- Minimum history filter: 12 months (configurable)
- Universe snapshots cached to Parquet: `data/cache/universes/{index_name}/{YYYY-MM-DD}.parquet`
- Eliminates both survivorship bias and look-ahead bias

**Files Created:**
- `docs/architecture/decisions/adr-009-point-in-time-universe-construction.md`

## Architecture Document Updates

### 1. source-tree.md

**Changes:**
- Added `universe.py` module to Data Layer
- Added `data/cache/universes/` directory for cached universe snapshots

**Location:** `docs/architecture/source-tree.md`

### 2. components.md

**Changes:**
- Added new component: `src/data/universe.py` - Point-in-Time Universe Construction
  - Interfaces: `get_point_in_time_universe()`, `get_index_constituents_at_date()`, `filter_minimum_history()`, `cache_universe_snapshot()`, `load_universe_snapshot()`
  - Dependencies: `norgate.py`, `cache.py`

- Updated component: `src/backtest/engine.py` - Return Calculation Engine
  - Added responsibility: "Manage overlapping portfolio state for K-month holding periods"
  - New interfaces: `run_backtest_with_overlapping()`, `_average_subportfolios()`, `_prune_expired_subportfolios()`

- Updated component diagram (Mermaid):
  - Added `UNI[universe.py]` node to Data Layer
  - Added dependencies: `LDR --> UNI`, `UNI --> NOR`, `UNI --> CAC`

**Location:** `docs/architecture/components.md`

### 3. data-models.md

**Changes:**
- Updated `StrategyConfig` data model with new fields:
  - `holding_months: int` - Overlapping portfolio holding period K (default: 6)
  - `min_history_months: int` - Minimum price history required for universe inclusion (default: 12)
  - Updated `universe` default: "Russell 1000 Current & Past" (was "S&P 500")

**Location:** `docs/architecture/data-models.md`

### 4. high-level-architecture.md

**Changes:**
- Updated **Primary Data Flow**:
  - Before: `Norgate API → Windows Bridge → Parquet Cache → pandas DataFrames → Signals → Weights → Returns → Metrics`
  - After: `Norgate API → Windows Bridge → Parquet Cache → **Universe Construction** → pandas DataFrames → Signals → Weights (K sub-portfolios) → **Composite Weights** → Returns → Metrics`

- Updated **High Level Project Diagram** (Mermaid):
  - Added `Universe[Point-in-Time Universe]` node to Data Layer
  - Updated data flow: `Cache --> Universe --> Validate --> Momentum`

- Updated **Architectural and Design Patterns** table:
  - Added: **Point-in-Time Universe** pattern
  - Added: **Overlapping Portfolios** pattern

**Location:** `docs/architecture/high-level-architecture.md`

### 5. core-workflows.md

**Changes:**
- Updated **Workflow 2: Full Backtest Execution** sequence diagram:
  - Added `UNI as universe.py` participant
  - Added new phase: "Universe Construction Phase" with loop calling `get_point_in_time_universe()` for each rebalance date
  - Updated "Backtest Execution Phase" to show overlapping portfolio mechanism:
    - Now calls `run_backtest_with_overlapping()`
    - Notes: "Engine maintains K=6 active sub-portfolios" and "Averages sub-portfolios to composite weights"

**Location:** `docs/architecture/core-workflows.md`

### 6. decisions/README.md

**Changes:**
- Added ADR-008 and ADR-009 to ADR Index table

**Location:** `docs/architecture/decisions/README.md`

## Impact Summary

### New Modules Required
- `src/momo/data/universe.py` - Point-in-time universe construction

### Modified Modules (Interfaces Extended)
- `src/momo/backtest/engine.py` - Add overlapping portfolio functions
- `src/momo/utils/config.py` - Add `holding_months` and `min_history_months` to `StrategyConfig`

### New Data Storage
- `data/cache/universes/{index_name}/{YYYY-MM-DD}.parquet` - Cached universe snapshots

### Testing Implications
- Unit tests for `universe.py`: point-in-time queries, minimum history filtering
- Unit tests for overlapping portfolio helpers: `_average_subportfolios()`, `_prune_expired_subportfolios()`
- Integration tests: verify K=6 produces ~17% turnover vs ~100% for K=1
- Validation tests: compare results against J&T (1993) benchmarks

## Alignment with PRD

| PRD Story | Architecture Coverage | Status |
|-----------|----------------------|--------|
| Story 1.5: Point-in-Time Universe Construction | ADR-009, `universe.py` module, updated data flow | ✅ Complete |
| Story 2.3: Overlapping Portfolios | ADR-008, `engine.py` extensions, state management documented | ✅ Complete |
| FR4: K-month holding periods | `holding_months` in StrategyConfig | ✅ Complete |
| FR7: Russell 1000 C&P default | Updated universe default in data models | ✅ Complete |
| NFR6: Test overlapping mechanics | Testing implications documented in ADR-008 | ✅ Complete |

## Next Steps for Implementation

1. **Implement `src/momo/data/universe.py`** following ADR-009 specification
2. **Extend `src/momo/backtest/engine.py`** with overlapping portfolio functions per ADR-008
3. **Update `src/momo/utils/config.py`** to add `holding_months` and `min_history_months` to `StrategyConfig`
4. **Create unit tests** for universe construction and overlapping portfolio helpers
5. **Create integration tests** comparing K=1 vs K=6 turnover characteristics
6. **Validation testing** against known academic results (J&T 1993)

## Files Modified

1. `docs/architecture/decisions/adr-008-overlapping-portfolio-state-management.md` (new)
2. `docs/architecture/decisions/adr-009-point-in-time-universe-construction.md` (new)
3. `docs/architecture/decisions/README.md` (updated)
4. `docs/architecture/source-tree.md` (updated)
5. `docs/architecture/components.md` (updated)
6. `docs/architecture/data-models.md` (updated)
7. `docs/architecture/high-level-architecture.md` (updated)
8. `docs/architecture/core-workflows.md` (updated)
9. `docs/architecture/ARCHITECTURE_UPDATE_SUMMARY.md` (new - this file)

---

**Architecture Review Status:** ✅ **Complete and Aligned with PRD**

All critical gaps identified during the architecture review have been addressed. The architecture now fully supports the Jegadeesh & Titman (1993) baseline methodology requirements.
