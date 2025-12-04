# Infrastructure and Deployment

## Infrastructure as Code

| Item | Value |
|------|-------|
| **Tool** | N/A (no cloud infrastructure) |
| **Approach** | Local-only for MVP |

## Deployment Strategy

| Item | Value |
|------|-------|
| **Strategy** | Local installation via `uv` |
| **CI/CD Platform** | GitHub Actions |
| **Pipeline Configuration** | `.github/workflows/ci.yml` |

## Environments

| Environment | Purpose |
|-------------|---------|
| **Development** | Local research (WSL2 + Windows for NDU) |
| **CI** | Automated testing on push/PR |

## CI Pipeline

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv python install 3.13
      - run: uv sync --all-extras
      - run: uv run ruff check src tests
      - run: uv run mypy src
      - run: uv run pytest -n auto --ignore=tests/integration -v
```

---
