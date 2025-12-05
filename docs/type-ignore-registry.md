# Type Ignore Registry

This document tracks all `type: ignore` comments in the codebase with justification and removal plans.

**Last Updated:** 2025-12-04 (Story 1.3 assessment)

**Purpose:** Every `type: ignore` comment represents a type safety gap. This registry ensures each one is justified, tracked, and has a plan for resolution or permanent acceptance.

**Policy:**
- All `type: ignore` comments must be registered here
- Each entry must have a justification
- Each entry must have a removal plan or permanent acceptance reason
- Entries should be resolved or permanently accepted within 2-3 stories

---

## Active Type Ignores

| Location | Added | Reason | Plan | Status |
|----------|-------|--------|------|--------|
| test_1_1_int_005.py:28 | Story 1.1 | jupyter lacks type stubs (no py.typed) | Permanent - third-party limitation | 🟢 Accepted |
| test_1_1_int_005.py:29 | Story 1.1 | jupyterlab lacks type stubs (no py.typed) | Permanent - third-party limitation | 🟢 Accepted |
| test_1_1_int_005.py:38 | Story 1.1 | pyarrow lacks type stubs (no py.typed) | Permanent - third-party limitation | 🟢 Accepted |
| test_1_1_int_005.py:42 | Story 1.1 | scipy lacks type stubs (no py.typed) | Permanent - third-party limitation | 🟢 Accepted |
| test_1_1_int_005.py:44 | Story 1.1 | statsmodels lacks type stubs (no py.typed) | Permanent - third-party limitation | 🟢 Accepted |
| cache.py:6 | Story 1.3 | pyarrow lacks type stubs (no py.typed) | Permanent - third-party limitation | 🟢 Accepted |
| cache.py:7 | Story 1.3 | pyarrow.parquet lacks type stubs | Permanent - third-party limitation | 🟢 Accepted |
| test_1_3_unit_018.py | Story 1.3 | Test mock functions (2×) | Acceptable - test pattern | 🟢 Accepted |
| test_1_3_int_010.py | Story 1.3 | Test mock function | Acceptable - test pattern | 🟢 Accepted |
| test_1_3_int_011.py | Story 1.3 | Test mock functions (2×) | Acceptable - test pattern | 🟢 Accepted |
| test_1_3_int_*.py (2 files) | Story 1.3 | pyarrow.parquet in tests | Acceptable - test imports | 🟢 Accepted |

---

## Story-by-Story Additions

<!-- Reverse chronological order - newest first -->

### Story 1.3 - 2025-12-04

**Context:** Data loading and Parquet caching implementation with comprehensive error handling and schema validation

**Net Change:** +8 type: ignore (all justified and acceptable)

**Production Code (src/momo/data/cache.py):**

| Location | Reason | Plan | Status |
|----------|--------|------|--------|
| cache.py:6 | `import pyarrow as pa  # type: ignore[import-untyped]` | Permanent - third-party limitation | 🟢 Accepted |
| cache.py:7 | `import pyarrow.parquet as pq  # type: ignore[import-untyped]` | Permanent - third-party limitation | 🟢 Accepted |

**Test Code:**

| Location | Reason | Plan | Status |
|----------|--------|------|--------|
| test_1_3_unit_018.py (2×) | Mock functions with `**kwargs` - `no-untyped-def` | Acceptable test pattern | 🟢 Accepted |
| test_1_3_int_010.py (1×) | Mock function with `**kwargs` - `no-untyped-def` | Acceptable test pattern | 🟢 Accepted |
| test_1_3_int_011.py (2×) | Mock functions with `**kwargs` - `no-untyped-def` | Acceptable test pattern | 🟢 Accepted |
| test_1_3_int_*.py (2 files) | `import pyarrow.parquet as pq  # type: ignore[import-untyped]` | Acceptable - test imports | 🟢 Accepted |

**Assessment:**
- **Production code:** Only 2 type ignores, both for unavoidable third-party import limitations (pyarrow lacks type stubs)
- **Test code:** 6 type ignores following standard pytest mock patterns
- **No type ignores for business logic** - Excellent type safety discipline
- All ignores use specific directives (`[import-untyped]`, `[no-untyped-def]`) - best practice
- Zero technical debt introduced

**Alternative Considered:** Could use `types-pyarrow` stub package, but pyarrow frequently changes APIs and stubs lag behind. Direct ignores are more pragmatic for this use case.

---

### Story 1.2 - 2025-12-04

**Context:** Windows Python bridge implementation with comprehensive error handling and retry logic

**Net Change:** -1 type: ignore (cleanup of unused import)

**Removed:**

| Location | Reason | Status |
|----------|--------|--------|
| test_1_1_int_005.py:27 | Removed unused `import pandas  # type: ignore[import-untyped]` | ✓ Cleaned up |

**Assessment:** Story 1.2 reduced technical debt by removing an unused type: ignore comment. No new type ignores were introduced in production code (`src/momo/`) or test code (`tests/stories/1.2/`). Excellent type safety discipline maintained.

---

### Story 1.1 - 2025-12-04

**Context:** Integration test validating core dependencies can be imported (Python 3.13 compatibility check)

All 6 type: ignore comments use the specific `type: ignore[import-untyped]` directive for third-party libraries that don't ship type stubs.

**Entries Added to Registry:**

| Location | Reason | Plan | Status |
|----------|--------|------|--------|
| test_1_1_int_005.py:28 | jupyter lacks py.typed marker | Permanent - upstream dependency limitation | 🟢 Accepted |
| test_1_1_int_005.py:29 | jupyterlab lacks py.typed marker | Permanent - upstream dependency limitation | 🟢 Accepted |
| test_1_1_int_005.py:38 | pyarrow lacks py.typed marker | Permanent - upstream dependency limitation | 🟢 Accepted |
| test_1_1_int_005.py:42 | scipy lacks py.typed marker | Permanent - upstream dependency limitation | 🟢 Accepted |
| test_1_1_int_005.py:44 | statsmodels lacks py.typed marker | Permanent - upstream dependency limitation | 🟢 Accepted |

**Assessment:** All type ignores are justified and acceptable. These are third-party libraries used only in tests for import validation. Using specific `type: ignore[import-untyped]` directive is best practice.

**Alternative Considered:** Could use `types-*` stub packages from typeshed, but these libraries are only imported for validation (not used), so ignores are more pragmatic.

---
