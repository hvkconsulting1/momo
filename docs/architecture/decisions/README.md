# Architecture Decision Records

This directory contains Architecture Decision Records (ADRs) for the portfolio-momentum project.

## What is an ADR?

An ADR is a document that captures an important architectural decision made along with its context and consequences. We use the [Michael Nygard format](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions).

## ADR Index

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [ADR-001](adr-001-layered-pipeline-architecture.md) | Layered Pipeline Architecture | Accepted | 2025-01-28 |
| [ADR-002](adr-002-windows-python-bridge.md) | Windows Python Bridge for Norgate | Accepted | 2025-01-28 |
| [ADR-003](adr-003-parquet-for-data-storage.md) | Parquet for Data Storage | Accepted | 2025-01-28 |
| [ADR-004](adr-004-pure-functions-in-core-layers.md) | Pure Functions in Core Layers | Accepted | 2025-01-28 |
| [ADR-005](adr-005-structlog-for-logging.md) | structlog for Structured Logging | Accepted | 2025-01-28 |
| [ADR-006](adr-006-mypy-strict-mode.md) | mypy Strict Mode | Accepted | 2025-01-28 |
| [ADR-007](adr-007-json-for-experiment-tracking.md) | JSON for Experiment Tracking | Accepted | 2025-01-28 |
| [ADR-008](adr-008-overlapping-portfolio-state-management.md) | Overlapping Portfolio State Management | Accepted | 2025-12-03 |
| [ADR-009](adr-009-point-in-time-universe-construction.md) | Point-in-Time Universe Construction | Accepted | 2025-12-03 |
| [ADR-010](adr-010-story-based-test-organization.md) | Story-Based Test Organization for AI Agent Workflows | Accepted | 2025-12-03 |

## Creating a New ADR

1. Copy `adr-template.md` to `adr-NNN-title.md`
2. Fill in the sections:
   - **Status**: Proposed → Accepted/Deprecated/Superseded
   - **Context**: Why is this decision needed?
   - **Decision**: What are we doing?
   - **Consequences**: What are the trade-offs?
3. Add entry to the index table above
4. Submit for review

## ADR Lifecycle

```
Proposed → Accepted → [Deprecated | Superseded by ADR-NNN]
```

- **Proposed**: Under discussion, not yet decided
- **Accepted**: Decision made and in effect
- **Deprecated**: No longer relevant (technology removed)
- **Superseded**: Replaced by a newer ADR

## References

- [Documenting Architecture Decisions - Michael Nygard](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [ADR GitHub Organization](https://adr.github.io/)
