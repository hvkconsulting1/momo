# ADR-001: Layered Pipeline Architecture

## Status

Accepted

## Context

The portfolio-momentum framework needs an architecture that:
- Supports clear separation of concerns (PRD NFR2)
- Enables independent testing of components (PRD NFR6)
- Allows new momentum strategies without modifying core engine (PRD NFR3)
- Maintains reproducibility through deterministic data flow (PRD NFR4)

We considered several architectural approaches:
1. **Monolithic script** - Simple but poor separation, hard to test
2. **Microservices** - Overkill for single-user local tool
3. **Plugin architecture** - Flexible but complex for MVP
4. **Layered pipeline** - Clear boundaries, unidirectional flow

## Decision

We will use a **layered pipeline architecture** with five discrete layers:

```
Data → Signal → Portfolio → Backtest → Risk
```

Each layer:
- Has a single responsibility
- Depends only on layers to its left (unidirectional)
- Exposes pure functions with well-defined interfaces
- Can be tested independently

The layers are implemented as separate Python subpackages:
- `src/momo/data/` - Norgate integration, caching, validation
- `src/momo/signals/` - Momentum calculation, ranking
- `src/momo/portfolio/` - Weight construction, rebalancing
- `src/momo/backtest/` - Return engine, metrics, visualization
- `src/momo/utils/` - Cross-cutting concerns (config, logging, exceptions)

## Consequences

**Positive:**
- Clear mental model for developers and AI agents
- Each layer can be tested with mocked inputs from previous layers
- New signal types (time-series momentum) require only new signal module
- Data flow is traceable through the pipeline
- Supports functional programming style with pure functions

**Negative:**
- Some boilerplate in passing data between layers
- Cannot easily skip layers (must flow through pipeline)
- Cross-cutting concerns require separate utils layer

**Neutral:**
- Requires discipline to maintain layer boundaries
- AI agents must understand which layer a component belongs to
