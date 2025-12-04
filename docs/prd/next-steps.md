# Next Steps

## UX Expert Prompt

The portfolio-momentum framework is a code-first research environment, so traditional UI/UX design is minimal. However, the "user experience" centers on Jupyter notebook workflows and data visualization. If UX architecture is needed, use this prompt:

---

**UX/Design Expert - Create UI/UX Architecture**

Using the attached Product Requirements Document (PRD) for the **portfolio-momentum** research framework, please create a comprehensive UI/UX architecture focused on the Jupyter notebook-based research workflow.

**Context:**
This is not a traditional GUI application - it's a Python research framework where users interact through Jupyter notebooks, visualizations, and markdown documentation. The "UX" is the research workflow experience.

**Key Focus Areas:**

1. **Research Workflow Design**
   - Map out the user journey from hypothesis → experiment → analysis → insights
   - Define notebook template structures (already outlined in Epic 4, Story 4.1)
   - Design visual language for charts (matplotlib/seaborn styling guidelines)

2. **Visualization Standards**
   - Define consistent chart styling (colors, fonts, layouts) for publication-quality outputs
   - Create examples of equity curves, drawdown charts, performance comparisons
   - Ensure colorblind-friendly palettes

3. **Information Architecture**
   - Document directory structure and file organization
   - Design research log structure (markdown format)
   - Define naming conventions for experiments and results

4. **Interaction Patterns**
   - Define configuration patterns (dataclasses vs dicts for strategy parameters)
   - Design error message and logging patterns
   - Specify how users navigate between data exploration, backtesting, and comparison

**Deliverables:**
- Research workflow diagram (user journey from hypothesis to insights)
- Visualization style guide (chart templates, color schemes, typography)
- Notebook template wireframes (showing structure and interaction patterns)
- File organization and naming conventions guide

**Reference PRD Sections:**
- User Interface Design Goals (code-first research environment vision)
- Epic 4: Research Workflow & Experimentation Tools
- Technical Assumptions (Jupyter notebooks, matplotlib/seaborn/plotly)

---

## Architect Prompt

**Software Architect - Create Technical Architecture**

Using the attached Product Requirements Document (PRD) for the **portfolio-momentum** quantitative research framework, please create a comprehensive technical architecture document that will guide development.

**Project Overview:**
A modular Python framework for researching and backtesting momentum trading strategies, starting with V1 cross-sectional momentum (12-1 Jegadeesh & Titman). The framework emphasizes learning through implementation, reproducibility, and extensibility.

**Your Task:**
Design the complete technical architecture covering:

1. **System Architecture**
   - Detailed layered architecture design (Data, Signal, Portfolio, Backtest, Risk layers)
   - Module responsibilities and interfaces between layers
   - Data flow from Norgate API → cached Parquet → signals → portfolio weights → backtest results
   - Dependency injection and composition patterns for extensibility

2. **Data Architecture**
   - Pandas DataFrame structures for price data, signals, portfolio weights, returns
   - Parquet file organization and naming conventions for caching
   - Handling of point-in-time constituents and corporate actions
   - Data validation pipeline design

3. **Key Module Design**
   - **Data Layer:** Norgate API integration, caching strategy, validation pipeline
   - **Signal Layer:** Pure function design for momentum calculations, ranking, selection
   - **Portfolio Layer:** Weight calculation, exposure normalization, rebalancing logic
   - **Backtest Layer:** Return calculation engine, performance metrics, visualization suite
   - **Utils Layer:** Experiment tracking, configuration management, logging

4. **Testing Strategy**
   - Unit test approach for pure functions (signal calculations, portfolio construction)
   - Integration test design for end-to-end backtests
   - Validation test approach (compare against known benchmarks)
   - Test data strategies (synthetic data, fixtures)

5. **Performance Optimization**
   - Pandas/numpy vectorization patterns to meet NFR1 (<1 min for 30yr × 500 securities)
   - Parquet caching strategy for fast iteration
   - Memory management for large datasets
   - Profiling and optimization approach

6. **Configuration & Extensibility**
   - Strategy configuration design (dataclasses, YAML, or dict-based)
   - Plugin architecture for new signal types
   - Template pattern for portfolio construction methods
   - Adding new performance metrics

7. **Error Handling & Logging**
   - Exception handling patterns (data quality issues, missing API credentials, calculation errors)
   - Logging strategy (Python logging module configuration)
   - User-facing error messages in notebooks

8. **Development Workflow**
   - Package structure enabling `import src` from project root
   - uv (Astral) dependency management setup
   - pytest configuration and test discovery
   - Code quality tools (ruff/pylint configuration)

**Critical Requirements to Address:**
- **NFR1:** Backtest performance <1 minute for 30 years × 500 securities
- **NFR2:** Clear separation of concerns across layers
- **NFR3:** Extensibility - new strategies without modifying core engine
- **NFR4:** Pure functions for reproducibility (deterministic, no side effects)
- **NFR7:** Offline operation with cached data
- **NFR8:** Survivorship bias elimination via point-in-time constituents

**Key Technical Decisions Needed:**
1. Pandas DataFrame index design (datetime index? MultiIndex for tickers × dates?)
2. Parquet file organization (single file vs sharded? by date range? by universe?)
3. Configuration approach (dataclass vs YAML vs dict) - recommend with rationale
4. Experiment tracking storage (JSON files vs SQLite) - recommend with rationale
5. Pure function enforcement (static type checking? runtime validation?)

**Deliverables:**
1. **Architecture Overview Document** with layered architecture diagram
2. **Module Design Specifications** for each layer (Data, Signal, Portfolio, Backtest, Utils)
3. **Data Structures & Schemas** (DataFrame formats, Parquet organization, config schemas)
4. **API/Interface Definitions** (function signatures for key modules with docstring examples)
5. **Technical Decision Log** (rationale for key architecture choices)
6. **Development Setup Guide** (package structure, dependency management, testing configuration)

**Reference PRD Sections:**
- Technical Assumptions (repository structure, architecture, tech stack, performance targets)
- All Epic/Story Acceptance Criteria (especially Epic 1 for data infrastructure)
- Requirements (FR1-FR13, NFR1-NFR10)

**Note:** This is a personal research project, so avoid over-engineering. Prioritize clarity, simplicity, and extensibility over enterprise-scale patterns. The architecture should support learning and experimentation.
