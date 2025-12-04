# Database Schema

This project uses **Parquet files** as the primary storage layer.

## Storage Location

```
data/
├── cache/
│   ├── prices/
│   │   ├── sp500.parquet
│   │   └── russell1000.parquet
│   └── constituents/
│       ├── sp500_constituents.parquet
│       └── russell1000_constituents.parquet
└── results/
    └── experiments/
        └── 20250115_143022_abc123.json
```

## Price Data Schema (`cache/prices/*.parquet`)

| Column | Type | Description |
|--------|------|-------------|
| `date` | `datetime64[ns]` | Trading date |
| `symbol` | `string` | Ticker symbol |
| `open` | `float64` | Opening price (adjusted) |
| `high` | `float64` | High price (adjusted) |
| `low` | `float64` | Low price (adjusted) |
| `close` | `float64` | Closing price (adjusted) |
| `volume` | `int64` | Trading volume |
| `unadjusted_close` | `float64` | Raw closing price |
| `dividend` | `float64` | Dividend amount |

## Constituent Data Schema (`cache/constituents/*.parquet`)

| Column | Type | Description |
|--------|------|-------------|
| `date` | `datetime64[ns]` | Trading date |
| `symbol` | `string` | Ticker symbol |
| `index_name` | `string` | Index identifier |
| `is_member` | `bool` | True if member on this date |

## Experiment Record Schema (`results/experiments/*.json`)

```json
{
  "experiment_id": "20250115_143022_abc123",
  "created_at": "2025-01-15T14:30:22Z",
  "config": { ... },
  "metrics": { ... },
  "notes": "...",
  "git_hash": "a1b2c3d"
}
```

---
