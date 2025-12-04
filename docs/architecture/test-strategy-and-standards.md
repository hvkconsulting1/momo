# Test Strategy and Standards

## Testing Philosophy

| Item | Value |
|------|-------|
| **Organization Model** | Story-based (optimized for AI agent workflows) |
| **Approach** | TDD for core calculations; test-after for utilities |
| **Coverage Goals** | 90%+ for signal/portfolio/backtest; 70%+ overall |
| **Test Pyramid** | 70% unit, 25% integration, 5% e2e |
| **Traceability** | 1:1 mapping between test IDs and test files |

**Key Principle**: Test organization mirrors product development organization (stories → test IDs → test files).

---

## Story-Based Test Organization

### Philosophy

Traditional test organization by layer (`tests/unit/data/`, `tests/unit/signals/`) optimizes for human browsing but creates friction for AI agent workflows:

- **Merge conflicts** when multiple agents edit the same test file
- **Ambiguity** finding which file contains test ID `1.1-UNIT-012`
- **Lifecycle mismatch** when story is complete but tests remain scattered

**Story-based organization** creates a deterministic mapping:
- Test ID `1.1-UNIT-001` → File `tests/stories/1.1/unit/test_1_1_unit_001.py`
- Story lifecycle = test lifecycle (ship story → archive test directory)
- Zero merge conflicts (one test per file)
- Perfect AI agent traceability

### When to Use Story-Based

✅ **Use Story-Based When:**
- AI agents are primary maintainers
- Parallel development is common
- Test lifecycle tied to story lifecycle
- Traceability to test design documents is critical
- Team works in story-based sprints

**Trade-off**: More files, less human browsing convenience.
**Payoff**: Deterministic agent workflows, zero merge conflicts, perfect traceability.

---

## Directory Structure

```
tests/
├── conftest.py                          # Global fixtures (project_root, etc.)
├── pytest.ini                           # Pytest configuration
│
├── stories/                             # Story-based test organization
│   ├── 1.1/                            # Story 1.1: Initialize Project Structure
│   │   ├── conftest.py                 # Story-specific fixtures
│   │   ├── README.md                   # Story test suite documentation
│   │   ├── unit/
│   │   │   ├── test_1_1_unit_001.py        # Verify top-level directories
│   │   │   ├── test_1_1_unit_002.py        # Verify data/ subdirectories
│   │   │   └── ...
│   │   └── integration/
│   │       ├── test_1_1_int_001.py         # uv sync resolves dependencies
│   │       └── ...
│   │
│   ├── 2.1/                            # Story 2.1: Norgate Data Bridge
│   │   ├── conftest.py
│   │   ├── README.md
│   │   ├── unit/
│   │   └── integration/
│   │
│   └── TEST_REGISTRY.md                # Auto-generated test ID → file mapping
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

---

## File Naming Conventions

### Test File Naming

**Pattern**: `test_{story_id}_{level}_{seq}.py`

- `story_id`: Story number with underscores (e.g., `1_1`, `2_3`, `10_5`)
- `level`: Lowercase test level (`unit`, `int`, `e2e`)
- `seq`: Zero-padded 3-digit number (e.g., `001`, `042`, `123`)

**Examples**:
- `test_1_1_unit_001.py` - Story 1.1, Unit test #1
- `test_2_3_int_015.py` - Story 2.3, Integration test #15
- `test_5_1_e2e_003.py` - Story 5.1, E2E test #3

### Test Function Naming

**One test function per file** (primary rule), but if multiple variants needed:

```python
# File: test_1_1_unit_001.py
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

### Example: test_1_1_unit_001.py

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
        'src/momo/data',
        'src/momo/signals',
        'tests/stories/1.1/unit',
        # ... etc
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
# In file: test_1_1_int_003.py

@pytest.fixture
def git_test_file(project_root):
    """Fixture only for 1.1-INT-003 git workflow test."""
    # Unique setup
    pass
```

---

## Test Types

### Unit Tests

- **Location**: `tests/stories/{story}/unit/`
- **Framework**: pytest 8.x
- **Coverage Goal**: 90% for core layers (signals, portfolio, backtest)
- **Characteristics**:
  - Isolated, no external dependencies
  - Fast execution (< 100ms per test)
  - Pure function testing
  - Mock all I/O operations

### Integration Tests

- **Location**: `tests/stories/{story}/integration/`
- **Coverage Goal**: Critical paths and layer boundaries
- **Characteristics**:
  - External dependencies allowed (subprocess, file I/O)
  - Mock Norgate via bridge substitution
  - Test layer interactions
  - Slower execution (< 5s per test)

### E2E Tests

- **Location**: `tests/stories/{story}/e2e/`
- **Framework**: Notebook execution via nbconvert
- **Characteristics**:
  - Full workflow validation
  - Limited scope (no web UI in this project)
  - Slowest execution (minutes)

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
pytest tests/stories/1.1/unit/test_1_1_unit_001.py -v

# Multiple specific test IDs
pytest tests/stories/1.1/unit/test_1_1_unit_001.py \
       tests/stories/1.1/unit/test_1_1_unit_005.py \
       tests/stories/1.1/integration/test_1_1_int_004.py -v
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

## AI Agent Workflows

### Agent Command Patterns

#### 1. Implement Test for Specific ID

**Command**: `/atomic-commit 1.1 2`

**Agent Workflow**:
1. Read `docs/qa/assessments/1.1-test-design-20251203.md`
2. Find test IDs for Commit 2
3. Create files: `tests/stories/1.1/unit/test_1_1_unit_012.py`, etc.
4. Write test code exactly as specified in test design
5. Run: `pytest tests/stories/1.1/unit/test_1_1_unit_012.py -v`
6. Verify: Test fails (red phase)
7. Implement minimal code to pass
8. Verify: Test passes (green phase)
9. Commit with message

**Zero Ambiguity**: Test ID → File path is deterministic.

#### 2. Fix Failing Test

**Human**: "Fix test 1.1-INT-003"

**Agent Workflow**:
1. Locate file: `tests/stories/1.1/integration/test_1_1_int_003.py`
2. Read test code
3. Run: `pytest tests/stories/1.1/integration/test_1_1_int_003.py -v`
4. Analyze failure
5. Fix implementation (not test code)
6. Verify: Test passes

**No Search Required**: Test ID = filename.

#### 3. Parallel Agent Execution

**Scenario**: 3 agents implement Commit 1 of Story 1.1 in parallel

- **Agent A**: Implements `test_1_1_unit_001.py`, `test_1_1_unit_002.py`
- **Agent B**: Implements `test_1_1_unit_003.py`, `test_1_1_unit_004.py`
- **Agent C**: Implements `test_1_1_unit_005.py`, `test_1_1_unit_006.py`

**Result**: Zero merge conflicts (different files), perfect parallel execution.

---

## Test Data Management

### Shared Fixtures

- **Location**: `tests/fixtures/`
- **Format**: Parquet for DataFrames, JSON for configs, CSV for small samples
- **Naming**: Prefix with `sample_` (e.g., `sample_prices.parquet`)
- **Reproducibility**: Use `np.random.seed(42)` for generated data

### Fixture Organization

```
tests/fixtures/
├── sample_prices.parquet          # Small price dataset (10 tickers, 1 year)
├── sample_constituents.parquet    # Sample index constituents
├── sample_universes.parquet       # Point-in-time universe snapshots
├── mock_norgate_responses.json    # Mocked Norgate API responses
└── expected_outputs/              # Expected outputs for integration tests
    ├── momentum_signals.parquet
    └── backtest_metrics.json
```

### Pytest Fixtures Best Practices

1. **Global fixtures** in `tests/conftest.py` - project structure paths
2. **Story fixtures** in `tests/stories/{story}/conftest.py` - story-specific data
3. **Test fixtures** inline - unique setup for one test
4. Use `scope="session"` for expensive setup (load data once)
5. Use `scope="module"` for story-level data
6. Use default scope (`function`) for test-specific setup

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
```

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

## Related Documentation

- **Test Environment Design**: `docs/test-environment-design.md` (comprehensive guide)
- **ADR-010**: Story-Based Test Organization for AI Agent Workflows
- **Source Tree**: `docs/architecture/source-tree.md` (directory structure)
- **Coding Standards**: `docs/architecture/coding-standards.md` (test conventions)

---
