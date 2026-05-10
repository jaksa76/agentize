---
name: improve-readiness
description: Assess the current readiness level of the project and implement all improvements needed to raise it to the next level. Runs the relevant improve-c* logic for each blocking criterion inline.
allowed-tools: Bash Read Write Edit
---

# Improve Readiness Level

This skill assesses the current readiness level of the project, identifies which criteria block the next level, and then implements the improvements for each blocking criterion directly.

---

## Evidence Collection

### C1.1 — Codebase Accessibility
!`ls CLAUDE.md AGENTS.md .claude/CLAUDE.md 2>/dev/null || echo "(no agent context file)"`
!`wc -l CLAUDE.md 2>/dev/null || wc -l AGENTS.md 2>/dev/null || echo "0 lines"`
!`head -5 README.md 2>/dev/null || echo "(no README.md)"`

### C2.1 — Setup Automation
!`ls .devcontainer/ devcontainer.json flake.nix shell.nix 2>/dev/null || echo "(no containerised env)"`
!`ls setup.sh install.sh bootstrap.sh 2>/dev/null || grep -i "^install\b\|^setup\b\|^dev\b" Makefile 2>/dev/null | head -3 || echo "(no setup scripts or Makefile targets)"`
!`ls package.json requirements.txt Pipfile pyproject.toml pom.xml build.gradle Cargo.toml go.mod 2>/dev/null || echo "(no dependency manifests)"`
!`grep -A5 -i "getting started\|quick start\|setup\|install" README.md 2>/dev/null | head -10 || echo "(no setup section in README)"`

### C3.1 — Architecture Depth
!`find . -maxdepth 4 \( -iname "ARCHITECTURE.md" -o -iname "architecture.md" -o -iname "DESIGN.md" \) 2>/dev/null | grep -v node_modules | head -5 || echo "(no architecture docs)"`
!`find docs/ -name "*.md" 2>/dev/null | head -10 || echo "(no docs/ directory)"`
!`find . -maxdepth 5 \( -name "*.puml" -o -name "*.c4" -o -name "*.drawio" -o -name "*.mmd" \) 2>/dev/null | grep -v node_modules | head -5 || echo "(no diagram files)"`
!`grep -n -i "architecture\|container diagram\|component\|context diagram\|critical flow\|sequence" README.md 2>/dev/null | head -5 || echo "(no architecture keywords in README)"`

### C4.1 — Requirements Access
!`ls VISION.md REQUIREMENTS.md requirements.md GOALS.md 2>/dev/null || echo "(no vision/requirements files at root)"`
!`ls -d stories/ features/ user-stories/ backlog/ 2>/dev/null || echo "(no stories/backlog directory)"`
!`cat .claude/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); mcp=d.get('mcpServers',{}); print('MCP servers:', list(mcp.keys()) if mcp else 'none')" 2>/dev/null || echo "(no MCP servers configured)"`

### C5.1 — Runnability
!`ls package.json pom.xml build.gradle setup.py pyproject.toml Cargo.toml go.mod 2>/dev/null || echo "(no build system found)"`
!`cat package.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print('npm scripts:', list(d.get('scripts',{}).keys()))" 2>/dev/null || true`
!`ls Procfile docker-compose.yml docker-compose.yaml 2>/dev/null || echo "(no Procfile or docker-compose)"`
!`grep -i "^build\b\|^run\b\|^start\b\|^serve\b" Makefile 2>/dev/null | head -3 || echo "(no run/build Makefile targets)"`

### C5.2 — Unit Test Coverage
!`find . -maxdepth 4 -type d \( -name "test" -o -name "tests" -o -name "__tests__" -o -name "spec" \) 2>/dev/null | grep -v node_modules | head -5 || echo "(no test directories)"`
!`find . -maxdepth 6 \( -name "*.test.ts" -o -name "*.test.js" -o -name "*_test.py" -o -name "test_*.py" -o -name "*Test.java" -o -name "*_test.go" \) 2>/dev/null | grep -v node_modules | wc -l`
!`ls coverage/ htmlcov/ .coverage 2>/dev/null && echo "(coverage artifacts exist)" || echo "(no coverage artifacts)"`
!`cat jest.config.js jest.config.ts 2>/dev/null | grep -i "coverage\|threshold" | head -5 || grep -A5 "\[tool.coverage" pyproject.toml 2>/dev/null | head -5 || echo "(no coverage threshold config)"`

### C5.3 — Integration and E2E Coverage
!`ls cypress.config.js cypress.config.ts playwright.config.ts playwright.config.js 2>/dev/null || echo "(no Cypress/Playwright config)"`
!`ls -d cypress/ e2e/ tests/e2e/ features/ 2>/dev/null || echo "(no E2E directories)"`
!`find . -maxdepth 5 -type d -name "integration" 2>/dev/null | grep -v node_modules | head -3 || echo "(no integration test directory)"`

### C6.1 — Static Analysis
!`ls .eslintrc .eslintrc.js .eslintrc.json eslint.config.js .pylintrc .flake8 ruff.toml .rubocop.yml .golangci.yml 2>/dev/null || echo "(no linting config)"`
!`ls tsconfig.json mypy.ini .mypy.ini 2>/dev/null || echo "(no type checking config)"`
!`ls .snyk sonar-project.properties .semgrep.yml 2>/dev/null || grep -r "codeql\|snyk\|semgrep\|trivy\|bandit" .github/workflows/ 2>/dev/null | head -3 || echo "(no SAST config or CI steps)"`

### C7.1 — Test Isolation
!`find . -maxdepth 5 -type d \( -name "mocks" -o -name "__mocks__" -o -name "fixtures" -o -name "stubs" \) 2>/dev/null | grep -v node_modules | head -5 || echo "(no mock/fixture directories)"`
!`find . -maxdepth 5 \( -iname "seed*" \) \( -name "*.js" -o -name "*.ts" -o -name "*.py" -o -name "*.sql" \) 2>/dev/null | grep -v node_modules | head -5 || echo "(no seed scripts)"`
!`ls docker-compose.test.yml docker-compose.testing.yml 2>/dev/null || grep -r "testcontainer\|localstack" . 2>/dev/null --include="*.json" --include="*.ts" --include="*.js" -l | grep -v node_modules | head -3 || echo "(no test-environment isolation tools)"`

### C8.1 — CI/CD Automation
!`ls .github/workflows/ 2>/dev/null && ls .github/workflows/ || ls .gitlab-ci.yml Jenkinsfile .circleci/ 2>/dev/null || echo "(no CI config)"`
!`find .github/workflows/ -name "*.yml" -o -name "*.yaml" 2>/dev/null | xargs grep -l "deploy\|release\|publish" 2>/dev/null | head -3 || echo "(no deployment steps in CI)"`
!`grep -r "workflow_dispatch" .github/workflows/ 2>/dev/null | head -3 || echo "(no workflow_dispatch triggers)"`
!`cat .claude/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); mcp=d.get('mcpServers',{}); ci=[k for k in mcp if any(x in k.lower() for x in ['github','gitlab','ci','pipeline'])]; print('CI MCP servers:', ci if ci else 'none')" 2>/dev/null || echo "(no CI MCP servers)"`

### C8.2 — Observability
!`cat package.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); deps={**d.get('dependencies',{}),**d.get('devDependencies',{})}; obs=[k for k in deps if any(x in k for x in ['datadog','opentelemetry','@opentelemetry','sentry','newrelic','dd-trace','pino','winston'])]; print('Observability deps:', obs)" 2>/dev/null || true`
!`ls datadog.yaml prometheus.yml grafana/ 2>/dev/null || echo "(no monitoring config files)"`
!`cat .claude/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); mcp=d.get('mcpServers',{}); obs=[k for k in mcp if any(x in k.lower() for x in ['grafana','datadog','sentry','cloudwatch','monitor','metric'])]; print('Observability MCP servers:', obs if obs else 'none')" 2>/dev/null || echo "(no observability MCP servers)"`

---

## Instructions

### Step 1 — Score each criterion

Using the evidence collected above, assign a fulfillment level to each criterion:

**C1.1 Codebase Accessibility (0–2)**
- 0: No single entry point; no README
- 1: Single root with a basic README present but no CLAUDE.md/AGENTS.md
- 2: CLAUDE.md or AGENTS.md exists with conventions, commands, and navigation guidance

**C2.1 Setup Automation (0–3)**
- 0: No setup instructions anywhere
- 1: Written step-by-step instructions in README (but no script)
- 2: Single script (`setup.sh`, `npm install`, etc.) installs everything automatically
- 3: Containerised/declarative environment (.devcontainer, Nix flake, etc.)

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
- 2: App can be run locally or in an ephemeral environment (run/start script or docker-compose)

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
- 1: Agents can read pipeline status (CI config exists and is readable; CI MCP server configured)
- 2: Agents can trigger pipeline runs (workflow_dispatch or equivalent)
- 3: Full pipeline control including deployment

**C8.2 Observability (0–3)**
- 0: No access to logs or metrics
- 1: Read-only access to logs/metrics
- 2: Queryable monitoring and logs (structured query API or observability MCP server)
- 3: Automated anomaly detection and alerting

---

### Step 2 — Determine current readiness level

Use the Level–Criteria Mapping table below. Check levels in order (1, then 2, then 3). The current level is the highest where **all** applicable thresholds are met.

| Criterion | Level 1 requires | Level 2 requires | Level 3 requires |
|-----------|-----------------|-----------------|-----------------|
| C1.1 Codebase Accessibility | ≥ 1 | ≥ 2 | ≥ 2 |
| C2.1 Setup Automation | ≥ 1 | ≥ 2 | ≥ 3 |
| C3.1 Architecture Depth | — | ≥ 1 | ≥ 3 |
| C4.1 Requirements Access | — | ≥ 1 | ≥ 3 |
| C5.1 Runnability | ≥ 1 | ≥ 2 | ≥ 2 |
| C5.2 Unit Test Coverage | ≥ 1 | ≥ 2 | ≥ 3 |
| C5.3 Integration and E2E Coverage | — | ≥ 1 | ≥ 2 |
| C6.1 Static Analysis | — | ≥ 1 | ≥ 2 |
| C7.1 Test Isolation | — | — | ≥ 2 (skip if N/A) |
| C8.1 CI/CD Automation | — | ≥ 1 | ≥ 3 |
| C8.2 Observability | — | — | ≥ 2 |

Level names: 0 = Uninstrumented, 1 = Foundation, 2 = Guided Autonomy, 3 = Supervised Autonomy

---

### Step 3 — Identify the target level and blocking criteria

- If current level is 3: Report "This project is already at Level 3 — Supervised Autonomy. No further readiness improvements are possible." Stop here.
- Otherwise, target level = current level + 1.
- List every criterion where the score is below the target level's threshold. These are the **blocking criteria**.

---

### Step 4 — Report the current state

Print a summary like this before making any changes:

```
## Current Readiness

**Level**: [N] — [Level Name]
**Target**: Level [N+1] — [Level Name]

## Blocking Criteria for Level [N+1]

| Criterion | Name | Current Score | Required |
|-----------|------|---------------|----------|
| C_._ | [Name] | [score] | ≥ [threshold] |
...

## Improvements to implement

For each blocking criterion, I will now run the corresponding improve-c* logic:
- C_._ → /improve-c_-_ (current: [score] → target: [threshold])
...
```

---

### Step 5 — Implement improvements for each blocking criterion

For each blocking criterion identified in Step 4, apply the improvement logic below. Work through them in the order listed (lowest criterion ID first).

---

#### C1.1 — Codebase Accessibility (improve-c1-1 logic)

Run these bash commands to gather evidence:
- `ls CLAUDE.md AGENTS.md .claude/CLAUDE.md 2>/dev/null || echo "(none)"`
- `cat CLAUDE.md 2>/dev/null || cat AGENTS.md 2>/dev/null || echo "(empty)"`
- `head -30 README.md 2>/dev/null || echo "(no README.md)"`
- `ls -la | head -30`
- `ls src/ lib/ app/ packages/ 2>/dev/null | head -20 || echo "(no standard source directories)"`
- `cat package.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print('scripts:', d.get('scripts',{}))" 2>/dev/null || true`
- `grep -i "^build\|^test\|^run\|^start\|^dev\|^lint" Makefile 2>/dev/null | head -10 || echo "(no Makefile targets)"`

**If C1.1 = 0 → raise to 1:** Create `README.md` at the project root with: project name and description, getting started section (prerequisites, how to clone and run), basic project structure overview.

**If C1.1 = 1 → raise to 2:** Create `CLAUDE.md` at the project root. Read enough of the actual codebase to write accurate, project-specific content. Include:
```markdown
# CLAUDE.md

## Project Overview
[brief description of what this project does]

## Key Commands
[list the most important commands: build, test, run, lint — use the actual commands detected above]

## Project Structure
[describe the main directories and what lives in them]

## Coding Conventions
[list conventions: naming style, file organisation, patterns used — infer from the existing code structure]

## Important Notes
[any non-obvious constraints, environment variables required, external services, known gotchas]
```
Do not write generic placeholder text — base it on the actual project.

**If C1.1 = 2:** Already at maximum; skip.

---

#### C2.1 — Setup Automation (improve-c2-1 logic)

Run these bash commands to gather evidence:
- `cat README.md 2>/dev/null | head -80 || echo "(no README)"`
- `ls setup.sh install.sh bootstrap.sh Makefile 2>/dev/null || echo "(no scripts)"`
- `ls package.json requirements.txt Pipfile pyproject.toml pom.xml build.gradle Cargo.toml go.mod 2>/dev/null || echo "(no dependency manifests)"`
- `ls .devcontainer/ devcontainer.json flake.nix shell.nix 2>/dev/null || echo "(no containerised env)"`
- `cat Makefile 2>/dev/null | head -40 || echo "(no Makefile)"`

**If C2.1 = 0 → raise to 1:** Add a "Getting Started" section to `README.md` with: prerequisites (language runtime version, tools), numbered steps to clone and set up, how to verify it worked.

**If C2.1 = 1 → raise to 2:** Create a `setup.sh` script in the project root that automates all setup steps from the README. The script should: detect the OS, install/verify dependencies, run the dependency install command (`npm install`, `pip install`, etc.), verify the setup succeeded. Make it executable (`chmod +x setup.sh`). Update README to reference the script.

**If C2.1 = 2 → raise to 3:** Create a `.devcontainer/devcontainer.json` file. Read the project's tech stack and dependencies from the evidence. Configure it with the correct base image, VS Code extensions, post-create command (`npm install`, etc.), and any required environment variables. Add a brief `DEVCONTAINER.md` or update README explaining how to use it.

**If C2.1 = 3:** Already at maximum; skip.

---

#### C3.1 — Architecture Depth (improve-c3-1 logic)

Run these bash commands to gather evidence:
- `cat README.md 2>/dev/null || echo "(no README)"`
- `find . -maxdepth 4 \( -iname "ARCHITECTURE.md" -o -iname "architecture.md" -o -iname "DESIGN.md" \) 2>/dev/null | grep -v node_modules | head -5 || echo "(none)"`
- `cat ARCHITECTURE.md 2>/dev/null || cat docs/ARCHITECTURE.md 2>/dev/null || echo "(no architecture file)"`
- `find docs/ -name "*.md" 2>/dev/null | head -10 || echo "(no docs/)"`
- `ls src/ lib/ app/ packages/ services/ 2>/dev/null | head -20 || echo "(no source dirs)"`
- `find . -maxdepth 3 -type d 2>/dev/null | grep -v node_modules | grep -v ".git" | head -30`

**If C3.1 = 0 → raise to 1:** Create `ARCHITECTURE.md` at the project root with a system context section: what the system does, who its users are, what external systems it integrates with, and a high-level description of the main components. Read the codebase to infer this — do not write placeholders.

**If C3.1 = 1 → raise to 2:** Expand `ARCHITECTURE.md` (or create `docs/architecture/`) to document container/service level: main services or modules, their responsibilities, how they communicate, key data flows between them. Include a text-based or Mermaid diagram if appropriate.

**If C3.1 = 2 → raise to 3:** Extend architecture docs to component level: for each major service/module, document its internal components, their responsibilities, and how they interact. Document at least 2–3 critical flows end-to-end (e.g., "user login", "order placement") as sequence descriptions or Mermaid sequence diagrams.

**If C3.1 = 3:** Already at maximum; skip.

---

#### C4.1 — Requirements Access (improve-c4-1 logic)

Run these bash commands to gather evidence:
- `cat VISION.md 2>/dev/null || cat REQUIREMENTS.md 2>/dev/null || echo "(no vision/requirements file)"`
- `ls -d stories/ features/ user-stories/ backlog/ 2>/dev/null || echo "(no stories directory)"`
- `cat README.md 2>/dev/null | head -100 || echo "(no README)"`
- `head -50 src/index.ts src/index.js src/main.py app/main.py main.go 2>/dev/null || find . -maxdepth 3 \( -name "main.*" -o -name "index.*" \) 2>/dev/null | grep -v node_modules | head -5 || echo "(no obvious entry points)"`
- `grep -r "app\.\(get\|post\|put\|delete\|patch\)\|router\.\(get\|post\)" --include="*.js" --include="*.ts" -h . 2>/dev/null | grep -v node_modules | head -20 || echo "(no route definitions)"`

**If C4.1 = 0 → raise to 1:** Create `VISION.md` at the project root. Infer the product's purpose, users, and goals from the README and codebase. Include: Problem (what it solves), Users (who uses it), Goals (3–5 key product goals), Non-goals (what is out of scope), Success metrics. Base on actual evidence — no placeholders.

**If C4.1 = 1 → raise to 2:** Create a `stories/` directory with: `stories/README.md` (explaining the format), and one `.md` file per major feature area, each with 3–5 user stories in this format:
```
## [Feature Name]

**As a** [user type],
**I want to** [action],
**so that** [benefit].

**Acceptance criteria:**
- [ ] [specific, testable criterion]
```
Infer features from routes, controllers, and existing code. Aim for 10–20 stories covering main functionality.

**If C4.1 = 2 → raise to 3:** Level 3 requires programmatic access via MCP server — this cannot be fully automated. Explain what is needed: configure an MCP server connection to GitHub Issues, Linear, Jira, or Notion in `.claude/settings.json`. Document the required configuration in README or a new `MCP_SETUP.md`.

**If C4.1 = 3:** Already at maximum; skip.

---

#### C5.1 — Runnability (improve-c5-1 logic)

Run these bash commands to gather evidence:
- `cat README.md 2>/dev/null | head -60 || echo "(no README)"`
- `cat package.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(json.dumps(d.get('scripts',{}), indent=2))" 2>/dev/null || true`
- `cat Makefile 2>/dev/null | head -60 || echo "(no Makefile)"`
- `ls Procfile docker-compose.yml docker-compose.yaml 2>/dev/null || echo "(no Procfile or docker-compose)"`
- `ls src/ app/ 2>/dev/null | head -10 || echo "(no source)"`

**If C5.1 = 0 → raise to 1:** The project does not build. Investigate the build errors, fix them, and ensure `npm run build` / `cargo build` / `python -m py_compile` / etc. exits cleanly. Document the build command in README.

**If C5.1 = 1 → raise to 2:** The project builds but cannot be run. Add a run mechanism: add a `start` or `dev` npm script, create a `docker-compose.yml`, or add a `run` Makefile target. Document how to run the app in README. If the project is a library (not an app), mark C5.1 as N/A at level 2 and explain why.

**If C5.1 = 2:** Already at maximum; skip.

---

#### C5.2 — Unit Test Coverage (improve-c5-2 logic)

Run these bash commands to gather evidence:
- `find . -maxdepth 4 -type d \( -name "test" -o -name "tests" -o -name "__tests__" -o -name "spec" \) 2>/dev/null | grep -v node_modules | head -5`
- `find . -maxdepth 6 \( -name "*.test.ts" -o -name "*.test.js" -o -name "*_test.py" -o -name "test_*.py" -o -name "*Test.java" -o -name "*_test.go" \) 2>/dev/null | grep -v node_modules | head -20`
- `cat jest.config.js jest.config.ts 2>/dev/null | head -30 || cat pyproject.toml 2>/dev/null | grep -A10 "\[tool.pytest" | head -15 || echo "(no test config)"`
- `ls src/ app/ lib/ 2>/dev/null | head -20`

**If C5.2 = 0 → raise to 1:** No tests exist. Set up the test framework (Jest for JS/TS, pytest for Python, etc.), write tests for the 2–3 most critical functions or modules. Add a `test` script to package.json / Makefile.

**If C5.2 = 1 → raise to 2:** Tests exist but coverage is below 50%. Read the existing tests and source files. Identify the most important untested modules. Write additional tests to meaningfully increase coverage toward 50%. Configure coverage reporting (`jest --coverage`, `pytest --cov`, etc.).

**If C5.2 = 2 → raise to 3:** Coverage is between 50–80%. Add tests for currently uncovered paths. Focus on edge cases, error handling, and branches. Enable a coverage threshold (e.g., `coverageThreshold: { global: { lines: 80 } }` in jest.config).

**If C5.2 = 3:** Already at maximum; skip.

---

#### C5.3 — Integration and E2E Coverage (improve-c5-3 logic)

Run these bash commands to gather evidence:
- `ls cypress.config.js cypress.config.ts playwright.config.ts playwright.config.js 2>/dev/null || echo "(no E2E config)"`
- `find . -maxdepth 5 -type d -name "integration" 2>/dev/null | grep -v node_modules | head -5`
- `ls -d cypress/ e2e/ tests/e2e/ features/ 2>/dev/null || echo "(no E2E directories)"`
- `cat package.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); deps={**d.get('dependencies',{}),**d.get('devDependencies',{})}; print('relevant deps:', [k for k in deps if any(x in k for x in ['cypress','playwright','supertest','jest-integration'])])" 2>/dev/null || true`
- `ls src/ app/ lib/ 2>/dev/null | head -10`

**If C5.3 = 0 → raise to 1:** No integration tests exist. Set up integration tests for key service boundaries. For a REST API: use supertest (Node) or pytest with httpx/requests (Python) to test key endpoints end-to-end. Create `tests/integration/` directory, write 3–5 integration tests covering the most critical API boundaries. Add an `test:integration` script.

**If C5.3 = 1 → raise to 2:** Integration tests exist but no E2E tests. Set up Playwright or Cypress for a UI project, or add E2E API flow tests for a backend. Create `e2e/` or `tests/e2e/` directory, write 3–5 E2E tests covering critical user flows. Add an `test:e2e` script.

**If C5.3 = 2 → raise to 3:** E2E tests exist. If the project has a UI, add visual regression testing (Playwright screenshots, Percy, or Chromatic). If no UI, mark as already at effective maximum and report N/A for visual regression.

**If C5.3 = 3:** Already at maximum; skip.

---

#### C6.1 — Static Analysis (improve-c6-1 logic)

Run these bash commands to gather evidence:
- `ls .eslintrc .eslintrc.js .eslintrc.json eslint.config.js .pylintrc .flake8 ruff.toml .rubocop.yml .golangci.yml 2>/dev/null || echo "(no linting config)"`
- `ls tsconfig.json mypy.ini .mypy.ini 2>/dev/null || echo "(no type checking config)"`
- `cat tsconfig.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); o=d.get('compilerOptions',{}); print('strict:', o.get('strict'), 'noImplicitAny:', o.get('noImplicitAny'))" 2>/dev/null || true`
- `ls .snyk sonar-project.properties .semgrep.yml 2>/dev/null || grep -r "codeql\|snyk\|semgrep\|trivy\|bandit" .github/workflows/ 2>/dev/null | head -3 || echo "(no SAST config)"`
- `cat package.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); deps={**d.get('dependencies',{}),**d.get('devDependencies',{})}; print('relevant:', [k for k in deps if any(x in k for x in ['eslint','prettier','typescript','@typescript'])])" 2>/dev/null || true`
- `ls *.json *.toml *.yml 2>/dev/null | head -10`

**If C6.1 = 0 → raise to 1:** No linting/formatting configured. Install and configure a linter appropriate for the project language:
- JS/TS: install `eslint` and `prettier`, create `eslint.config.js` (or `.eslintrc.json`) and `.prettierrc`; add `lint` and `format` npm scripts.
- Python: install `ruff` (covers linting + formatting), create `ruff.toml`; add a `lint` target.
- Go: configure `.golangci.yml`.
- Other: choose the community-standard linter.

**If C6.1 = 1 → raise to 2:** Linting exists; add type checking:
- TS: ensure `tsconfig.json` has `"strict": true` (or at minimum `"noImplicitAny": true`); add a `typecheck` npm script (`tsc --noEmit`).
- Python: install `mypy`, create `mypy.ini`, add a `typecheck` target.
- Other: configure the language's type checker.
Fix any type errors introduced.

**If C6.1 = 2 → raise to 3:** Linting and type checking exist; add SAST:
- Add a GitHub Actions workflow step (if CI exists) running CodeQL, Semgrep, or Trivy.
- Or create a `.semgrep.yml` config running `semgrep --config=auto`.
- Or integrate `snyk` via a CI step.

**If C6.1 = 3:** Already at maximum; skip.

---

#### C7.1 — Test Isolation (improve-c7-1 logic)

Run these bash commands to gather evidence:
- `find . -maxdepth 5 -type d \( -name "mocks" -o -name "__mocks__" -o -name "fixtures" -o -name "stubs" \) 2>/dev/null | grep -v node_modules | head -5 || echo "(no mock/fixture directories)"`
- `find . -maxdepth 5 \( -iname "seed*" \) \( -name "*.js" -o -name "*.ts" -o -name "*.py" -o -name "*.sql" \) 2>/dev/null | grep -v node_modules | head -5 || echo "(no seed scripts)"`
- `ls docker-compose.test.yml docker-compose.testing.yml 2>/dev/null || echo "(none)"`
- `grep -r "testcontainer\|localstack\|pg\|postgres\|mysql\|redis\|mongodb" --include="*.json" --include="*.ts" --include="*.js" -l . 2>/dev/null | grep -v node_modules | head -5 || echo "(no DB or external deps detected)"`

**If C7.1 = N/A (no external dependencies):** Skip; report N/A.

**If C7.1 = 0 → raise to 1:** Create `tests/__mocks__/` or `tests/fixtures/` directory. Add mocks/stubs for any external HTTP calls (using `jest.mock`, `unittest.mock`, `responses`, etc.). Add basic fixture data files (JSON/YAML/SQL) representing test data.

**If C7.1 = 1 → raise to 2:** Create a `docker-compose.test.yml` with the database/external services needed for tests. Add a seed script (e.g., `tests/fixtures/seed.sql` or `scripts/seed.ts`) that populates the test database with known data. Update the integration test setup to use this ephemeral environment.

**If C7.1 = 2:** Already at maximum; skip.

---

#### C8.1 — CI/CD Automation (improve-c8-1 logic)

Run these bash commands to gather evidence:
- `ls .github/workflows/ 2>/dev/null && cat .github/workflows/*.yml 2>/dev/null | head -60 || echo "(no GitHub Actions)"`
- `ls .gitlab-ci.yml Jenkinsfile .circleci/ 2>/dev/null || echo "(no other CI)"`
- `grep -r "workflow_dispatch" .github/workflows/ 2>/dev/null | head -5 || echo "(no workflow_dispatch)"`
- `grep -r "deploy\|release\|publish" .github/workflows/ 2>/dev/null | head -10 || echo "(no deployment steps)"`
- `cat .claude/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); mcp=d.get('mcpServers',{}); print('MCP servers:', list(mcp.keys()))" 2>/dev/null || echo "(no MCP servers)"`

**If C8.1 = 0 → raise to 1:** No CI pipeline exists. Create `.github/workflows/ci.yml` with a basic pipeline that: checks out code, sets up the runtime (node, python, etc.), installs dependencies, runs lint, runs tests, reports status. This gives agents read access to pipeline status via the GitHub MCP or GitHub CLI.

**If C8.1 = 1 → raise to 2:** CI exists but agents cannot trigger it. Add `workflow_dispatch:` trigger to the main CI workflow. This allows agents (and humans) to trigger runs via the GitHub API or GitHub MCP server.

**If C8.1 = 2 → raise to 3:** CI can be triggered but lacks deployment. Add a deployment job to the CI workflow: build the production artifact, deploy to staging/production (using the appropriate provider). Level 3 requires full pipeline control including deployment — document the deployment target and add the necessary secrets/environment configuration instructions to README.

**If C8.1 = 3:** Already at maximum; skip.

---

#### C8.2 — Observability (improve-c8-2 logic)

Run these bash commands to gather evidence:
- `cat package.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); deps={**d.get('dependencies',{}),**d.get('devDependencies',{})}; obs=[k for k in deps if any(x in k for x in ['datadog','opentelemetry','sentry','newrelic','dd-trace','pino','winston','bunyan'])]; print('Observability deps:', obs)" 2>/dev/null || true`
- `ls datadog.yaml prometheus.yml grafana/ 2>/dev/null || echo "(no monitoring config files)"`
- `cat .claude/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); mcp=d.get('mcpServers',{}); obs=[k for k in mcp if any(x in k.lower() for x in ['grafana','datadog','sentry','cloudwatch','monitor','metric'])]; print('Observability MCP servers:', obs if obs else 'none')" 2>/dev/null || echo "(no observability MCP servers)"`

**If C8.2 = 0 → raise to 1:** No observability. Add structured logging to the application:
- JS/TS: install `pino` or `winston`, replace `console.log` calls with structured logger calls.
- Python: configure `logging` with JSON formatter or install `structlog`.
Emit logs to stdout in JSON format so they can be read from CI/runtime logs. Document how to access logs in README.

**If C8.2 = 1 → raise to 2:** Logs exist but are not queryable. Configure a queryable monitoring/logging backend:
- Add a Grafana + Loki or Datadog MCP server to `.claude/settings.json` so agents can query logs programmatically.
- Or configure OpenTelemetry export to a collector and document the query API.
This step may require external infrastructure; document what is needed and configure as much as can be automated.

**If C8.2 = 2 → raise to 3:** Queryable logs exist. Add automated alerting: configure alert rules in Grafana, Datadog, or equivalent (error rate thresholds, latency SLOs). Document the alerting setup.

**If C8.2 = 3:** Already at maximum; skip.

---

### Step 6 — Final report

After completing all improvements, produce a summary:

```
## Improvement Summary

**Previous level**: Level [N] — [Name]
**New level**: Level [N+1] — [Name] (if all blocking criteria have been resolved)

### Changes made

| Criterion | Before | After | Change |
|-----------|--------|-------|--------|
| C_._ [Name] | [old score] | [new score] | [file/action] |
...

### Remaining gaps (if any)

[List any criteria that could not be fully automated, e.g., C4.1 → 3 requires MCP infrastructure, C8.2 → 2 requires external monitoring setup. Explain what manual steps the team needs to take.]

### Next steps

[If still below Level 3, note what the next improvement cycle would target.]
```
