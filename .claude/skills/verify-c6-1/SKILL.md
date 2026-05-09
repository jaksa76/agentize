---
name: verify-c6-1
description: Verify readiness criterion C6.1 (Static Analysis) in the current project. Reports fulfillment level 0–3.
allowed-tools: Bash Read
---

# Verify C6.1 — Static Analysis

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | No quality tooling |
| 1 | Linting and/or formatting configured |
| 2 | + Type checking enforced |
| 3 | + Security scanning (SAST) |

## Evidence

### Linting / formatting config files
!`ls .eslintrc .eslintrc.js .eslintrc.cjs .eslintrc.json .eslintrc.yml .eslintrc.yaml eslint.config.js eslint.config.mjs .prettierrc .prettierrc.js prettier.config.js 2>/dev/null || echo "(no ESLint/Prettier config)"`
!`ls .pylintrc .flake8 ruff.toml .ruff.toml pyproject.toml 2>/dev/null | head -5 && grep -l "\[tool.ruff\]\|\[tool.flake8\]\|\[tool.pylint\]" pyproject.toml 2>/dev/null || echo "(no Python linting config)"`
!`ls .rubocop.yml checkstyle.xml .golangci.yml .golangci.yaml 2>/dev/null || echo "(no Ruby/Java/Go linting config)"`

### Linting in CI
!`grep -r -i "eslint\|pylint\|flake8\|ruff\|rubocop\|golangci\|lint" .github/workflows/ 2>/dev/null | head -10 || echo "(no linting steps in CI)"`

### Type checking config
!`ls tsconfig.json tsconfig.*.json 2>/dev/null || echo "(no tsconfig)"`
!`cat tsconfig.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); opts=d.get('compilerOptions',{}); print('strict:', opts.get('strict'), '| noImplicitAny:', opts.get('noImplicitAny'), '| strictNullChecks:', opts.get('strictNullChecks'))" 2>/dev/null || true`
!`ls mypy.ini .mypy.ini 2>/dev/null || grep -l "\[tool.mypy\]" pyproject.toml setup.cfg 2>/dev/null || echo "(no mypy config)"`
!`grep -r -i "mypy\|tsc --noEmit\|pyright\|type-check" .github/workflows/ 2>/dev/null | head -5 || echo "(no type checking in CI)"`

### Security scanning (SAST)
!`ls .snyk sonar-project.properties .semgrep.yml .semgrep/ .github/workflows/codeql*.yml 2>/dev/null || echo "(no SAST config files found)"`
!`grep -r -i "codeql\|snyk\|semgrep\|sonar\|trivy\|bandit\|gosec\|brakeman\|safety" .github/workflows/ 2>/dev/null | head -10 || echo "(no SAST steps in CI)"`
!`cat package.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); deps={**d.get('dependencies',{}),**d.get('devDependencies',{})}; sec=[k for k in deps if any(x in k for x in ['snyk','sonar','semgrep'])]; print('Security deps:', sec if sec else 'none')" 2>/dev/null || true`

## Instructions

Analyse the evidence above and determine the fulfillment level for C6.1.

Scoring guide:
- **Level 0**: No quality tooling of any kind — no linter config, no formatter config, no type checking, no security scanning.
- **Level 1**: Linting and/or formatting is configured — an ESLint, Prettier, Ruff, pylint, or equivalent config file exists, or a linting step runs in CI. At least one of: linter config file present, linting step in CI.
- **Level 2**: Type checking is additionally enforced — a tsconfig with strict mode or noImplicitAny, a mypy config, Pyright, or equivalent is configured. Type checking runs in CI is a strong indicator. Level 1 requirements must also be met.
- **Level 3**: Security scanning (SAST) is additionally configured — CodeQL, Snyk, Semgrep, SonarQube, Bandit, or equivalent runs in CI or is configured as a pre-merge step. Levels 1 and 2 must also be met.

Report in exactly this format:

**C6.1 — Static Analysis**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [one or two sentences citing the specific evidence]
