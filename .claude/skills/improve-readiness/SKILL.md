---
name: improve-readiness
description: Assess the current readiness level of the project and implement all improvements needed to raise it to the next level. Runs the relevant improve-c* logic for each blocking criterion inline.
allowed-tools: Bash Read Write Edit
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Improve Readiness Level

This skill assesses the current readiness level of the project, identifies which criteria block the next level, and then implements the improvements for each blocking criterion directly.

---

## Evidence to Gather

Before scoring, examine the project for evidence relevant to each criterion. Use your knowledge of the project structure and tech stack to look in the right places.

### C1.1 — Codebase Accessibility
Check for agent context files (`CLAUDE.md`, `AGENTS.md`, or equivalent) and read their content. Check for a README and assess its depth.

### C2.1 — Setup Automation
Check for a containerised or declarative environment. Look for setup scripts and relevant Makefile targets. Check for dependency manifests. Read the README setup section.

### C3.1 — Architecture Depth
Look for architecture documentation files and diagram files. Check the README for architecture content.

### C4.1 — Requirements Access
Look for vision or requirements files. Check for stories or backlog directories. Check the MCP server configuration for any PM tool connections.

### C5.1 — Runnability
Identify the build system from the dependency manifest. Look for build/run scripts and runtime configuration (Procfile, docker-compose, etc.).

### C5.2 — Unit Test Coverage
Look for test directories and test files. Look for coverage configuration and report artifacts.

### C5.3 — Integration and E2E Coverage
Look for E2E framework configuration and test directories. Look for integration test directories.

### C6.1 — Static Analysis
Look for linting and formatting configuration files. Look for type checking configuration. Look for security scanning configuration and CI steps.

### C7.1 — Test Isolation
Check if the project has external dependencies. If yes: look for mock/fixture directories, seed scripts, and test-specific container configuration.

### C8.1 — CI/CD Automation
Look for CI configuration files and read them. Check the MCP server configuration for pipeline access. Look for `workflow_dispatch` triggers and deployment steps.

### C8.2 — Observability
Check dependency manifests for logging and observability libraries. Look for monitoring configuration files. Check the MCP server configuration for observability access.

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

Look at the project to gather evidence: check for agent context files and read their content; read the README; look at the project structure and identify the technology stack; identify key build, run, and test commands.

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

Look at the project to gather evidence: check for containerised/declarative environment; look for setup scripts and Makefile targets; identify the dependency manifest and install command; read the README setup section.

**If C2.1 = 0 → raise to 1:** Add a "Getting Started" section to `README.md` with: prerequisites (language runtime version, tools), numbered steps to clone and set up, how to verify it worked.

**If C2.1 = 1 → raise to 2:** Create a `setup.sh` script in the project root that automates all setup steps from the README. The script should: detect the OS, install/verify dependencies, run the dependency install command (`npm install`, `pip install`, etc.), verify the setup succeeded. Make it executable (`chmod +x setup.sh`). Update README to reference the script.

**If C2.1 = 2 → raise to 3:** Create a `.devcontainer/devcontainer.json` file. Read the project's tech stack and dependencies from the evidence. Configure it with the correct base image, VS Code extensions, post-create command (`npm install`, etc.), and any required environment variables. Add a brief `DEVCONTAINER.md` or update README explaining how to use it.

**If C2.1 = 3:** Already at maximum; skip.

---

#### C3.1 — Architecture Depth (improve-c3-1 logic)

Look at the project to gather evidence: check for existing architecture documentation and read it; look at the directory structure and any multi-service configuration to understand the system; read the README; browse route/handler files to understand the API surface.

**If C3.1 = 0 → raise to 1:** Create `ARCHITECTURE.md` at the project root with a system context section: what the system does, who its users are, what external systems it integrates with, and a high-level description of the main components. Read the codebase to infer this — do not write placeholders.

**If C3.1 = 1 → raise to 2:** Expand `ARCHITECTURE.md` (or create `docs/architecture/`) to document container/service level: main services or modules, their responsibilities, how they communicate, key data flows between them. Include a text-based or Mermaid diagram if appropriate.

**If C3.1 = 2 → raise to 3:** Extend architecture docs to component level: for each major service/module, document its internal components, their responsibilities, and how they interact. Document at least 2–3 critical flows end-to-end (e.g., "user login", "order placement") as sequence descriptions or Mermaid sequence diagrams.

**If C3.1 = 3:** Already at maximum; skip.

---

#### C4.1 — Requirements Access (improve-c4-1 logic)

Look at the project to gather evidence: check for existing vision or requirements files and read them; look for stories or backlog directories; check MCP configuration for PM tool connections; read the README and browse source files to understand what the system does.

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

Look at the project to gather evidence: identify the language and build system from the dependency manifest; look for build and run scripts and Makefile targets; look for runtime configuration such as Procfile or docker-compose; read the README for build and run instructions.

**If C5.1 = 0 → raise to 1:** The project does not build. Investigate the build errors, fix them, and ensure `npm run build` / `cargo build` / `python -m py_compile` / etc. exits cleanly. Document the build command in README.

**If C5.1 = 1 → raise to 2:** The project builds but cannot be run. Add a run mechanism: add a `start` or `dev` npm script, create a `docker-compose.yml`, or add a `run` Makefile target. Document how to run the app in README. If the project is a library (not an app), mark C5.1 as N/A at level 2 and explain why.

**If C5.1 = 2:** Already at maximum; skip.

---

#### C5.2 — Unit Test Coverage (improve-c5-2 logic)

Look at the project to gather evidence: look for test directories and test files; identify the test framework from the manifest or config files; look for coverage configuration and existing coverage reports; look at source directories to understand the scope of untested code.

**If C5.2 = 0 → raise to 1:** No tests exist. Set up the test framework (Jest for JS/TS, pytest for Python, etc.), write tests for the 2–3 most critical functions or modules. Add a `test` script to package.json / Makefile.

**If C5.2 = 1 → raise to 2:** Tests exist but coverage is below 50%. Read the existing tests and source files. Identify the most important untested modules. Write additional tests to meaningfully increase coverage toward 50%. Configure coverage reporting (`jest --coverage`, `pytest --cov`, etc.).

**If C5.2 = 2 → raise to 3:** Coverage is between 50–80%. Add tests for currently uncovered paths. Focus on edge cases, error handling, and branches. Enable a coverage threshold (e.g., `coverageThreshold: { global: { lines: 80 } }` in jest.config).

**If C5.2 = 3:** Already at maximum; skip.

---

#### C5.3 — Integration and E2E Coverage (improve-c5-3 logic)

Look at the project to gather evidence: look for E2E framework configuration and test directories; look for integration test directories and files; check the dependency manifest for E2E testing libraries and visual regression tools; look at source directories to understand the main flows to cover.

**If C5.3 = 0 → raise to 1:** No integration tests exist. Set up integration tests for key service boundaries. For a REST API: use supertest (Node) or pytest with httpx/requests (Python) to test key endpoints end-to-end. Create `tests/integration/` directory, write 3–5 integration tests covering the most critical API boundaries. Add an `test:integration` script.

**If C5.3 = 1 → raise to 2:** Integration tests exist but no E2E tests. Set up Playwright or Cypress for a UI project, or add E2E API flow tests for a backend. Create `e2e/` or `tests/e2e/` directory, write 3–5 E2E tests covering critical user flows. Add an `test:e2e` script.

**If C5.3 = 2 → raise to 3:** E2E tests exist. If the project has a UI, add visual regression testing (Playwright screenshots, Percy, or Chromatic). If no UI, mark as already at effective maximum and report N/A for visual regression.

**If C5.3 = 3:** Already at maximum; skip.

---

#### C6.1 — Static Analysis (improve-c6-1 logic)

Look at the project to gather evidence: identify the language and build system; look for linting and formatting configuration files; look for type checking configuration; look for security scanning configuration files and CI steps; check the build scripts and Makefile for existing quality commands.

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

Look at the project to gather evidence: check the manifest and source files for external dependencies such as databases or external APIs (this determines applicability); look for mock, stub, or fixture directories; look for seed scripts; look for test-specific container configuration.

**If C7.1 = N/A (no external dependencies):** Skip; report N/A.

**If C7.1 = 0 → raise to 1:** Create `tests/__mocks__/` or `tests/fixtures/` directory. Add mocks/stubs for any external HTTP calls (using `jest.mock`, `unittest.mock`, `responses`, etc.). Add basic fixture data files (JSON/YAML/SQL) representing test data.

**If C7.1 = 1 → raise to 2:** Create a `docker-compose.test.yml` with the database/external services needed for tests. Add a seed script (e.g., `tests/fixtures/seed.sql` or `scripts/seed.ts`) that populates the test database with known data. Update the integration test setup to use this ephemeral environment.

**If C7.1 = 2:** Already at maximum; skip.

---

#### C8.1 — CI/CD Automation (improve-c8-1 logic)

Look at the project to gather evidence: look for CI configuration files and read them; check for manual trigger support; check the MCP configuration for pipeline access; look for deployment steps in existing workflows and any infrastructure configuration.

**If C8.1 = 0 → raise to 1:** No CI pipeline exists. Create `.github/workflows/ci.yml` with a basic pipeline that: checks out code, sets up the runtime (node, python, etc.), installs dependencies, runs lint, runs tests, reports status. This gives agents read access to pipeline status via the GitHub MCP or GitHub CLI.

**If C8.1 = 1 → raise to 2:** CI exists but agents cannot trigger it. Add `workflow_dispatch:` trigger to the main CI workflow. This allows agents (and humans) to trigger runs via the GitHub API or GitHub MCP server.

**If C8.1 = 2 → raise to 3:** CI can be triggered but lacks deployment. Add a deployment job to the CI workflow: build the production artifact, deploy to staging/production (using the appropriate provider). Level 3 requires full pipeline control including deployment — document the deployment target and add the necessary secrets/environment configuration instructions to README.

**If C8.1 = 3:** Already at maximum; skip.

---

#### C8.2 — Observability (improve-c8-2 logic)

Look at the project to gather evidence: check the dependency manifest for logging and observability libraries; look for monitoring configuration files; check the MCP configuration for observability servers; look for alerting configuration files; identify the language and framework from the manifest and main entry point.

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
