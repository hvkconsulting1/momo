# ADR-010: Story-Based Test Organization for AI Agent Workflows

## Status

Accepted

## Context

Traditional test organization structures tests by layer or module (e.g., `tests/unit/data/`, `tests/unit/signals/`), grouping multiple related tests in files like `test_momentum.py` or `test_cache.py`. This approach optimizes for human browsing and logical grouping but creates friction for AI agent workflows:

### Problems with Traditional Organization

1. **Merge Conflicts in Parallel Development**
   - Multiple agents working on the same story edit the same test file
   - File-level locks prevent true parallel execution
   - Manual conflict resolution required

2. **Ambiguous Test ID → File Mapping**
   - Test ID `1.1-UNIT-012` could be in `test_imports.py`, `test_structure.py`, or `test_environment.py`
   - Agents must search/grep docstrings to locate tests
   - No deterministic mapping from test design document to test file

3. **Lifecycle Mismatch**
   - Story complete → Tests scattered across multiple files
   - Cannot easily archive/deprecate story tests as a unit
   - Tests for deprecated features remain mixed with active tests

4. **Traceability Gaps**
   - Test design documents define test IDs (e.g., `1.1-UNIT-001`)
   - No 1:1 mapping between test ID and file path
   - Hard to verify all test IDs implemented

### Project Context

This project is explicitly designed for AI-agent-first development:
- Slash commands (`/develop-story`, `/atomic-commit`) automate story-based workflows
- Test design documents define test IDs before implementation
- Multiple agents will work in parallel on atomic commits
- Story-based development model (Epic → Story → Atomic Commits → Test IDs)

### Options Considered

1. **Traditional Layer-Based** (`tests/unit/{layer}/test_{module}.py`)
   - ✅ Fewer files, easier human browsing
   - ❌ Merge conflicts, ambiguous test location, lifecycle mismatch

2. **Story-Based with Multiple Tests Per File** (`tests/stories/{story}/test_{module}.py`)
   - ✅ Story-level organization
   - ❌ Still has merge conflicts, still ambiguous within file

3. **Story-Based with One Test Per File** (`tests/stories/{story}/{level}/{test-id}.py`)
   - ✅ Deterministic test ID → file mapping
   - ✅ Zero merge conflicts (one test per file)
   - ✅ Story lifecycle = test lifecycle
   - ❌ More files (21 tests = 21 files for Story 1.1)

## Decision

We will adopt **story-based test organization with one test per file** (Option 3).

### Directory Structure

```
tests/
├── conftest.py                          # Global fixtures
├── pytest.ini                           # Pytest configuration
├── stories/                             # Story-based organization
│   ├── {story-id}/                      # e.g., 1.1/, 2.1/
│   │   ├── conftest.py                 # Story-specific fixtures
│   │   ├── README.md                   # Story test documentation
│   │   ├── unit/
│   │   │   ├── {story-id}-UNIT-{seq}.py    # e.g., 1.1-UNIT-001.py
│   │   │   └── ...
│   │   ├── integration/
│   │   │   ├── {story-id}-INT-{seq}.py
│   │   │   └── ...
│   │   └── e2e/
│   │       └── {story-id}-E2E-{seq}.py
│   └── TEST_REGISTRY.md                # Auto-generated test ID → file mapping
├── fixtures/                            # Shared test data
└── utils/                               # Test utilities
```

### File Naming Convention

**Pattern**: `{story-id}-{LEVEL}-{seq}.py`
- `story-id`: Story number (e.g., `1.1`, `2.3`)
- `LEVEL`: `UNIT`, `INT`, `E2E`
- `seq`: Zero-padded 3-digit sequence (e.g., `001`, `042`)

**Examples**:
- `1.1-UNIT-001.py` - Story 1.1, Unit test #1
- `2.3-INT-015.py` - Story 2.3, Integration test #15

### Test Function Naming

**Pattern**: `test_{story}_{level}_{seq}()`

**Examples**:
- `test_1_1_unit_001()` - Primary test function
- `test_1_1_unit_001_edge_case_empty()` - Optional variant

### Deterministic Mapping

Test ID from test design document maps directly to file path:
- Test ID `1.1-UNIT-001` → `tests/stories/1.1/unit/1.1-UNIT-001.py`
- Test ID `2.1-INT-003` → `tests/stories/2.1/integration/2.1-INT-003.py`

No search required. No ambiguity.

### Fixture Hierarchy

1. **Global fixtures** (`tests/conftest.py`) - Project-wide paths
2. **Story fixtures** (`tests/stories/{story}/conftest.py`) - Story-specific data
3. **Test fixtures** (inline) - Test-specific setup

### Test Discovery

```bash
# All tests for a story
pytest tests/stories/1.1/ -v

# Single test by ID
pytest tests/stories/1.1/unit/1.1-UNIT-001.py -v

# All P0 tests
pytest -m p0 -v

# All integration tests
pytest tests/stories/*/integration/ -v
```

## Consequences

### Positive Consequences

**For AI Agents:**
1. **Deterministic File Mapping** - Test ID → File path is a pure function
2. **Zero Coordination Overhead** - Parallel agents never collide on file edits
3. **Clear Ownership** - Each test ID has exactly one file
4. **Lifecycle Alignment** - Story done → `rm -rf tests/stories/{story}/`
5. **Precise Error Reporting** - "Test 1.1-INT-003 failed" → exact file path
6. **Perfect Traceability** - Test design doc line → test file (1:1 mapping)

**For Human Developers:**
1. **Story Focus** - See all tests for a story in one directory
2. **Atomic Code Review** - Each test file is independent, easy to review
3. **Debugging** - Run single test by ID with zero ambiguity
4. **Test Lifecycle** - Deprecate story → delete test directory

**For CI/CD:**
1. **Granular Execution** - Run by story, priority, test level, or test ID
2. **Parallel Execution** - GitHub Actions matrix strategy by story (no conflicts)
3. **Clear Reporting** - Test failures map to exact files
4. **Coverage Tracking** - Per-story coverage reports

### Negative Consequences

**File Count Explosion:**
- 21 tests for Story 1.1 = 21 files (vs ~3-5 traditional files)
- Large projects could have 1000+ test files
- **Mitigation**: Story-level organization prevents flat directory; pytest handles large file counts efficiently; modern tools (`fd`, `ripgrep`) search fast

**Human Browsing Difficulty:**
- Can't easily see "all data layer tests" across stories
- More navigation required to explore test organization
- **Mitigation**: Use pytest markers (`pytest -m data_layer`); maintain `TEST_REGISTRY.md` with tags; VS Code test explorer

**Test Discovery Performance:**
- pytest collecting 1000 files slower than 50 files
- **Mitigation**: Run tests by story in CI (only collect that story's tests); use pytest-xdist parallel collection; measured impact negligible for <500 files

**Shared Test Logic:**
- Multiple tests needing same helper function
- **Mitigation**: Use story-level `conftest.py` for story-specific helpers; use `tests/utils/` for cross-story helpers; prefer small duplication over coupling

### Trade-offs Accepted

**We accept:**
- More files (21 vs 5 per story)
- Harder human browsing by layer
- Slightly slower test discovery

**In exchange for:**
- Zero merge conflicts in parallel AI agent workflows
- Deterministic test ID → file mapping
- Perfect traceability from test design to implementation
- Story lifecycle alignment

### Migration Strategy

**Phase 1: Story 1.1 (Current)**
- Implement story-based organization immediately
- Validate approach through first story

**Phase 2: All Future Stories**
- All new stories use story-based organization
- Refine patterns based on Story 1.1 learnings

**Phase 3: Continuous Improvement**
- Generate `TEST_REGISTRY.md` automatically in CI
- Add pytest markers for cross-story organization views
- Measure and optimize test discovery performance

### Related Documentation

- **Test Strategy**: `docs/architecture/test-strategy-and-standards.md`
- **Test Environment Design**: `docs/test-environment-design.md`
- **Source Tree**: `docs/architecture/source-tree.md`
- **Coding Standards**: `docs/architecture/coding-standards.md`

### Success Criteria

This decision succeeds if:
1. ✅ AI agents can implement tests without search/grep
2. ✅ Zero merge conflicts when 3+ agents work on same story
3. ✅ Test lifecycle matches story lifecycle (easy to archive)
4. ✅ Traceability: Every test ID in test design has corresponding file
5. ✅ CI execution time remains acceptable (<10 minutes for full suite)

This decision fails if:
1. ❌ Test discovery time becomes prohibitive (>30s for collection)
2. ❌ Human developers cannot effectively navigate tests
3. ❌ File count management becomes unwieldy

**Review Date**: After Story 1.1 completion (validate approach with real-world data)

---
