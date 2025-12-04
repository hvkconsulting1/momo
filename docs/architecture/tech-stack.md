# Tech Stack

This section defines the **definitive technology choices** for the project. All other documents and implementation must reference these selections.

## Cloud Infrastructure

| Item | Value |
|------|-------|
| **Provider** | Local (WSL2 on Windows) |
| **Deployment Target** | Personal development machine |
| **Future Consideration** | AWS/GCP for paper trading phase (post-MVP) |

## Technology Stack Table

| Category | Technology | Version | Purpose | Rationale |
|----------|------------|---------|---------|-----------|
| **Language** | Python | 3.13 | Primary development language | Modern Python with full type hints; already initialized per git history |
| **Runtime** | CPython | 3.13 | Python interpreter | Standard interpreter; best ecosystem compatibility |
| **Package Manager** | uv (Astral) | 0.5+ | Dependency management | Fast, reliable; already initialized per PRD; replaces pip/poetry |
| **Data Processing** | pandas | 2.2.x | DataFrame operations, time series | Industry standard for financial data; vectorized operations |
| **Data Processing** | numpy | 2.1.x | Numerical computations | Foundation for pandas; required for vectorized calculations |
| **Data Processing** | pyarrow | 18.x | Parquet read/write | Required for pandas Parquet support; fast columnar storage |
| **Statistics** | scipy | 1.14.x | Statistical functions | Performance metrics, distributions |
| **Statistics** | statsmodels | 0.14.x | Time series analysis | Regression, statistical tests for validation |
| **Data Source** | norgatedata | 1.0.74 | Norgate Data API | Required for market data access; Windows-only (WSL accesses via subprocess bridge) |
| **Visualization** | matplotlib | 3.9.x | Static charts, equity curves | Publication-quality figures; Jupyter integration |
| **Visualization** | seaborn | 0.13.x | Statistical visualizations | Better defaults than matplotlib; heatmaps |
| **Interactive** | jupyter | 4.x | Research notebooks | Primary research interface per PRD |
| **Interactive** | jupyterlab | 4.x | Enhanced notebook IDE | Better UX than classic notebook |
| **Testing** | pytest | 8.x | Test framework | Industry standard; fixtures, parametrize |
| **Testing** | pytest-cov | 5.x | Coverage reporting | Track test coverage on critical paths |
| **Testing** | pytest-xdist | 3.5.x | Parallel test execution | Fast test runs across CPU cores; critical for parameter sweep validation |
| **Linting** | ruff | 0.7.x | Linting + formatting | Fast, replaces flake8/black/isort |
| **Type Checking** | mypy | 1.13.x | Static type analysis (strict mode) | Quant accuracy requires precise types; catch numeric/DataFrame errors early |
| **Logging** | structlog | 24.x | Structured logging | JSON-formatted logs for AI agent troubleshooting; context preservation across pipeline stages |
| **Retry Logic** | tenacity | 9.x | Retry with backoff | Resilient Norgate API calls via bridge |

---
