# Security

## Security Context

| Aspect | Status |
|--------|--------|
| **Attack Surface** | Minimal - local tool |
| **User Authentication** | N/A |
| **Data Sensitivity** | Low |

## Key Security Measures

**Input Validation:**
- Validate Norgate data before caching
- Whitelist expected columns and dtypes

**Subprocess Security:**
- Never use `shell=True`
- Validate symbol format before bridge calls
- Never pass user input to subprocess

**Dependency Security:**
- Pin versions via `uv.lock`
- GitHub Dependabot for updates
- Review before adding new packages

## Security Checklist for AI Agents

- [ ] No `shell=True` in subprocess
- [ ] No `eval()` or `exec()` with external data
- [ ] No pickle for untrusted data
- [ ] Validated inputs at boundaries
- [ ] No sensitive data in logs

---
