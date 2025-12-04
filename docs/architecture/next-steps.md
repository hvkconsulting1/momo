# Next Steps

## Immediate Actions

**1. Story Development**

The architecture is ready to support story implementation. Recommended sequence:

```
Epic 1: Foundation & Data Infrastructure
├── Story 1.1: Initialize Project Structure ← START HERE
├── Story 1.2: Integrate Norgate Data API
├── Story 1.3: Implement Data Loading and Caching
├── Story 1.4: Build Data Quality Validation
└── Story 1.5: End-to-End Data Pipeline Verification
```

**2. Project Scaffolding**

Create the directory structure before Story 1.1:

```bash
mkdir -p src/momo/{data,signals,portfolio,backtest,utils}
mkdir -p tests/{unit,integration,fixtures}
mkdir -p data/{cache/prices,cache/constituents,results/experiments}
mkdir -p notebooks/scratch
mkdir -p scripts
touch src/momo/__init__.py src/momo/py.typed
touch src/momo/{data,signals,portfolio,backtest,utils}/__init__.py
```

**3. Dependencies Installation**

```bash
uv add pandas numpy pyarrow scipy statsmodels matplotlib seaborn structlog tenacity
uv add --dev pytest pytest-cov pytest-xdist mypy ruff jupyterlab ipykernel
```

## Development Workflow

For each story:

1. **Read architecture sections** relevant to the story
2. **Create tests first** (TDD for signal/portfolio/backtest layers)
3. **Implement following coding standards** (pure functions, structlog, schema docs)
4. **Run validation**: `uv run pytest && uv run mypy src && uv run ruff check src`
5. **Update experiment tracker** if running backtests

## Architecture Document Usage

| Agent/Role | Key Sections |
|------------|--------------|
| **Dev Agent** | Components, Coding Standards, Source Tree |
| **QA Agent** | Test Strategy, Data Models, Workflows |
| **Any Agent** | Tech Stack (definitive versions), Error Handling |

**Note:** Coding standards in this document are **mandatory** for all AI agents.

## Post-MVP Roadmap

| Phase | Feature | Architecture Impact |
|-------|---------|---------------------|
| 2.0 | Transaction costs & slippage | Add to backtest engine |
| 2.1 | Time-series momentum | New signal module |
| 2.2 | Rank-weighted portfolios | New construction method |
| 3.0 | Paper trading | Add scheduling, broker API |
| 3.1 | Web dashboard | Separate frontend architecture needed |
