# Technical Debt Tracker

This document tracks technical debt, consolidation opportunities, and refactoring candidates identified during post-story assessments.

**Last Updated:** 2025-12-05 (Story 1.4 assessment complete)

**Purpose:** Maintain a living record of technical debt across stories to guide refactoring efforts and prevent quality erosion.

---

## Active Debt Items

**Summary:** No actionable technical debt. All critical items resolved. Story 1.3 maintains excellent quality standards.

### Fixture Consolidation Opportunities

*No consolidation opportunities identified*

### Code Duplication

*No significant duplication patterns detected*

### Architecture Improvements

*No improvements needed - full compliance*

### Type Safety Issues

**Status: Acceptable (Not Actionable)**

- **tests/stories/1.1/integration/test_1_1_int_005.py** (6 instances)
  - Lines 28, 29, 38, 42, 44: Third-party libraries lacking type stubs
  - Reason: jupyter, jupyterlab, pyarrow, scipy, statsmodels don't ship py.typed markers
  - Resolution: These are acceptable permanent ignores for untyped third-party libraries
  - Action Required: None - industry-standard practice for missing type stubs

### Test Organization

**Status: ✅ RESOLVED (2025-12-04)**

- **pytest markers completed across all Story 1.1 and Story 1.2 tests** (38 files)
  - All test files now have both `@pytest.mark.p[012]` and `@pytest.mark.[unit|integration]` markers
  - Test selection by priority and level now functional
  - Verified: `pytest -m p0` and `pytest -m unit` work correctly
  - Unblocks: CI/CD pipelines, selective test execution, quality gates

---

## Story Assessments

<!-- Reverse chronological order - newest first -->

### Story 1.4 - 2025-12-05

**Story Title:** Build Data Quality Validation Pipeline
**Commits:** 12 commits (1ea69e1..1521762)
**Files Changed:** 31 files

#### Findings Summary

| Category | Count | Status |
|----------|-------|--------|
| Type Ignores Added | 3 | 🟢 |
| TODOs/FIXMEs Added | 0 | 🟢 |
| New Fixtures | 15 | 🟡 |
| Architecture Violations | 0 | 🟢 |
| Test Naming Issues | 0 | 🟢 |
| Missing Test Markers | 0 | 🟢 |

**Status Key:** 🟢 Clean (0) | 🟡 Minor (1-2) | 🔴 Needs Attention (3+)

#### New Fixtures in Story Conftest

Story 1.4 introduced `tests/stories/1.4/conftest.py` with 15 fixtures:
- `sample_price_df_clean()` - Clean multi-index price DataFrame (5 tickers, 10 days)
- `sample_price_df_with_nans_close()` - Price DataFrame with NaN in close column
- `sample_price_df_with_nans_ohlc()` - Price DataFrame with NaN across OHLC columns
- `sample_price_df_with_10day_gap()` - Price DataFrame with 10 business day gap
- `sample_price_df_with_weekends_missing()` - Price DataFrame excluding weekends (normal)
- `sample_price_df_with_july4_missing()` - Price DataFrame excluding July 4th holiday
- `sample_price_df_with_negative_price()` - Price DataFrame with negative price (invalid adjustment)
- `sample_price_df_with_50pct_jump_no_div()` - Price DataFrame with 50% jump without dividend
- `mock_bridge_response_russell1000()` - Mock Russell 1000 constituent list (~1000 tickers)
- `sample_price_df_with_aapl_split()` - Price DataFrame with AAPL 7:1 split (legitimate)
- `sample_price_df_with_enron_delisted()` - Price DataFrame with Enron delisting
- `sample_price_df_with_recent_delisting()` - Price DataFrame with recent delisting
- `mock_validation_report()` - Mock ValidationReport with various issues
- `sample_price_df_100tickers()` - Large price DataFrame (100 tickers × 252 days for performance testing)
- `cached_corrupt_test_data()` - Comprehensive corrupt data fixture with 4 known issues

**Promotion Candidates:**
- `sample_price_df_clean()` - Could be promoted to global conftest as a general-purpose clean price fixture. Similar to Story 1.3's `sample_price_df()` but with multi-index schema. Consider consolidating.

**Assessment:** Most fixtures are validation-specific test data (corrupt data, gaps, adjustment issues). The `sample_price_df_clean()` fixture is a potential promotion candidate for reuse across stories requiring clean price data.

#### Type Ignores Added

3 type: ignore comments added, all in **test files** (not production code):

**Location:**
- `tests/stories/1.4/unit/test_1_4_unit_018.py:27` - `# type: ignore[no-untyped-def]`
- `tests/stories/1.4/unit/test_1_4_unit_019.py:23` - `# type: ignore[no-untyped-def]`
- `tests/stories/1.4/unit/test_1_4_unit_020.py:24` - `# type: ignore[no-untyped-def]`

**Reason:** Test functions accept fixtures as parameters without explicit type annotations (pytest pattern)
**Plan:** Acceptable - test code pattern, fixtures have dynamic types inferred by pytest
**Status:** 🟢 Accepted

**Assessment:** All type ignores are in test code following standard pytest patterns for fixture injection. Production code (`src/momo/data/validation.py`) has zero type ignores - excellent type safety discipline maintained.

#### TODOs/FIXMEs Added

None - ✓ No unresolved work items

#### Architecture Notes

✓ No violations detected
- Data layer: Validation module properly isolated to `src/momo/data/validation.py`
- Bridge usage: New `fetch_index_constituent_timeseries()` function added to bridge.py (correct pattern)
- No cross-layer dependencies introduced
- Pure function requirements: N/A (data layer allows I/O)
- Exception handling: ValidationError properly added to `src/momo/utils/exceptions.py`

#### Test Quality Notes

✓ All tests properly structured and marked
- **25 tests implemented** (21 unit, 4 integration)
- ✅ All tests have priority markers (@pytest.mark.p0/p1/p2)
- ✅ All tests have level markers (@pytest.mark.unit/integration)
- ✅ All test files follow naming convention (test_1_4_{level}_{seq}.py)
- ✅ One test ID per file principle maintained
- ✅ Strong test coverage (89% for validation.py)

#### Code Duplication Detected

✓ No obvious duplication detected
- No duplicate function names found across src/momo
- Validation module is distinct and non-overlapping with existing code

#### Recommendations

1. **Immediate:**
   - None - implementation is production-ready

2. **Next Story:**
   - Consider promoting `sample_price_df_clean()` to global conftest if other stories need clean multi-index price data
   - Address FutureWarning in validation.py:308 (`pct_change()` fill_method deprecation)

3. **Backlog:**
   - None

---

### Story 1.3 - 2025-12-04

**Story Title:** Implement Data Loading and Parquet Caching
**Commits:** 8 commits (b0f35a7..95d3550)
**Files Changed:** 39 files

#### Findings Summary

| Category | Count | Status |
|----------|-------|--------|
| Type Ignores Added | 8 | 🟢 |
| TODOs/FIXMEs Added | 0 | 🟢 |
| New Fixtures | 3 | 🟢 |
| Architecture Violations | 0 | 🟢 |
| Test Naming Issues | 0 | 🟢 |
| Missing Test Markers | 0 | 🟢 |

**Status Key:** 🟢 Clean (0) | 🟡 Minor (1-2) | 🔴 Needs Attention (3+)

#### New Fixtures in Story Conftest

Story 1.3 introduced `tests/stories/1.3/conftest.py` with 3 fixtures:
- `sample_price_df()` - Creates sample OHLCV DataFrame for testing cache functions
- `invalid_schema_dfs()` - Provides dict of invalid schemas for validation tests
- `temp_cache_dir()` - Provides temporary cache directory (wraps pytest tmp_path)

**Promotion Candidates:**
- None - All fixtures are story-specific and not reusable across stories
- `sample_price_df` follows the price data schema but is tailored for cache testing
- `invalid_schema_dfs` is cache validation specific
- `temp_cache_dir` is a thin wrapper around pytest's tmp_path fixture

**Assessment:** Fixtures are appropriately scoped to story 1.3 testing needs. No promotion needed.

#### Type Ignores Added

8 type: ignore comments added, all in **test files** (not production code):

**Category 1: Third-Party Import Typing (3 instances)**
- `src/momo/data/cache.py:6` - `import pyarrow as pa  # type: ignore[import-untyped]`
- `src/momo/data/cache.py:7` - `import pyarrow.parquet as pq  # type: ignore[import-untyped]`
- `tests/stories/1.3/integration/test_1_3_int_*.py` (2 files) - `import pyarrow.parquet as pq  # type: ignore[import-untyped]`

**Reason:** pyarrow lacks type stubs (no py.typed marker) - same as Story 1.1
**Plan:** Permanent - third-party limitation
**Status:** 🟢 Accepted

**Category 2: Test Mock Functions (5 instances)**
- `tests/stories/1.3/unit/test_1_3_unit_018.py` (2 instances) - Mock functions with `# type: ignore[no-untyped-def]`
- `tests/stories/1.3/integration/test_1_3_int_010.py` (1 instance) - Mock function
- `tests/stories/1.3/integration/test_1_3_int_011.py` (2 instances) - Mock functions

**Reason:** Test mock functions use **kwargs without full type annotations (acceptable pattern for test mocks)
**Plan:** Acceptable - test code pattern, not production code
**Status:** 🟢 Accepted

**Assessment:** All type ignores are justified and follow best practices:
- Production code (cache.py, loader.py) only has third-party import ignores (unavoidable)
- Test mock functions use ignores appropriately (common pytest pattern)
- No type ignores for business logic or algorithms

#### TODOs/FIXMEs Added

None - ✓ No unresolved work items

#### Architecture Notes

✓ No violations detected
- Data layer: Cache and loader properly isolated to `src/momo/data/`
- No cross-layer dependencies introduced
- Pure function requirements: N/A (data layer allows I/O)
- Bridge usage: All Norgate calls correctly routed through `bridge.fetch_price_data()`
- Exception handling: New `DataError` and `CacheError` properly defined in `src/momo/utils/exceptions.py`

#### Test Quality Notes

✓ All tests properly structured and marked
- **30 tests implemented** (18 unit, 12 integration)
- ✅ All tests have priority markers (@pytest.mark.p0/p1/p2)
- ✅ All tests have level markers (@pytest.mark.unit/integration)
- ✅ All test files follow naming convention (test_1_3_{level}_{seq}.py)
- ✅ One test ID per file principle maintained
- ✅ Comprehensive test coverage (98% for cache.py and loader.py)

#### Code Duplication Detected

✓ No obvious duplication detected
- No duplicate function names found across src/momo
- Cache and loader modules are distinct and non-overlapping

#### Recommendations

1. **Immediate:**
   - None - implementation is production-ready

2. **Next Story:**
   - Continue current quality standards for Story 1.4 (Data Validation)
   - Consider adding type stubs for pyarrow if it becomes problematic (currently acceptable)

3. **Backlog:**
   - Batch fetching optimization (deferred from Story 1.3 scope, documented in loader.py)

---

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
| Missing Test Markers | 0 | 🟢 |

**Status Key:** 🟢 Clean (0) | 🟡 Minor (1-2) | 🔴 Needs Attention (3+)
**Update (2025-12-04):** ✅ All pytest markers added to Story 1.2 tests

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

**Critical Issues (Resolved):**
- ✅ All 19 test files now have priority markers (@pytest.mark.p0/p1/p2)
- ✅ All 19 test files now have level markers (@pytest.mark.unit/integration)
- 🟡 8 integration tests have unconventional naming (test_1_2_int_XXX.py instead of test_1_2_int_0XX.py) - non-blocking

**Positive Notes:**
- ✓ Test files follow story-based organization (tests/stories/1.2/{unit,integration}/)
- ✓ One test ID per file principle maintained
- ✓ Comprehensive docstring headers document priority and level (just not implemented as decorators)
- ✓ 95% code coverage achieved (90/95 statements)

#### Code Duplication Detected

✓ No duplicate function names detected across src/momo

#### Recommendations

1. **Immediate (Before Next Story):**
   - ✅ COMPLETED: pytest marker decorators added to all Story 1.2 test files (19 files)
   - ✅ COMPLETED: Story 1.1 markers also added (38 files total)

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
| Missing Test Markers | 0 | 🟢 |

**Status Key:** 🟢 Clean (0) | 🟡 Minor (1-2) | 🔴 Needs Attention (3+)
**Update (2025-12-04):** ✅ All pytest markers added to Story 1.1 tests

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

**Critical Issues (Resolved):**
- ✅ All 19 test files now have priority markers (@pytest.mark.p0/p1/p2)
- ✅ All 19 test files now have level markers (@pytest.mark.unit/integration)
- 🟡 8 test files have naming variations (test_1_1_int_00X.py) - non-blocking, naming is acceptable

**Note:** Test file naming is correct and follows conventions. All tests have proper decorators.

#### Code Duplication Detected

✓ No obvious duplication detected - no duplicate function names found across src/momo

#### Recommendations

1. **Immediate (Before Next Story):**
   - ✅ COMPLETED: pytest markers added to all Story 1.1 test files (priority + level markers)
   - ✅ COMPLETED: Test file naming verified as compliant

2. **Next Story:**
   - Establish pre-commit hook or linter to enforce pytest markers on all test files
   - Update test templates to include marker decorators by default

3. **Backlog:**
   - Consider adding stub packages for untyped dependencies if they become problematic (currently acceptable)

---
