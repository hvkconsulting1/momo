# Development Commands

## Type Checking

```bash
# Type check package
uv run mypy src/

# Type check tests
uv run mypy tests/
```

## Linting & Formatting

```bash
# Format code
uv run ruff format .

# Lint and auto-fix
uv run ruff check --fix .

# Lint only (no fixes)
uv run ruff check .
```

## Run All Checks

```bash
# Full validation
uv run mypy src/ tests/ && uv run ruff format . && uv run ruff check --fix .
```
