---
name: assess-readiness
description: Assess the Agent Readiness level of the current project across all 11 criteria (C1.1–C8.2) and produce a structured report with the achieved level, per-criterion scores, gaps, and recommendations.
allowed-tools: Bash Read
---

# Agent Readiness Assessment

This skill collects evidence for all 11 readiness criteria and instructs you to
score each one, determine the overall readiness level, and produce a full report.

---

## Evidence Collection

### C1.1 — Codebase Accessibility
!`ls CLAUDE.md AGENTS.md .claude/CLAUDE.md 2>/dev/null || echo "(no agent context file)"`
!`wc -l CLAUDE.md 2>/dev/null || wc -l AGENTS.md 2>/dev/null || echo "(empty)"`
!`head -40 CLAUDE.md 2>/dev/null || head -40 AGENTS.md 2>/dev/null || head -20 README.md 2>/dev/null || echo "(no README or agent context file)"`
!`cat .gitmodules 2>/dev/null || echo "(no .gitmodules)"`

### C2.1 — Setup Automation
!`ls .devcontainer/ devcontainer.json flake.nix shell.nix 2>/dev/null || echo "(no containerised env)"`
!`ls setup.sh install.sh bootstrap.sh 2>/dev/null || grep -i "^install\b\|^setup\b\|^dev\b" Makefile 2>/dev/null | head -5 || echo "(no setup scripts or Makefile targets)"`
!`ls package.json requirements.txt Pipfile pyproject.toml pom.xml build.gradle Cargo.toml go.mod 2>/dev/null || echo "(no dependency manifests)"`
!`grep -A8 -i "getting started\|quick start\|setup\|install" README.md 2>/dev/null | head -20 || echo "(no setup section in README)"`

### C3.1 — Architecture Depth
!`find . -maxdepth 4 \( -iname "ARCHITECTURE.md" -o -iname "architecture.md" -o -iname "DESIGN.md" \) 2>/dev/null | grep -v node_modules | head -10 || echo "(no architecture docs at root or docs/)"`
!`find docs/ -name "*.md" 2>/dev/null | head -15 || echo "(no docs/ directory)"`
!`find . -maxdepth 5 \( -name "*.puml" -o -name "*.c4" -o -name "*.drawio" -o -name "*.mmd" \) 2>/dev/null | grep -v node_modules | head -10 || echo "(no diagram files)"`
!`grep -n -i "architecture\|container diagram\|component\|service\|context diagram\|critical flow\|sequence" README.md 2>/dev/null | head -10 || echo "(no architecture keywords in README)"`

### C4.1 — Requirements Access
!`ls VISION.md REQUIREMENTS.md requirements.md GOALS.md 2>/dev/null || echo "(no vision/requirements files at root)"`
!`ls -d stories/ features/ user-stories/ backlog/ 2>/dev/null || echo "(no stories/backlog directory)"`
!`cat .claude/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); mcp=d.get('mcpServers',{}); print('MCP servers:', list(mcp.keys()) if mcp else 'none')" 2>/dev/null || echo "(no MCP servers configured)"`
!`head -10 VISION.md 2>/dev/null || echo "(no VISION.md)"`

### C5.1 — Runnability
!`ls package.json pom.xml build.gradle setup.py pyproject.toml Cargo.toml go.mod 2>/dev/null || echo "(no build system found)"`
!`cat package.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print('npm scripts:', list(d.get('scripts',{}).keys()))" 2>/dev/null || true`
!`ls Procfile docker-compose.yml docker-compose.yaml 2>/dev/null || echo "(no Procfile or docker-compose)"`
!`grep -i "^build\b\|^run\b\|^start\b\|^serve\b" Makefile 2>/dev/null | head -5 || echo "(no run/build Makefile targets)"`

### C5.2 — Unit Test Coverage
!`find . -maxdepth 4 -type d \( -name "test" -o -name "tests" -o -name "__tests__" -o -name "spec" \) 2>/dev/null | grep -v node_modules | head -10 || echo "(no test directories)"`
!`find . -maxdepth 6 \( -name "*.test.ts" -o -name "*.test.js" -o -name "*_test.py" -o -name "test_*.py" -o -name "*Test.java" -o -name "*_test.go" \) 2>/dev/null | grep -v node_modules | wc -l`
!`ls coverage/ htmlcov/ .coverage 2>/dev/null && echo "(coverage artifacts exist)" || echo "(no coverage artifacts)"`
!`cat jest.config.js jest.config.ts 2>/dev/null | grep -i "coverage\|threshold" | head -10 || grep -A5 "\[tool.coverage" pyproject.toml 2>/dev/null | head -10 || echo "(no coverage threshold config)"`

### C5.3 — Integration and E2E Coverage
!`ls cypress.config.js cypress.config.ts playwright.config.ts playwright.config.js 2>/dev/null || echo "(no Cypress/Playwright config)"`
!`ls -d cypress/ e2e/ tests/e2e/ features/ 2>/dev/null || echo "(no E2E directories)"`
!`find . -maxdepth 5 -type d -name "integration" 2>/dev/null | grep -v node_modules | head -5 || echo "(no integration test directory)"`
!`cat package.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); deps={**d.get('dependencies',{}),**d.get('devDependencies',{})}; e2e=[k for k in deps if any(x in k for x in ['cypress','playwright','puppeteer','percy','chromatic'])]; print('E2E/visual deps:', e2e)" 2>/dev/null || true`

### C6.1 — Static Analysis
!`ls .eslintrc .eslintrc.js .eslintrc.json eslint.config.js .pylintrc .flake8 ruff.toml .rubocop.yml .golangci.yml 2>/dev/null || echo "(no linting config)"`
!`ls tsconfig.json mypy.ini .mypy.ini 2>/dev/null || echo "(no type checking config)"`
!`cat tsconfig.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); o=d.get('compilerOptions',{}); print('strict:', o.get('strict'), 'noImplicitAny:', o.get('noImplicitAny'))" 2>/dev/null || true`
!`ls .snyk sonar-project.properties .semgrep.yml 2>/dev/null || grep -r "codeql\|snyk\|semgrep\|trivy\|bandit" .github/workflows/ 2>/dev/null | head -5 || echo "(no SAST config or CI steps)"`

### C7.1 — Test Isolation
!`find . -maxdepth 5 -type d \( -name "mocks" -o -name "__mocks__" -o -name "fixtures" -o -name "stubs" \) 2>/dev/null | grep -v node_modules | head -10 || echo "(no mock/fixture directories)"`
!`find . -maxdepth 5 \( -iname "seed*" \) \( -name "*.js" -o -name "*.ts" -o -name "*.py" -o -name "*.sql" \) 2>/dev/null | grep -v node_modules | head -10 || echo "(no seed scripts)"`
!`ls docker-compose.test.yml docker-compose.testing.yml 2>/dev/null || grep -r "testcontainer\|localstack" . 2>/dev/null --include="*.json" --include="*.ts" --include="*.js" -l | grep -v node_modules | head -5 || echo "(no test-environment isolation tools)"`

### C8.1 — CI/CD Automation
!`ls .github/workflows/ 2>/dev/null && ls .github/workflows/ || ls .gitlab-ci.yml Jenkinsfile .circleci/ 2>/dev/null || echo "(no CI config)"`
!`find .github/workflows/ -name "*.yml" -o -name "*.yaml" 2>/dev/null | xargs grep -l "deploy\|release\|publish" 2>/dev/null | head -5 || echo "(no deployment steps in CI)"`
!`grep -r "workflow_dispatch" .github/workflows/ 2>/dev/null | head -5 || echo "(no workflow_dispatch triggers)"`
!`cat .claude/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); mcp=d.get('mcpServers',{}); ci=[k for k in mcp if any(x in k.lower() for x in ['github','gitlab','ci','pipeline'])]; print('CI MCP servers:', ci if ci else 'none')" 2>/dev/null || echo "(no CI MCP servers)"`

### C8.2 — Observability
!`cat package.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); deps={**d.get('dependencies',{}),**d.get('devDependencies',{})}; obs=[k for k in deps if any(x in k for x in ['datadog','opentelemetry','@opentelemetry','sentry','newrelic','dd-trace','pino','winston'])]; print('Observability deps:', obs)" 2>/dev/null || true`
!`ls datadog.yaml prometheus.yml grafana/ 2>/dev/null || echo "(no monitoring config files)"`
!`cat .claude/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); mcp=d.get('mcpServers',{}); obs=[k for k in mcp if any(x in k.lower() for x in ['grafana','datadog','sentry','cloudwatch','monitor','metric'])]; print('Observability MCP servers:', obs if obs else 'none')" 2>/dev/null || echo "(no observability MCP servers)"`
!`find . -maxdepth 4 \( -iname "alert*.yml" -o -iname "*.rules.yml" -o -iname "alertmanager*" \) 2>/dev/null | head -5 || echo "(no alerting config)"`

---

## Scoring Instructions

Using the evidence collected above, assign a fulfillment level to each criterion.

### Criterion scoring guides

**C1.1 Codebase Accessibility (0–2)**
- 0: No single entry point; no README
- 1: Single root with a basic README
- 2: CLAUDE.md or AGENTS.md with conventions, commands, and navigation guidance

**C2.1 Setup Automation (0–3)**
- 0: No setup instructions
- 1: Written step-by-step instructions in README
- 2: Single script (`setup.sh`, `npm install`, etc.) installs everything
- 3: Containerised/declarative environment (.devcontainer, Nix, etc.)

**C3.1 Architecture Depth (0–3)**
- 0: No in-repo architecture docs
- 1: System context documented (purpose, users, external systems)
- 2: Container/service level documented
- 3: Component level + critical flows documented

**C4.1 Requirements Access (0–3)**
- 0: No documented requirements
- 1: Product vision or goals documented (VISION.md, README overview)
- 2: User stories or acceptance criteria accessible (stories/, backlog, linked issues)
- 3: Programmatic access via MCP server or API

**C5.1 Runnability (0–2)**
- 0: Project does not build
- 1: Project builds without errors
- 2: App can be run locally or in an ephemeral environment

**C5.2 Unit Test Coverage (0–3)**
- 0: No unit tests
- 1: Some tests present (<50% coverage)
- 2: ≥50% coverage
- 3: ≥80% coverage

**C5.3 Integration and E2E Coverage (0–3)**
- 0: No integration or E2E tests
- 1: Integration tests cover key boundaries
- 2: E2E tests cover critical flows
- 3: E2E + UI visual regression (N/A for projects without a UI — max Level 2)

**C6.1 Static Analysis (0–3)**
- 0: No quality tooling
- 1: Linting and/or formatting configured
- 2: + Type checking enforced
- 3: + Security scanning (SAST)

**C7.1 Test Isolation (0–2, or N/A)**
- N/A: No database or external dependencies
- 0: No isolation from external systems
- 1: In-code mocks/stubs and basic fixtures
- 2: Reproducible DB state via seed scripts + sandbox environments

**C8.1 CI/CD Automation (0–3)**
- 0: No CI pipeline
- 1: Agents can read pipeline status (CI MCP server or API access)
- 2: Agents can trigger pipeline runs (workflow_dispatch or equivalent)
- 3: Full pipeline control including deployment

**C8.2 Observability (0–3)**
- 0: No access to logs or metrics
- 1: Read-only access to logs/metrics
- 2: Queryable monitoring and logs (structured query API or observability MCP server)
- 3: Automated anomaly detection and alerting

---

## Level–Criteria Mapping

After scoring all criteria, determine the highest readiness level where **all** thresholds are met:

| Criterion | Level 1 | Level 2 | Level 3 |
|-----------|---------|---------|---------|
| C1.1 | ≥ 1 | ≥ 2 | ≥ 2 |
| C2.1 | ≥ 1 | ≥ 2 | ≥ 3 |
| C3.1 | — | ≥ 1 | ≥ 3 |
| C4.1 | — | ≥ 1 | ≥ 3 |
| C5.1 | ≥ 1 | ≥ 2 | ≥ 2 |
| C5.2 | ≥ 1 | ≥ 2 | ≥ 3 |
| C5.3 | — | ≥ 1 | ≥ 2 |
| C6.1 | — | ≥ 1 | ≥ 2 |
| C7.1 | — | — | ≥ 2 (skip if N/A) |
| C8.1 | — | ≥ 1 | ≥ 3 |
| C8.2 | — | — | ≥ 2 |

Check Level 1 first. If all Level 1 thresholds are met, check Level 2. If all Level 2 thresholds are met, check Level 3. The achieved level is the highest where all thresholds pass.

---

## Report Format

Produce a report in exactly this structure:

---

# Agent Readiness Assessment Report

**Project**: [name from README or directory name]
**Date**: [today's date]

## Result: Level [0/1/2/3] — [Level Name]

Level names: 0 = Uninstrumented, 1 = Foundation, 2 = Guided Autonomy, 3 = Supervised Autonomy

## Criterion Scores

| Criterion | Name | Score | Max |
|-----------|------|-------|-----|
| C1.1 | Codebase Accessibility | [score] | 2 |
| C2.1 | Setup Automation | [score] | 3 |
| C3.1 | Architecture Depth | [score] | 3 |
| C4.1 | Requirements Access | [score] | 3 |
| C5.1 | Runnability | [score] | 2 |
| C5.2 | Unit Test Coverage | [score] | 3 |
| C5.3 | Integration and E2E Coverage | [score] | 3 |
| C6.1 | Static Analysis | [score] | 3 |
| C7.1 | Test Isolation | [score or N/A] | 2 |
| C8.1 | CI/CD Automation | [score] | 3 |
| C8.2 | Observability | [score] | 3 |

## Gaps Blocking the Next Level

[If the project is at Level 3, write "Maximum level reached."]

[Otherwise, list each criterion that is below the threshold for Level N+1:]

To reach Level [N+1] ([Name]), improve:
- **C_._ [Name]**: currently [score], need [required] — [one sentence on what to improve]

## Recommendations

[3–5 prioritised, actionable recommendations based on the gaps. Order by impact: criteria that block a level increase first, then criteria where incremental improvement is easiest.]

---
