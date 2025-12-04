# ADR-007: JSON Files for Experiment Tracking

## Status

Accepted

## Context

The framework needs to track experiments for reproducibility (PRD Story 4.2):
- Strategy configuration (parameters)
- Performance metrics (CAGR, Sharpe, etc.)
- Metadata (timestamp, notes, git hash)

Storage options considered:

| Option | Complexity | Query | Human Readable | Concurrent |
|--------|------------|-------|----------------|------------|
| **JSON files** | Low | Poor | Excellent | Good |
| **SQLite** | Medium | Excellent | Poor | Good |
| **CSV** | Low | Poor | Good | Poor |
| **MLflow** | High | Excellent | Medium | Excellent |

Key requirements:
- Simple for single-user research tool
- Human-readable for inspection
- No server to manage
- Sufficient for ~100s of experiments

## Decision

We will use **JSON files** for experiment tracking.

File organization:
```
data/results/experiments/
├── 20250115_143022_abc123.json
├── 20250115_150045_def456.json
└── ...
```

File naming: `{YYYYMMDD}_{HHMMSS}_{short_hash}.json`

Schema:
```json
{
  "experiment_id": "20250115_143022_abc123",
  "created_at": "2025-01-15T14:30:22Z",
  "config": {
    "lookback_months": 12,
    "skip_months": 1,
    ...
  },
  "metrics": {
    "cagr": 0.0823,
    "sharpe_ratio": 0.661,
    ...
  },
  "notes": "Baseline 12-1 momentum",
  "git_hash": "a1b2c3d"
}
```

## Consequences

**Positive:**
- Zero setup - just write files
- Human readable - can inspect with any text editor
- Version control friendly (can commit experiments)
- No database server to manage
- Simple to backup (file copy)

**Negative:**
- No SQL queries (must load all files to filter)
- Performance degrades with 1000s of experiments
- No schema enforcement (validation in code)
- Concurrent writes need care (unlikely for single user)

**Migration path:**
- If JSON becomes unwieldy, migrate to SQLite
- JSON schema makes migration straightforward
- `ExperimentTracker` class abstracts storage

**Acceptable for MVP:**
- Expected ~100s of experiments, not 1000s
- Single user eliminates concurrency concerns
- Query needs are simple (list, filter by date)
