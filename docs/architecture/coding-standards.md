# Coding Standards

## Core Standards

| Item | Value |
|------|-------|
| **Language & Runtime** | Python 3.13 (strict type hints required) |
| **Style & Linting** | ruff |
| **Type Checking** | mypy strict mode |
| **Test Organization** | Story-based: `tests/stories/{story-id}/{level}/{test-id}.py` |

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| DataFrame variables | Suffix `_df` | `prices_df` |
| Series variables | Suffix `_s` | `returns_s` |
| Date variables | Suffix `_date` | `start_date` |
| Config dataclasses | Suffix `Config` | `StrategyConfig` |
| Test fixtures | Prefix `sample_` | `sample_prices_df` |
| Test files | `{story}-{LEVEL}-{seq}.py` | `1.1-UNIT-001.py` |
| Test functions | `test_{story}_{level}_{seq}()` | `test_1_1_unit_001()` |

## Critical Rules

1. **Pure Functions in Signal/Portfolio Layers** - No I/O, no mutation of inputs
2. **Always Use structlog** - Never `print()` or stdlib `logging`
3. **DataFrame Schema Documentation** - Document columns and dtypes in docstrings
4. **Explicit Date Handling** - Use `datetime.date`, not strings
5. **No Magic Numbers** - Name all constants or use config
6. **Validate at Layer Boundaries** - Data layer validates; inner layers trust input
7. **Test File Naming** - `{story-id}-{LEVEL}-{seq}.py` (e.g., `1.1-UNIT-001.py`)
8. **Test Function Naming** - `test_{story}_{level}_{seq}()` (primary function in each file)
9. **One Test Per File Principle** - Each test ID gets exactly one file for deterministic AI agent mapping
10. **No Relative Imports Across Layers** - Use absolute imports from `momo`

## Code Review Guidelines

### Review Checklist

Before approving any code change, verify:

| Category | Check |
|----------|-------|
| **Correctness** | Logic matches acceptance criteria; edge cases handled |
| **Type Safety** | All functions have type hints; mypy passes with no errors |
| **Testing** | Test IDs from test design doc implemented; test file naming correct; coverage maintained |
| **Pure Functions** | Signal/Portfolio layer functions have no side effects |
| **Documentation** | Docstrings for public functions; DataFrame schemas documented |
| **Naming** | Follows conventions (`_df`, `_s`, `_date` suffixes) |
| **Logging** | Uses structlog, not print(); appropriate log levels |
| **Error Handling** | Uses custom exceptions from `momo.utils.exceptions` |

### Review Process

1. **Self-Review First** - Author reviews own code before requesting review
2. **CI Must Pass** - All checks (ruff, mypy, pytest) green before review
3. **Atomic Changes** - Each PR addresses one logical change
4. **Descriptive Commits** - Follow conventional commit format

### Layer-Specific Review Focus

| Layer | Primary Review Focus |
|-------|---------------------|
| **Data** | Validation logic, caching correctness, bridge error handling |
| **Signals** | Mathematical correctness, pure functions, vectorization |
| **Portfolio** | Weight constraints, exposure normalization, edge cases |
| **Backtest** | Return calculation accuracy, metric formulas, reproducibility |
| **Utils** | Configuration validation, logging setup, exception hierarchy |

### Review Workflow

```
1. Author creates PR with description linking to story
2. CI runs automatically (lint, type check, tests)
3. Reviewer checks against layer-specific focus areas
4. Author addresses feedback
5. Reviewer approves when all checks pass
6. Author merges (squash for clean history)
```

---
