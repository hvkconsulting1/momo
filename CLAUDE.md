# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Momo is a momentum strategy backtesting framework built for AI-agent-first development. It uses a layered pipeline architecture for quantitative trading research with a strong emphasis on reproducibility, testability, and parallel development workflows.

## Development Commands

### Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/momo --cov-report=term-missing

# Run specific story tests
uv run pytest tests/stories/1.1/ -v

# Run single test by ID
uv run pytest tests/stories/1.1/unit/test_1_1_unit_001.py -v

# Run by priority marker
uv run pytest -m p0 -v       # Critical path tests only
uv run pytest -m p1 -v       # High priority tests
uv run pytest -m p2 -v       # Lower priority tests

# Run by test level marker
uv run pytest -m unit -v          # Fast unit tests
uv run pytest -m integration -v   # Integration tests

# Combine markers
uv run pytest -m "p0 and unit" -v
```

### Type Checking

```bash
# Type check package
uv run mypy src/

# Type check tests
uv run mypy tests/

# Type check both
uv run mypy src/ tests/
```

### Linting & Formatting

```bash
# Format code
uv run ruff format .

# Lint and auto-fix
uv run ruff check --fix .

# Lint only (no fixes)
uv run ruff check .
```

### Full Validation

```bash
# Run all checks (type, format, lint)
uv run mypy src/ tests/ && uv run ruff format . && uv run ruff check --fix .
```

## Architecture

### Layered Pipeline Architecture (ADR-001)

The codebase follows a strict layered pipeline with unidirectional data flow:

```
Data → Signal → Portfolio → Backtest → Utils
```

**Layer Responsibilities:**
- `src/momo/data/` - Norgate integration via Windows Python bridge, caching, validation
- `src/momo/signals/` - Momentum calculations and ranking (pure functions only)
- `src/momo/portfolio/` - Weight construction and rebalancing (pure functions only)
- `src/momo/backtest/` - Return engine, metrics, visualization
- `src/momo/utils/` - Cross-cutting concerns (logging, config, exceptions)

**Key Rules:**
- Each layer depends only on layers to its left
- Signal and Portfolio layers MUST use pure functions (no I/O, no mutations, deterministic)
- Use `df.copy()` before modifying DataFrames to maintain immutability

### Windows Python Bridge for Norgate Data (ADR-002)

Norgate Data is Windows-only and accessed via subprocess bridge on WSL:

```python
# Bridge pattern (see src/momo/data/bridge.py)
subprocess.run(["python.exe", "-c", norgate_code], ...)
```

**Key Points:**
- Bridge is isolated to `src/momo/data/bridge.py`
- All Norgate calls go through the bridge with retry logic
- Parquet caching eliminates repeated bridge calls
- Integration tests requiring NDU are marked and may be skipped in CI
- Windows Python must be in PATH on WSL

### Story-Based Test Organization (ADR-010)

Tests are organized by story with **one test ID per file** to enable parallel AI agent workflows:

```
tests/stories/{story-id}/{level}/test_{story}_{level}_{seq}.py
```

**File Naming Convention:**
- Test ID `1.1-UNIT-001` → `tests/stories/1.1/unit/test_1_1_unit_001.py`
- Test ID `2.3-INT-015` → `tests/stories/2.3/integration/test_2_3_int_015.py`

**Note:** A single test ID file can contain multiple test functions (e.g., testing different edge cases, variants, or related scenarios), but all functions within that file belong to that one test ID.

**Benefits:**
- Deterministic test ID → file path mapping (no search required)
- Zero merge conflicts when multiple agents work in parallel on different test IDs
- Story lifecycle matches test lifecycle
- Perfect traceability from test design to implementation

**Pytest Markers (REQUIRED):**

All test functions MUST have both markers:
1. **Priority marker:** `@pytest.mark.p0`, `@pytest.mark.p1`, or `@pytest.mark.p2`
2. **Level marker:** `@pytest.mark.unit` or `@pytest.mark.integration`

Example:
```python
import pytest

@pytest.mark.p0
@pytest.mark.unit
def test_1_2_unit_001() -> None:
    """Test critical functionality."""
    ...
```

**Priority Guidelines:**
- **P0:** Critical path - must pass before merge (core functionality, high-risk areas)
- **P1:** High priority - important but not blocking (edge cases, common scenarios)
- **P2:** Lower priority - nice to have (documentation tests, minor features)

**Fixture Hierarchy:**
1. Global fixtures: `tests/conftest.py`
2. Story fixtures: `tests/stories/{story}/conftest.py`
3. Test-specific fixtures: inline in test file

### Pure Functions in Core Layers (ADR-004)

Signal and Portfolio layers require pure functions for reproducibility:

**Requirements:**
- No I/O operations
- No mutation of input DataFrames (use `df.copy()`)
- No global state access
- No random operations without explicit seed
- Deterministic output for identical inputs

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

**Note:** Logging is allowed in pure functions as it doesn't affect computation.

## Story-Based Development Workflow

This project uses slash commands for AI-agent workflows:

- `/develop-story <story-number>` - Complete story development lifecycle
- `/atomic-commit <story-id> <commit-number>` - Execute single atomic commit with TDD
- `/plan-atomic-commits <story-file> <test-design-file>` - Generate commit plan

When implementing tests:
1. Test ID from test design maps directly to file path (deterministic mapping)
2. Use story-level conftest.py for shared fixtures
3. **REQUIRED:** Add both priority and level markers to ALL test functions:
   - Priority: `@pytest.mark.p0`, `@pytest.mark.p1`, or `@pytest.mark.p2`
   - Level: `@pytest.mark.unit` or `@pytest.mark.integration`
   - Both markers must be present on every test function

## Type Checking & Code Quality

- **Python Version:** 3.13+
- **Type Checking:** mypy strict mode enabled
- All functions must have type annotations
- All tests must pass mypy type checking
- Ruff is configured for line length 100, Python 3.13 target

## Working with Data

- Norgate Data requires NDU running on Windows
- On WSL, ensure `python.exe` is in PATH
- Price data is cached as Parquet files in `data/` (gitignored)
- Use `src/momo/data/bridge.py` for all Norgate API calls
- Never call norgatedata directly from WSL Python

## Common Pitfalls

1. **Don't mutate DataFrames in Signal/Portfolio layers** - Always use `df.copy()`
2. **Don't import norgatedata directly in WSL** - Use the bridge in `data/bridge.py`
3. **Don't mix test IDs in one file** - Each file should contain only test functions for a single test ID
4. **Don't skip type annotations** - Strict mypy mode is enforced
5. **Don't create cross-layer dependencies** - Respect unidirectional data flow
6. **Don't forget pytest markers** - ALL tests must have both `@pytest.mark.p[012]` and `@pytest.mark.[unit|integration]` markers
