# ADR-005: structlog for Structured Logging

## Status

Accepted

## Context

The framework needs logging for:
- Debugging data pipeline issues
- Tracking backtest execution
- AI agent troubleshooting and maintenance

The user specifically requested "structlog for optimum AI agent troubleshooting and maintenance, since they are the ones building and maintaining this code."

Options considered:
1. **stdlib logging** - Built-in but verbose configuration, string formatting
2. **loguru** - Simple API but less structured output
3. **structlog** - Structured logging with JSON output, context binding

Key requirements:
- JSON output for AI agent parsing
- Human-readable console output for interactive development
- Context preservation across pipeline stages
- Easy to filter and search

## Decision

We will use **structlog** as the logging library with dual output modes.

Configuration:
```python
# JSON mode (CI, scripts, AI parsing)
structlog.configure(
    processors=[...JSONRenderer()]
)

# Console mode (interactive development)
structlog.configure(
    processors=[...ConsoleRenderer(colors=True)]
)
```

Usage pattern:
```python
from momo.utils.logging import get_logger

log = get_logger(__name__)
log.info("Loading universe", universe="S&P 500", symbols=500)
```

Required context fields:
- `layer` - Component layer (data, signals, portfolio, backtest)
- `operation` - Current function/task
- `correlation_id` - UUID for tracing operations

## Consequences

**Positive:**
- JSON output is directly parseable by AI agents
- Context binding tracks data through pipeline
- Consistent log format across all modules
- Easy to switch between human/machine readable
- Better than print() for production code

**Negative:**
- Additional dependency
- Slightly more verbose than print()
- Learning curve for context binding

**Rules established:**
- Never use `print()` except in CLI scripts
- Never use stdlib `logging` directly
- Always use `from momo.utils.logging import get_logger`
