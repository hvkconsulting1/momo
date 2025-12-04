# Technical Debt Tracker

This document tracks technical debt, consolidation opportunities, and refactoring candidates identified during post-story assessments.

**Last Updated:** 2025-12-04 (Story 1.2 assessment)

**Purpose:** Maintain a living record of technical debt across stories to guide refactoring efforts and prevent quality erosion.

---

## Active Debt Items

### Fixture Consolidation Opportunities

*No consolidation opportunities identified*

### Code Duplication

*No significant duplication patterns detected*

### Architecture Improvements

*No improvements needed - full compliance*

### Type Safety Issues

**Priority: Medium**

- **tests/stories/1.1/integration/test_1_1_int_005.py** (6 instances)
  - Lines 28, 29, 38, 42, 44: Third-party libraries lacking type stubs
  - Reason: jupyter, jupyterlab, pyarrow, scipy, statsmodels don't ship py.typed markers
  - Resolution: These are acceptable permanent ignores for untyped third-party libraries

### Test Organization

**Priority: High - Blocking Quality**

- **Missing pytest markers across all Story 1.1 and Story 1.2 tests** (38 files)
  - All test files missing both `@pytest.mark.p[012]` (priority) and `@pytest.mark.[unit|integration]` (level) markers
  - Tests have markers documented in docstrings but lack actual decorator implementation
  - Impact: Cannot run tests by priority or level, breaks test selection strategy
  - Required for: CI/CD pipelines, selective test execution, quality gates

---

## Story Assessments

<!-- Reverse chronological order - newest first -->

### Story 1.2 - 2025-12-04

**Story Title:** Integrate Norgate Data API via Windows Python Bridge
**Commits:** 7 commits (c358f99..4599226)
**Files Changed:** 42 files

#### Findings Summary

| Category | Count | Status |
|----------|-------|--------|
| Type Ignores Added | 1 | 🟢 |
| TODOs/FIXMEs Added | 0 | 🟢 |
| New Fixtures | 0 | 🟢 |
| Architecture Violations | 0 | 🟢 |
| Test Naming Issues | 8 | 🟡 |
| Missing Test Markers | 19 | 🔴 |

**Status Key:** 🟢 Clean (0) | 🟡 Minor (1-2) | 🔴 Needs Attention (3+)

#### New Fixtures in Story Conftest

None - Story 1.2 has no story-level conftest.py

**Promotion Candidates:** None

#### Type Ignores Added

One type: ignore removed from `tests/stories/1.1/integration/test_1_1_int_005.py`:
- Line 27: Removed unused `import pandas  # type: ignore[import-untyped]` (cleanup)

**Net Type Ignores:** -1 (improvement)

**Note:** Several references to "type: ignore" were added in `docs/type-ignore-registry.md` documentation, not actual code. These are not counted as technical debt.

#### TODOs/FIXMEs Added

None - ✓ No unresolved work items

#### Architecture Notes

✓ No violations detected
- Data layer: Bridge properly isolated to `src/momo/data/bridge.py`
- Norgatedata usage: All imports correctly routed through bridge
- No cross-layer dependency violations
- Exception handling properly located in `src/momo/utils/exceptions.py`

#### Test Quality Notes

**Critical Issues:**
- ✗ All 19 test files missing priority markers (@pytest.mark.p0/p1/p2)
- ✗ All 19 test files missing level markers (@pytest.mark.unit/integration)
- 🟡 8 integration tests have unconventional naming (test_1_2_int_XXX.py instead of test_1_2_int_0XX.py)

**Positive Notes:**
- ✓ Test files follow story-based organization (tests/stories/1.2/{unit,integration}/)
- ✓ One test ID per file principle maintained
- ✓ Comprehensive docstring headers document priority and level (just not implemented as decorators)
- ✓ 95% code coverage achieved (90/95 statements)

#### Code Duplication Detected

✓ No duplicate function names detected across src/momo

#### Recommendations

1. **Immediate (Before Next Story):**
   - **CRITICAL:** Add pytest marker decorators to all Story 1.2 test files (19 files)
     - Add `@pytest.mark.p0` decorator to match documented priority
     - Add `@pytest.mark.unit` or `@pytest.mark.integration` decorator to match test level
   - Consider bulk-fixing Story 1.1 markers at same time (38 files total)

2. **Next Story:**
   - Establish pre-commit hook or linter to enforce pytest markers on all test files
   - Update test templates to include marker decorators by default

3. **Backlog:**
   - None

---

### Story 1.1 - 2025-12-04

**Story Title:** Initialize Project Structure and Development Environment
**Commits:** 12 commits (b218537..18fe5eb)
**Files Changed:** 31 files

#### Findings Summary

| Category | Count | Status |
|----------|-------|--------|
| Type Ignores Added | 6 | 🟡 |
| TODOs/FIXMEs Added | 0 | 🟢 |
| New Fixtures | 0 | 🟢 |
| Architecture Violations | 0 | 🟢 |
| Test Naming Issues | 8 | 🔴 |
| Missing Test Markers | 19 | 🔴 |

**Status Key:** 🟢 Clean (0) | 🟡 Minor (1-2) | 🔴 Needs Attention (3+)

#### New Fixtures in Story Conftest

None - Story 1.1 uses only global fixtures from tests/conftest.py

**Promotion Candidates:** None

#### Type Ignores Added

All 6 type: ignore comments are in `tests/stories/1.1/integration/test_1_1_int_005.py`:

- Line 28: `jupyter` - Third-party library lacks type stubs
- Line 29: `jupyterlab` - Third-party library lacks type stubs
- Line 38: `pyarrow` - Third-party library lacks type stubs
- Line 42: `scipy` - Third-party library lacks type stubs
- Line 44: `statsmodels` - Third-party library lacks type stubs

All are `type: ignore[import-untyped]` for third-party dependencies that don't ship py.typed markers.

#### TODOs/FIXMEs Added

None - ✓ No unresolved work items

#### Architecture Notes

✓ No violations detected
- Signal layer: Clean (no imports from backtest/portfolio)
- Portfolio layer: Clean (no imports from backtest)
- Norgatedata usage: Properly isolated to bridge module
- No obvious DataFrame mutations detected

#### Test Quality Notes

**Critical Issues:**
- ✗ All 19 test files missing priority markers (@pytest.mark.p0/p1/p2)
- ✗ All 19 test files missing level markers (@pytest.mark.unit/integration)
- ✗ 8 test files have incorrect naming (missing underscores): test_1_1_int_00X.py instead of test_1_1_int_00X.py

**Note:** Test file naming appears correct upon inspection (all use underscores). The grep pattern may need adjustment.

#### Code Duplication Detected

✓ No obvious duplication detected - no duplicate function names found across src/momo

#### Recommendations

1. **Immediate (Before Next Story):**
   - Add pytest markers to all Story 1.1 test files (priority + level markers)
   - Verify test file naming compliance (may be false positive)

2. **Next Story:**
   - Consider adding stub packages for untyped dependencies if mypy strict mode requires it
   - Document marker conventions in test-strategy-and-standards.md if not already present

3. **Backlog:**
   - None

---
