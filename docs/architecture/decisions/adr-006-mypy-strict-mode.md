# ADR-006: mypy Strict Mode for Type Checking

## Status

Accepted

## Context

The user specifically requested "mypy strict typing for quant trading type accuracy."

For quantitative finance code, type precision matters:
- `float` vs `int` in return calculations
- `pd.DataFrame` vs `pd.Series` distinctions
- Preventing `None` propagation in signal chains
- Documenting expected shapes and dtypes

Options considered:
1. **No type checking** - Fast development but error-prone
2. **mypy basic** - Catches obvious errors
3. **mypy strict** - Maximum type safety
4. **pyright** - Alternative type checker

## Decision

We will use **mypy in strict mode** for all source code.

Configuration (`mypy.ini`):
```ini
[mypy]
python_version = 3.13
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true

[mypy-pandas.*]
ignore_missing_imports = true

[mypy-numpy.*]
ignore_missing_imports = true
```

All public functions must have complete type annotations:
```python
def calculate_momentum(
    prices_df: pd.DataFrame,
    lookback_months: int = 12,
    skip_months: int = 1,
) -> pd.DataFrame:
    ...
```

## Consequences

**Positive:**
- Catches type errors before runtime
- Documents function interfaces
- Prevents None propagation bugs
- AI agents can understand expected types
- IDE autocomplete works better

**Negative:**
- Pandas/numpy stubs are incomplete (requires `ignore_missing_imports`)
- Initial setup overhead for existing code
- Some valid patterns require `# type: ignore`
- Slower feedback loop (must run mypy)

**Trade-offs:**
- Strict mode is worth the overhead for financial calculations
- Third-party library stubs are imperfect but improving
- CI enforces type checking on all PRs
