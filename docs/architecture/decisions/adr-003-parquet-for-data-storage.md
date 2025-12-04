# ADR-003: Parquet for Data Storage

## Status

Accepted

## Context

The framework needs to cache market data locally for:
- Fast iteration without repeated API calls (PRD NFR1, NFR7)
- Reproducible backtests with consistent data
- Offline operation when Norgate is unavailable

Storage options considered:

| Option | Read Speed | Write Speed | pandas Integration | Query Flexibility |
|--------|------------|-------------|-------------------|-------------------|
| **Parquet** | Excellent | Good | Native | Limited |
| **SQLite** | Good | Good | Requires conversion | Excellent |
| **CSV** | Poor | Good | Native | None |
| **HDF5** | Excellent | Excellent | Native | Limited |
| **Feather** | Excellent | Excellent | Native | None |

Key requirements:
- Time-series financial data (columnar access patterns)
- Direct pandas DataFrame integration
- No server to manage
- Good compression for multi-year datasets

## Decision

We will use **Apache Parquet** as the primary storage format for cached data.

File organization:
```
data/cache/
├── prices/
│   ├── sp500.parquet
│   └── russell1000.parquet
└── constituents/
    ├── sp500_constituents.parquet
    └── russell1000_constituents.parquet
```

Configuration:
```python
df.to_parquet(
    path,
    engine="pyarrow",
    compression="snappy",  # Fast read/write
    index=False,           # Store as columns
)
```

## Consequences

**Positive:**
- Columnar format ideal for "get all closes" operations
- Native pandas integration (`pd.read_parquet()`)
- Excellent compression (snappy) for financial data
- No server or connection management
- Files are portable and human-inspectable (with tools)
- pyarrow provides fast read performance

**Negative:**
- No SQL queries (must load into pandas first)
- Schema changes require re-caching
- Not suitable for frequent small updates (batch-oriented)
- Requires pyarrow dependency

**Neutral:**
- Single file per universe is sufficient for expected data sizes
- No partitioning needed for MVP (~2.5M rows max)
