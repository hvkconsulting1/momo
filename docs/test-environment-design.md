# Test Environment Design: Story-Based Test Organization

**Date**: 2025-12-03
**Status**: Proposed
**Purpose**: AI-agent-optimized test organization for the momo project

---

## Executive Summary

This document proposes a **story-based test organization** where each test ID from the test design document maps to exactly one test file. This approach optimizes for:

1. **AI Agent Maintainability**: Perfect traceability, zero merge conflicts
2. **Atomic Operations**: Each test file is independently deployable
3. **Lifecycle Management**: Story-level test organization matches story-based development
4. **Execution Granularity**: Run/skip/debug individual tests by ID

**Key Principle**: Test organization mirrors product development organization (stories → test IDs → test files).

---

## Directory Structure

### Proposed Organization

```
tests/
├── conftest.py                          # Global fixtures (project_root, etc.)
├── pytest.ini                           # Pytest configuration
│
├── stories/                             # Story-based test organization
│   ├── 1.1/                            # Story 1.1: Initialize Project Structure
│   │   ├── conftest.py                 # Story-specific fixtures
│   │   ├── unit/
│   │   │   ├── 1.1-UNIT-001.py        # Verify top-level directories
│   │   │   ├── 1.1-UNIT-002.py        # Verify data/ subdirectories
│   │   │   ├── 1.1-UNIT-003.py        # Verify src/momo/ structure
│   │   │   ├── 1.1-UNIT-004.py        # Verify tests/ structure
│   │   │   ├── 1.1-UNIT-005.py        # Verify __init__.py files
│   │   │   ├── 1.1-UNIT-006.py        # Verify py.typed marker
│   │   │   ├── 1.1-UNIT-007.py        # Verify dependencies
│   │   │   ├── 1.1-UNIT-008.py        # Verify gitignore data/
│   │   │   ├── 1.1-UNIT-009.py        # Verify gitignore artifacts
│   │   │   ├── 1.1-UNIT-010.py        # Verify README exists
│   │   │   ├── 1.1-UNIT-011.py        # Verify README sections
│   │   │   ├── 1.1-UNIT-012.py        # Import momo succeeds
│   │   │   └── 1.1-UNIT-013.py        # Import subpackages
│   │   └── integration/
│   │       ├── 1.1-INT-001.py         # uv sync resolves dependencies
│   │       ├── 1.1-INT-002.py         # uv.lock up-to-date
│   │       ├── 1.1-INT-003.py         # git status excludes data/
│   │       ├── 1.1-INT-004.py         # Cross-directory imports
│   │       ├── 1.1-INT-005.py         # ruff check no config errors
│   │       ├── 1.1-INT-006.py         # mypy strict mode works
│   │       ├── 1.1-INT-007.py         # pytest discovery works
│   │       └── 1.1-INT-008.py         # pytest coverage works
│   │
│   ├── 2.1/                            # Story 2.1: Norgate Data Bridge
│   │   ├── conftest.py
│   │   ├── unit/
│   │   │   ├── 2.1-UNIT-001.py
│   │   │   └── ...
│   │   └── integration/
│   │       ├── 2.1-INT-001.py
│   │       └── ...
│   │
│   └── 3.1/                            # Story 3.1: Momentum Signal Core
│       ├── conftest.py
│       ├── unit/
│       │   └── ...
│       └── integration/
│           └── ...
│
├── fixtures/                            # Shared test data
│   ├── sample_prices.parquet
│   ├── sample_constituents.parquet
│   └── mock_norgate_responses.json
│
└── utils/                               # Test utilities (not tests themselves)
    ├── __init__.py
    ├── assertions.py                    # Custom assertion helpers
    ├── factories.py                     # Test data factories
    └── mocks.py                         # Mock object builders
```

### Traditional Structure (for comparison)

```
tests/
├── conftest.py
├── unit/
│   ├── data/
│   │   ├── test_bridge.py              # Multiple tests mixed together
│   │   ├── test_norgate.py
│   │   └── test_cache.py
│   ├── signals/
│   │   └── test_momentum.py
│   └── ...
└── integration/
    ├── test_environment.py              # Multiple unrelated tests
    ├── test_tooling.py
    └── ...
```

---

## File Naming Convention

### Test File Naming

**Pattern**: `{story-id}-{test-level}-{sequence}.py`

- `story-id`: Story number (e.g., `1.1`, `2.3`, `10.5`)
- `test-level`: `UNIT`, `INT` (integration), `E2E` (end-to-end)
- `sequence`: Zero-padded 3-digit number (e.g., `001`, `042`, `123`)

**Examples**:
- `1.1-UNIT-001.py` - Story 1.1, Unit test #1
- `2.3-INT-015.py` - Story 2.3, Integration test #15
- `5.1-E2E-003.py` - Story 5.1, E2E test #3

### Test Function Naming

**One test function per file** (primary rule), but if multiple variants needed:

```python
# File: 1.1-UNIT-001.py
def test_1_1_unit_001():
    """Primary test function matching test ID."""
    # Main test logic

def test_1_1_unit_001_edge_case_empty_directory():
    """Optional: Edge case variant of primary test."""
    # Edge case logic
```

**Naming Pattern**: `test_{story}_{level}_{seq}[_variant_description]()`

---

## Test File Structure

### Template

Each test file follows this structure:

```python
"""
Test ID: {TEST-ID}
Story: {STORY-NUMBER} - {STORY-NAME}
Priority: P{0-3}
Test Level: {Unit|Integration|E2E}
Risk Coverage: {RISK-ID} ({Risk Title})

Description:
{Detailed description from test design document}

Acceptance Criteria: AC{N}
Test Design Reference: docs/qa/assessments/{story}-test-design-{date}.md:{line}
"""

import pytest
from pathlib import Path
# ... other imports


# Fixtures specific to this test (if needed)
@pytest.fixture
def specific_fixture():
    """Fixture used only by this test."""
    # Setup
    yield value
    # Teardown


def test_{story}_{level}_{seq}():
    """
    {TEST-ID}: {Test scenario description}

    Justification: {Why this test exists}

    Expected: {Expected outcome}
    Failure mode: {What failure looks like}
    """
    # Arrange
    # ... setup

    # Act
    # ... execute

    # Assert
    # ... verify
```

### Example: 1.1-UNIT-001.py

```python
"""
Test ID: 1.1-UNIT-001
Story: 1.1 - Initialize Project Structure and Development Environment
Priority: P0
Test Level: Unit
Risk Coverage: OPS-001 (Missing directory prevents tests)

Description:
Verify all top-level directories exist per architecture/source-tree.md specification.
This is a foundational infrastructure test - directory structure must be correct
before any development can proceed.

Acceptance Criteria: AC1
Test Design Reference: docs/qa/assessments/1.1-test-design-20251203.md:70
"""

import pytest
from pathlib import Path


def test_1_1_unit_001_all_top_level_directories_exist(project_root):
    """
    1.1-UNIT-001: Verify all top-level directories exist.

    Justification: Pure file system check; fast feedback on infrastructure setup.

    Expected: All top-level directories (data/, src/, notebooks/, docs/, tests/,
              scripts/) exist and are actual directories.

    Failure mode: FileNotFoundError or assertion failure with missing directory name.
    """
    # Arrange
    top_level_dirs = ['data', 'src', 'notebooks', 'docs', 'tests', 'scripts']

    # Act & Assert
    for dir_name in top_level_dirs:
        dir_path = project_root / dir_name

        assert dir_path.exists(), \
            f"Missing top-level directory: {dir_name}"

        assert dir_path.is_dir(), \
            f"Path exists but is not directory: {dir_name}"
```

---

## Fixture Management

### Three-Tier Fixture System

#### 1. Global Fixtures (`tests/conftest.py`)

**Scope**: All tests across all stories
**Purpose**: Project-wide fixtures that never change

```python
"""Global pytest fixtures for all stories."""

import pytest
from pathlib import Path


@pytest.fixture(scope="session")
def project_root():
    """Return project root directory (2 levels up from tests/)."""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def src_dir(project_root):
    """Return src/momo directory."""
    return project_root / 'src' / 'momo'


@pytest.fixture(scope="session")
def data_dir(project_root):
    """Return data directory."""
    return project_root / 'data'
```

#### 2. Story-Specific Fixtures (`tests/stories/{story}/conftest.py`)

**Scope**: All tests within a story
**Purpose**: Fixtures shared across test IDs in same story

```python
"""Fixtures for Story 1.1: Initialize Project Structure."""

import pytest
from pathlib import Path


@pytest.fixture(scope="module")
def required_directories():
    """List of all required directories from architecture/source-tree.md."""
    return [
        'data/cache/prices',
        'data/cache/constituents',
        'data/cache/universes',
        'data/results/experiments',
        'src/momo',
        'src/momo/data',
        'src/momo/signals',
        'src/momo/portfolio',
        'src/momo/backtest',
        'src/momo/utils',
        'notebooks/scratch',
        'tests/unit/data',
        'tests/unit/signals',
        'tests/unit/portfolio',
        'tests/unit/backtest',
        'tests/unit/utils',
        'tests/integration',
        'tests/fixtures',
        'scripts',
    ]


@pytest.fixture
def temp_data_file(project_root):
    """Create temporary file in data/ for gitignore testing."""
    test_file = project_root / 'data/cache/prices/test_gitignore.txt'
    test_file.write_text('temporary test data')
    yield test_file
    # Cleanup
    if test_file.exists():
        test_file.unlink()
```

#### 3. Test-Specific Fixtures (inline in test file)

**Scope**: Only that specific test
**Purpose**: Unique setup for one test ID

```python
# In file: 1.1-INT-003.py

@pytest.fixture
def git_test_file(project_root):
    """Fixture only for 1.1-INT-003 git workflow test."""
    # Unique setup
    pass
```

---

## Test Discovery and Execution

### Pytest Configuration

**File**: `pytest.ini`

```ini
[pytest]
# Test discovery - find tests in stories/ subdirectories
testpaths = tests/stories
python_files = *.py
python_classes = Test*
python_functions = test_*

# Output
addopts =
    --verbose
    --strict-markers
    --tb=short

# Custom markers for story-based organization
markers =
    story_1_1: Story 1.1 - Initialize Project Structure
    story_2_1: Story 2.1 - Norgate Data Bridge
    unit: Unit tests (isolated, no external dependencies)
    integration: Integration tests (external dependencies, subprocess)
    e2e: End-to-end tests (full workflows)
    p0: Priority 0 - Critical tests
    p1: Priority 1 - High priority tests
    p2: Priority 2 - Medium priority tests
    p3: Priority 3 - Low priority tests
```

### Execution Patterns

#### Run All Tests for a Story

```bash
# All Story 1.1 tests
pytest tests/stories/1.1/ -v

# All Story 2.3 tests
pytest tests/stories/2.3/ -v
```

#### Run by Test Level

```bash
# All unit tests for Story 1.1
pytest tests/stories/1.1/unit/ -v

# All integration tests for Story 1.1
pytest tests/stories/1.1/integration/ -v

# All integration tests across all stories
pytest tests/stories/*/integration/ -v
```

#### Run by Test ID

```bash
# Single test by ID
pytest tests/stories/1.1/unit/1.1-UNIT-001.py -v

# Multiple specific test IDs
pytest tests/stories/1.1/unit/1.1-UNIT-001.py \
       tests/stories/1.1/unit/1.1-UNIT-005.py \
       tests/stories/1.1/integration/1.1-INT-004.py -v
```

#### Run by Priority (using markers)

```bash
# All P0 tests
pytest -m p0 -v

# All P0 tests for Story 1.1
pytest tests/stories/1.1/ -m p0 -v

# P0 and P1 tests only
pytest -m "p0 or p1" -v
```

#### Run with Coverage (Story-Specific)

```bash
# Coverage for Story 1.1 (tests infra, no src coverage expected)
pytest tests/stories/1.1/ --cov=src/momo --cov-report=term-missing

# Coverage for Story 2.1 (tests momo.data layer)
pytest tests/stories/2.1/ --cov=src/momo/data --cov-report=term-missing
```

---

## CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/ci.yml

name: CI - Story-Based Tests

on: [push, pull_request]

jobs:
  # Fast feedback: P0 tests only
  p0-tests:
    name: P0 Critical Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      - name: Install uv
        run: pip install uv
      - name: Install dependencies
        run: uv sync
      - name: Run P0 tests
        run: pytest -m p0 --tb=short --maxfail=5

  # Story-level test execution
  story-tests:
    name: Story ${{ matrix.story }} Tests
    runs-on: ubuntu-latest
    strategy:
      matrix:
        story: ['1.1', '2.1', '2.2', '3.1']
      fail-fast: false
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      - name: Install uv
        run: pip install uv
      - name: Install dependencies
        run: uv sync
      - name: Run Story ${{ matrix.story }} tests
        run: pytest tests/stories/${{ matrix.story }}/ -v --cov=src/momo --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
          flags: story-${{ matrix.story }}

  # Full test suite (all stories)
  full-suite:
    name: Full Test Suite
    runs-on: ubuntu-latest
    needs: [p0-tests]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      - name: Install uv
        run: pip install uv
      - name: Install dependencies
        run: uv sync
      - name: Run all tests
        run: pytest tests/stories/ -v --cov=src/momo --cov-report=html --cov-report=term
      - name: Archive coverage report
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: htmlcov/
```

---

## AI Agent Workflows

### Agent Command Patterns

#### 1. Implement Test for Specific ID

**Command**: `/atomic-commit 1.1 2`

**Agent Workflow**:
1. Read `docs/qa/assessments/1.1-test-design-20251203.md`
2. Find test ID `1.1-UNIT-012` and `1.1-INT-004` (from Commit 2)
3. Create files:
   - `tests/stories/1.1/unit/1.1-UNIT-012.py`
   - `tests/stories/1.1/integration/1.1-INT-004.py`
4. Write test code exactly as specified in test design
5. Run: `pytest tests/stories/1.1/unit/1.1-UNIT-012.py -v`
6. Verify: Test fails (red phase)
7. Implement minimal code to pass
8. Verify: Test passes (green phase)
9. Commit with message: `test(1.1): implement package import tests (1.1-UNIT-012, 1.1-INT-004)`

**Zero Ambiguity**: Test ID → File path is deterministic.

#### 2. Fix Failing Test

**Human**: "Fix test 1.1-INT-003"

**Agent Workflow**:
1. Locate file: `tests/stories/1.1/integration/1.1-INT-003.py`
2. Read test code
3. Run: `pytest tests/stories/1.1/integration/1.1-INT-003.py -v`
4. Analyze failure
5. Fix implementation (not test code)
6. Verify: `pytest tests/stories/1.1/integration/1.1-INT-003.py -v` passes

**No Search Required**: Test ID = filename.

#### 3. Review Story Completion

**Human**: "Check Story 1.1 test status"

**Agent Workflow**:
1. Read `docs/qa/assessments/1.1-test-design-20251203.md` → 21 test IDs
2. Check `tests/stories/1.1/` → count .py files
3. Run: `pytest tests/stories/1.1/ -v --tb=no`
4. Report:
   ```
   Story 1.1 Test Status:
   - Test IDs defined: 21
   - Test files created: 21
   - Tests passing: 19
   - Tests failing: 2 (1.1-INT-003, 1.1-INT-007)
   - Coverage: 90.5%
   ```

**Clear Accountability**: Each test ID has exactly one file.

#### 4. Parallel Agent Execution

**Scenario**: 3 agents implement Commit 1 of Story 1.1 in parallel

- **Agent A**: Implements `1.1-UNIT-001.py`, `1.1-UNIT-002.py`
- **Agent B**: Implements `1.1-UNIT-003.py`, `1.1-UNIT-004.py`
- **Agent C**: Implements `1.1-UNIT-005.py`, `1.1-UNIT-006.py`

**Result**: Zero merge conflicts (different files), perfect parallel execution.

---

## Comparison: Traditional vs Story-Based

| Aspect | Traditional | Story-Based | Winner |
|--------|-------------|-------------|--------|
| **File Count** | ~10-15 files | ~50-100 files | Traditional (fewer files) |
| **Traceability** | Grep for test ID in docstrings | Test ID = filename | **Story-Based** |
| **Merge Conflicts** | High (multiple tests per file) | Near zero (one test per file) | **Story-Based** |
| **Agent Certainty** | "Find test in test_imports.py" | "Edit 1.1-UNIT-012.py" | **Story-Based** |
| **Test Lifecycle** | Manual cleanup when story done | `rm -rf tests/stories/1.1/` | **Story-Based** |
| **Discovery Speed** | Fast (fewer files) | Slower (more files) | Traditional |
| **Parallel Execution** | Limited by file locks | Unlimited (isolated files) | **Story-Based** |
| **Human Browsing** | Easier (grouped by module) | Harder (many files) | Traditional |
| **AI Maintenance** | Ambiguous | Deterministic | **Story-Based** |
| **CI Granularity** | Test function level | File level or story level | **Story-Based** |

### When to Use Story-Based

✅ **Use Story-Based When**:
- AI agents are primary maintainers
- Parallel development is common
- Test lifecycle tied to story lifecycle
- Traceability to test design documents is critical
- Team works in story-based sprints

❌ **Use Traditional When**:
- Human developers browse tests frequently
- Codebase is small (<1000 tests)
- Test organization by domain (data layer, signal layer) is more important than story organization
- Merge conflicts are rare (solo developer)

---

## Migration Strategy

### Phase 1: Hybrid Approach (Current Sprint)

**Story 1.1**: Use traditional structure (already planned in atomic commits)
**Story 1.2+**: Migrate to story-based

**Rationale**: Don't disrupt Story 1.1 planning already done.

### Phase 2: New Stories (Next Sprint)

**All new stories** use story-based organization:
- Story 2.1 → `tests/stories/2.1/`
- Story 2.2 → `tests/stories/2.2/`

### Phase 3: Gradual Migration (Future)

**Optional**: Migrate Story 1.1 tests:
```bash
# Move tests to story-based structure
mkdir -p tests/stories/1.1/unit
mkdir -p tests/stories/1.1/integration

# Extract each test from test_structure.py to individual files
# test_all_top_level_directories_exist → 1.1-UNIT-001.py
# test_data_subdirectory_structure → 1.1-UNIT-002.py
# ...
```

---

## Metadata and Documentation

### Test Registry

**File**: `tests/stories/TEST_REGISTRY.md`

```markdown
# Test Registry

Automatically generated mapping of Test IDs to files.

| Story | Test ID | File | Priority | Status |
|-------|---------|------|----------|--------|
| 1.1 | 1.1-UNIT-001 | tests/stories/1.1/unit/1.1-UNIT-001.py | P0 | ✅ Pass |
| 1.1 | 1.1-UNIT-002 | tests/stories/1.1/unit/1.1-UNIT-002.py | P0 | ✅ Pass |
| 1.1 | 1.1-INT-003 | tests/stories/1.1/integration/1.1-INT-003.py | P0 | ❌ Fail |
| ... | ... | ... | ... | ... |

Last updated: 2025-12-03 18:45:00
```

**Generation**: CI/CD auto-generates after each test run.

### Story-Level README

**File**: `tests/stories/1.1/README.md`

```markdown
# Story 1.1: Initialize Project Structure - Test Suite

**Story**: 1.1 - Initialize Project Structure and Development Environment
**Test Count**: 21 tests (13 unit, 8 integration)
**Priority**: 17 P0, 1 P1, 2 P2

## Test Coverage

- **AC1** (Directory Structure): 1.1-UNIT-001 through 1.1-UNIT-006
- **AC2** (Python Environment): 1.1-UNIT-007, 1.1-INT-001, 1.1-INT-002
- **AC3** (.gitignore): 1.1-UNIT-008, 1.1-UNIT-009, 1.1-INT-003
- **AC7** (Package Imports): 1.1-UNIT-012, 1.1-UNIT-013, 1.1-INT-004

## Running Tests

```bash
# All Story 1.1 tests
pytest tests/stories/1.1/ -v

# Only P0 tests
pytest tests/stories/1.1/ -m p0 -v

# Single test
pytest tests/stories/1.1/unit/1.1-UNIT-001.py -v
```

## Test Design Reference

See: `docs/qa/assessments/1.1-test-design-20251203.md`
```

---

## Tool Integration

### pytest Plugins

**Custom plugin**: `tests/pytest_story_markers.py`

```python
"""Pytest plugin to auto-add story markers based on directory structure."""

import pytest


def pytest_collection_modifyitems(config, items):
    """Auto-add markers based on test file path."""
    for item in items:
        # Extract story from path: tests/stories/1.1/unit/1.1-UNIT-001.py
        parts = item.nodeid.split('/')

        if 'stories' in parts:
            story_idx = parts.index('stories') + 1
            if story_idx < len(parts):
                story_id = parts[story_idx]

                # Add story marker
                marker = pytest.mark.__getattr__(f'story_{story_id.replace(".", "_")}')
                item.add_marker(marker)

                # Add level marker (unit/integration/e2e)
                if story_idx + 1 < len(parts):
                    level = parts[story_idx + 1]
                    item.add_marker(pytest.mark.__getattr__(level))

                # Extract priority from test ID in filename
                filename = parts[-1]
                # Parse priority from test docstring (requires reading file)
                # For now, default to p0
                item.add_marker(pytest.mark.p0)
```

**Enable in pytest.ini**:
```ini
[pytest]
plugins = tests.pytest_story_markers
```

### VS Code Integration

**File**: `.vscode/settings.json`

```json
{
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": [
    "tests/stories"
  ],
  "python.testing.autoTestDiscoverOnSaveEnabled": true,

  "files.associations": {
    "**/*-UNIT-*.py": "python-test",
    "**/*-INT-*.py": "python-test",
    "**/*-E2E-*.py": "python-test"
  }
}
```

---

## Advantages Summary

### For AI Agents

1. **Deterministic File Mapping**: Test ID → File path is a pure function
2. **Zero Coordination Overhead**: Parallel agents never collide
3. **Clear Ownership**: Each test ID has exactly one owner (one file)
4. **Lifecycle Alignment**: Story done → Delete story test directory
5. **Precise Error Reporting**: "Test 1.1-INT-003 failed" → exact file
6. **Traceability**: Test design doc line → Test file (1:1 mapping)

### For Human Developers

1. **Story Focus**: See all tests for a story in one directory
2. **Test Lifecycle**: Deprecate story → Delete test directory
3. **Code Review**: Each test file is atomic, easy to review
4. **Debugging**: Run single test by ID with zero ambiguity

### For CI/CD

1. **Granular Execution**: Run story-level, priority-level, or test-ID-level
2. **Parallel Execution**: Matrix strategy by story (no conflicts)
3. **Clear Reporting**: Test failures map to exact files
4. **Coverage Tracking**: Per-story coverage reports

---

## Disadvantages and Mitigations

### Disadvantage 1: File Count Explosion

**Problem**: 21 tests = 21 files for Story 1.1 alone. Large projects could have 1000+ test files.

**Mitigations**:
- pytest handles large file counts well (discovery is still fast)
- Modern IDEs handle file trees efficiently
- Use `fd` or `ripgrep` for fast file searching: `fd 1.1-INT tests/`
- Story-level organization prevents "flat" directory with 1000 files

### Disadvantage 2: Shared Test Logic

**Problem**: Multiple tests need same helper function.

**Mitigations**:
- Use story-level `conftest.py` for story-specific helpers
- Use `tests/utils/` for cross-story helpers
- Keep test files focused; duplication better than coupling

### Disadvantage 3: Human Browsing Difficulty

**Problem**: Humans want to see "all data layer tests" not "all Story 2.1 tests."

**Mitigations**:
- Maintain `tests/stories/TEST_REGISTRY.md` with tags/categories
- Use pytest markers: `pytest -m data_layer -v`
- Generate cross-reference: `tests/by_layer/data/` → symlinks to story tests
- Hybrid approach: Keep traditional structure for exploration, story structure for execution

### Disadvantage 4: Test Discovery Performance

**Problem**: pytest collecting 1000 files slower than collecting 50 files.

**Mitigations**:
- Use `pytest --co` caching
- Run tests by story in CI (only collect that story's tests)
- pytest-xdist parallel collection
- **Measured impact**: Negligible for <500 files (< 1 second difference)

---

## Decision: Recommendation

### For `momo` Project

**Recommended**: **Adopt Story-Based Test Organization**

**Rationale**:
1. Project explicitly designed for AI agent development (slash commands, atomic commits)
2. Story-based development workflow (Epic → Story → Atomic Commits)
3. Multiple agents will work in parallel
4. Test design documents already map to test IDs
5. Traceability is critical for agent workflows

**Implementation**:
- Start with Story 1.1 using story-based organization
- Validate approach through first story
- Refine patterns based on learnings
- Scale to all future stories

### Alternative: Hybrid Approach

**If uncertain**, implement hybrid:
- **Critical infrastructure tests** (Story 1.1): Traditional structure (easier human review)
- **Feature tests** (Story 2.1+): Story-based structure (agent-optimized)

Monitor which approach works better, migrate if needed.

---

## Action Items

### Immediate (Story 1.1)

- [ ] Create `tests/stories/1.1/` directory structure
- [ ] Update `pytest.ini` with `testpaths = tests/stories`
- [ ] Create global `tests/conftest.py` with `project_root` fixture
- [ ] Create story-specific `tests/stories/1.1/conftest.py`
- [ ] Implement first test: `tests/stories/1.1/unit/1.1-UNIT-001.py`
- [ ] Validate test discovery: `pytest tests/stories/1.1/ --collect-only`

### Short-term (Sprint 1)

- [ ] Document pytest execution patterns in `tests/stories/README.md`
- [ ] Create pytest plugin for auto-markers
- [ ] Generate initial `TEST_REGISTRY.md`
- [ ] Set up CI/CD with story-level test execution

### Long-term (Future Sprints)

- [ ] Build test registry generator (auto-update on CI)
- [ ] Create test coverage dashboard by story
- [ ] Implement cross-reference views (by layer, by component)
- [ ] Measure test discovery performance at scale

---

## Conclusion

**Story-based test organization is a paradigm shift optimized for AI-agent-maintained codebases.** The 1:1 mapping between test IDs and files eliminates ambiguity, enables perfect parallel execution, and aligns test lifecycle with story lifecycle.

**Trade-off**: More files, less human browsing convenience.
**Payoff**: Deterministic agent workflows, zero merge conflicts, perfect traceability.

For a project explicitly designed around AI agents (`/atomic-commit`, `/develop-story` commands), **this approach is the right choice**.

---

**Document**: `docs/test-environment-design.md`
**Created**: 2025-12-03
**Status**: Proposed (awaiting Story 1.1 validation)
**Next Review**: After Story 1.1 completion
