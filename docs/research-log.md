# Research Log

This document tracks experiments, investigations, and learnings throughout the portfolio-momentum project development.

## How to Use This Log

1. **Add entries chronologically** - Newest entries at the top of each section
2. **Be specific** - Include parameters, data ranges, and quantitative results
3. **Document failures** - Failed experiments are valuable learning
4. **Link to notebooks** - Reference the notebook file for reproducibility
5. **Update technical debt** - Track known issues and improvement opportunities

---

## Experiment Log

### Template

```markdown
### [DATE] - [EXPERIMENT TITLE]

**Hypothesis:** What you expected to find

**Parameters:**
- Lookback: X months
- Skip: Y months
- Universe: [index name]
- Date range: YYYY-MM-DD to YYYY-MM-DD

**Results:**
- CAGR: X.X%
- Sharpe: X.XX
- Max Drawdown: X.X%

**Insights:** What you learned

**Next Steps:** Follow-up experiments or actions

**Notebook:** `notebooks/XX_experiment_name.ipynb`
```

### Entries

*(Add new entries below this line, newest first)*

---

## Technical Debt Register

Track known issues, shortcuts, and improvement opportunities. Review quarterly to prioritize remediation.

### Active Technical Debt

| ID | Date Added | Category | Description | Impact | Remediation | Priority |
|----|------------|----------|-------------|--------|-------------|----------|
| TD-001 | 2025-11-28 | Documentation | README.md needs setup instructions | New developers lack quick start | Populate during Story 1.1 | High |

### Debt Categories

- **Architecture** - Design decisions that may need revisiting
- **Performance** - Known bottlenecks or optimization opportunities
- **Testing** - Missing test coverage or test quality issues
- **Documentation** - Gaps in docs, outdated information
- **Code Quality** - Code that works but could be cleaner
- **Dependencies** - Outdated packages, security concerns

### Debt Lifecycle

```
1. IDENTIFY  - Add to register with description and impact
2. ASSESS    - Assign priority (High/Medium/Low) based on impact
3. PLAN      - Schedule remediation in appropriate epic/story
4. REMEDIATE - Fix the issue
5. CLOSE     - Move to "Resolved" section with resolution date
```

### Resolved Technical Debt

| ID | Date Added | Date Resolved | Description | Resolution |
|----|------------|---------------|-------------|------------|
| *(none yet)* | | | | |

---

## Investigation Spikes

### Completed Spikes

| Date | Topic | Outcome | Document |
|------|-------|---------|----------|
| 2025-11-25 | Norgate Data API Exploration | GO - Proceed with architecture | [norgate-api-exploration.md](research/norgate-api-exploration.md) |

### Planned Spikes

*(Add investigation topics that need research before implementation)*

---

## Key Learnings

Significant insights that should inform future development:

1. **Windows Python Bridge Pattern** (2025-11-25) - norgatedata cannot run in WSL; use subprocess to Windows python.exe with JSON serialization for data transfer.

2. **No Historical Market Cap** (2025-11-25) - Norgate provides only point-in-time market cap; use index membership (Russell 1000/2000/3000) as size proxy.

3. **Delisted Symbol Format** (2025-11-25) - Delisted symbols use `SYMBOL-YYYYMM` format (e.g., `LEHMQ-201203` for Lehman Brothers).

---

## Quarterly Review Checklist

Use this checklist each quarter to maintain the research log:

- [ ] Review and prioritize technical debt items
- [ ] Archive completed experiments older than 6 months
- [ ] Update key learnings with new insights
- [ ] Close resolved technical debt items
- [ ] Plan spikes for upcoming quarter
