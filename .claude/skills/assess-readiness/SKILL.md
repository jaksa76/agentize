---
name: assess-readiness
description: Assess the Agent Readiness level of the current project across all 11 criteria (C1.1–C8.2) and produce a structured report with the achieved level, per-criterion scores, gaps, and recommendations.
allowed-tools: Bash Read
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Agent Readiness Assessment

This skill collects evidence for all 11 readiness criteria and instructs you to
score each one, determine the overall readiness level, and produce a full report.

---

## Evidence to Gather

Before scoring, examine the project for evidence relevant to each criterion. Use your knowledge of the project structure and tech stack to look in the right places.

### C1.1 — Codebase Accessibility
Check for agent context files (`CLAUDE.md`, `AGENTS.md`, or equivalent) and read their content. Check for a README. Look for any indicators of a multi-repo setup.

### C2.1 — Setup Automation
Check for a containerised or declarative environment. Look for setup or install scripts and relevant Makefile targets. Check for standard dependency manifests. Read the README setup section.

### C3.1 — Architecture Depth
Look for architecture documentation files at the project root and in a `docs/` directory. Look for diagram files. Check the README for architecture content. Read any primary architecture document to assess its depth.

### C4.1 — Requirements Access
Look for vision or requirements files at the project root. Check a `docs/` directory for specification documents. Look for a stories, features, or backlog directory. Check the MCP server configuration for any PM tool connections.

### C5.1 — Runnability
Identify the build system from the dependency manifest. Look for build and run scripts. Look for runtime configuration (Procfile, docker-compose, etc.). Check the README for build and run instructions.

### C5.2 — Unit Test Coverage
Look for test directories and test files. Look for coverage configuration or threshold settings. Check for existing coverage report artifacts. Look for a CI step that measures coverage.

### C5.3 — Integration and E2E Coverage
Look for integration test directories and files. Look for E2E test framework configuration and test directories. Check dependency manifests for E2E or visual regression testing libraries.

### C6.1 — Static Analysis
Look for linting and formatting configuration files. Look for type checking configuration. Look for security scanning (SAST) configuration files and CI steps.

### C7.1 — Test Isolation
First check if the project has external dependencies (database, APIs). If not, note N/A. Otherwise: look for mock/stub/fixture directories and files, seed scripts, and test-specific container configuration.

### C8.1 — CI/CD Automation
Look for CI configuration files and read them. Check the MCP server configuration for CI/pipeline access. Look for manual trigger support. Look for deployment steps and infrastructure configuration.

### C8.2 — Observability
Check dependency manifests for logging and observability libraries. Look for monitoring configuration files. Check the MCP server configuration for observability access. Look for alerting configuration.

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
