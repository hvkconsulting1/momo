# ADR-004: Pure Functions in Core Layers

## Status

Accepted

## Context

The PRD emphasizes reproducibility (NFR4): "Signal calculation functions must be pure (deterministic, no side effects) to ensure reproducible results."

For quantitative finance backtesting, reproducibility is critical:
- Same inputs must always produce same outputs
- Debugging requires traceable data flow
- Validation against known results needs determinism

We need to decide which parts of the codebase require pure functions and how to enforce this.

## Decision

We will **mandate pure functions** in the Signal and Portfolio layers:

**Pure function requirements:**
1. No I/O operations (file reads, network calls)
2. No mutation of input DataFrames (return new DataFrame)
3. No global state access or modification
4. No random operations without explicit seed parameter
5. Deterministic output for identical inputs

**Layers affected:**
- `src/momo/signals/` - All functions must be pure
- `src/momo/portfolio/` - All functions must be pure

**Layers exempt:**
- `src/momo/data/` - Requires I/O for Norgate/cache
- `src/momo/backtest/` - Visualization requires I/O
- `src/momo/utils/` - Logging, config are inherently stateful

**Enforcement:**
- Coding standards document the requirement
- Code review (AI and human) checks for violations
- No runtime enforcement for MVP

**Pattern:**
```python
# CORRECT - returns new DataFrame
def calculate_momentum(prices_df: pd.DataFrame) -> pd.DataFrame:
    result = prices_df.copy()
    result["momentum"] = ...
    return result

# WRONG - mutates input
def calculate_momentum(prices_df: pd.DataFrame) -> pd.DataFrame:
    prices_df["momentum"] = ...  # Mutation!
    return prices_df
```

## Consequences

**Positive:**
- Guaranteed reproducibility for signal/portfolio calculations
- Easy unit testing (no mocking required)
- Clear data flow for debugging
- AI agents can reason about function behavior
- Enables potential parallelization

**Negative:**
- Memory overhead from DataFrame copies
- Cannot use in-place optimizations
- Logging requires special handling (allowed as side effect)
- Requires developer discipline

**Trade-off accepted:**
- Memory overhead is acceptable for research workloads
- Logging is allowed because it doesn't affect computation
