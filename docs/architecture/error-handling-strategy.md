# Error Handling Strategy

## General Approach

| Item | Value |
|------|-------|
| **Error Model** | Exception-based with custom hierarchy |
| **Exception Hierarchy** | `MomoError` base class with layer-specific subclasses |
| **Error Propagation** | Fail fast at boundaries; let exceptions bubble up with context |

## Logging Standards

| Item | Value |
|------|-------|
| **Library** | structlog 24.x |
| **Format** | JSON (CI/scripts) / Console (interactive) |
| **Levels** | DEBUG, INFO, WARNING, ERROR, CRITICAL |

**Required Context:**
- `correlation_id` - UUID per operation
- `layer` - Component layer name
- `operation` - Current function/task
- `symbol` / `universe` - When applicable

## Error Handling Patterns

**External API Errors (Norgate Bridge):**
- 3 retry attempts with exponential backoff (1s, 2s, 4s)
- 30s timeout per symbol, 300s for full universe
- Bridge errors translated to `BridgeError` or `NDUNotAvailableError`

**Data Consistency:**
- Atomic file writes (tempfile + rename)
- Validation before caching
- Cache is idempotent (overwrite existing)

---
