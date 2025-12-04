# Source Tree

```
momo/
├── .github/
│   └── workflows/
│       └── ci.yml                    # GitHub Actions CI pipeline
│
├── data/
│   ├── cache/
│   │   ├── prices/                   # Cached price Parquet files
│   │   ├── constituents/             # Cached constituent Parquet files
│   │   └── universes/                # Cached universe snapshots (point-in-time)
│   └── results/
│       └── experiments/              # Experiment JSON records
│
├── docs/
│   ├── prd.md                        # Product Requirements Document
│   ├── architecture.md               # This document
│   ├── research/
│   │   └── norgate-api-exploration.md
│   └── stories/                      # User stories for development
│
├── notebooks/
│   ├── 01_data_exploration.ipynb     # Explore Norgate data
│   ├── 02_signal_development.ipynb   # Develop momentum signals
│   ├── 03_backtest_analysis.ipynb    # Run and analyze backtests
│   ├── 04_parameter_sweep.ipynb      # Compare strategy variants
│   └── scratch/                      # Temporary exploration notebooks
│
├── src/
│   └── momo/                         # Main package
│       ├── __init__.py
│       ├── py.typed                  # PEP 561 marker for type hints
│       │
│       ├── data/                     # Data Layer
│       │   ├── __init__.py
│       │   ├── bridge.py
│       │   ├── norgate.py
│       │   ├── cache.py
│       │   ├── loader.py
│       │   ├── universe.py           # Point-in-time universe construction
│       │   └── validation.py
│       │
│       ├── signals/                  # Signal Layer
│       │   ├── __init__.py
│       │   ├── momentum.py
│       │   └── ranking.py
│       │
│       ├── portfolio/                # Portfolio Layer
│       │   ├── __init__.py
│       │   ├── construction.py
│       │   └── rebalance.py
│       │
│       ├── backtest/                 # Backtest Layer
│       │   ├── __init__.py
│       │   ├── engine.py
│       │   ├── metrics.py
│       │   ├── visualization.py
│       │   └── comparison.py
│       │
│       └── utils/                    # Utils Layer
│           ├── __init__.py
│           ├── config.py
│           ├── experiment.py
│           ├── logging.py
│           ├── exceptions.py
│           └── types.py
│
├── tests/
│   ├── conftest.py                   # Global fixtures (project_root, etc.)
│   ├── pytest.ini                    # Pytest configuration
│   │
│   ├── stories/                      # Story-based test organization
│   │   ├── 1.1/                     # Story 1.1: Initialize Project Structure
│   │   │   ├── conftest.py          # Story-specific fixtures
│   │   │   ├── README.md            # Story test suite documentation
│   │   │   ├── unit/
│   │   │   │   ├── 1.1-UNIT-001.py # Verify top-level directories
│   │   │   │   ├── 1.1-UNIT-002.py # Verify data/ subdirectories
│   │   │   │   └── ...
│   │   │   └── integration/
│   │   │       ├── 1.1-INT-001.py  # uv sync resolves dependencies
│   │   │       └── ...
│   │   │
│   │   ├── 2.1/                     # Story 2.1: Norgate Data Bridge
│   │   │   ├── conftest.py
│   │   │   ├── README.md
│   │   │   ├── unit/
│   │   │   └── integration/
│   │   │
│   │   └── TEST_REGISTRY.md         # Auto-generated test ID → file mapping
│   │
│   ├── fixtures/                     # Shared test data
│   │   ├── sample_prices.parquet
│   │   └── mock_norgate_responses.json
│   │
│   └── utils/                        # Test utilities (not tests themselves)
│       ├── __init__.py
│       ├── assertions.py             # Custom assertion helpers
│       ├── factories.py              # Test data factories
│       └── mocks.py                  # Mock object builders
│
├── scripts/
│   ├── refresh_cache.py
│   └── run_backtest.py
│
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
├── ruff.toml
├── mypy.ini
├── pytest.ini
└── README.md
```

---
