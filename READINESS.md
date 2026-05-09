# Agent Readiness Maturity Model

## Overview

This model evaluates how ready a software project is for agentic coding. "Readiness" measures the structural, environmental, and documentary properties of a codebase that determine how effectively an AI agent can understand, navigate, modify, and verify the project.

Agentic coding amplifies what is already there: a well-structured, well-tested, well-documented project benefits enormously; a chaotic one becomes harder to manage. This model allows teams to assess their starting point and prioritise improvements before or during agentic adoption.

---

## Levels

### Level 0 — Uninstrumented

The project provides no meaningful context or feedback to an agent. Applying agentic coding produces little to no benefit and risks introducing hard-to-detect regressions.

An agent operating at this level is essentially guessing: it cannot understand the system's purpose, cannot verify correctness, and cannot reproduce the development environment.

**Typical state:**
- No documentation beyond scattered inline comments
- No automated tests of any kind
- No reproducible development environment
- Codebase may be split across repositories with no clear entry point
- Build/run instructions exist only in someone's head

---

### Level 1 — Foundation

The project has enough structure for an agent to take small, targeted steps. A human must micromanage each step: reviewing every change, providing explicit context, and manually verifying output. Agents have a basic feedback mechanism (compilation, a handful of unit tests) but lack broader understanding of the system.

**Typical state:**
- All source code is accessible from a single entry point
- A human can set up the development environment by following written instructions
- The project builds and reports compilation errors
- A small number of unit tests exist (coverage is low but non-zero)
- A high-level description of the project's purpose exists in a README or similar

---

### Level 2 — Guided Autonomy

Humans guide agents at the story or feature level rather than step by step. Agents have enough context to plan implementations, write tests, navigate the architecture, and execute multi-step tasks. Feedback loops exist but are not comprehensive — agents can confirm correctness for the unit they changed but may miss cross-cutting effects.

**Typical state:**
- Development environment can be set up automatically (script or devcontainer)
- Architecture documentation covers the system context and major services
- Requirements are accessible within the repository or via tooling
- Meaningful unit test coverage (>50%) provides reliable feedback
- Integration tests cover key service boundaries
- Linting and type-checking are automated and provide immediate feedback
- Agents can run the full test suite locally

---

### Level 3 — Supervised Autonomy

Humans operate at a strategic level: defining goals, reviewing outcomes, and handling exceptions. Agents can autonomously implement most stories end-to-end, from understanding the requirement through to deploying the change. Feedback loops are comprehensive — including end-to-end tests, UI verification (where applicable), and observable production behaviour.

**Typical state:**
- Fully reproducible development environment (devcontainer, Nix, or equivalent)
- Comprehensive architecture documentation from system context down to component level
- High unit test coverage (>80%) plus integration and end-to-end tests
- UI tests with screenshot diffing or visual regression (if a UI is present)
- Reproducible database state (seed scripts, migrations, test fixtures)
- Automated deployment pipeline; agents can trigger and verify deployments
- Requirements management tool is accessible to agents (via MCP server or API)
- Monitoring and logs are queryable, enabling agents to verify production behaviour

---

## Criteria

Each criterion has 2–4 fulfillment levels (0 = absent, higher = more capable). Binary criteria have levels 0 and 1 only. The level assignment rules specify which criteria and at which fulfillment level are required for each readiness level.

---

### C1 — Codebase Accessibility

The degree to which an agent can see, navigate, and orient itself within the codebase.

| ID | Criterion | 0 | 1 | 2 |
|----|-----------|---|---|---|
| C1.1 | Codebase accessibility | Code split across unlinked repos with no entry point | All code reachable from a single root with a basic README | Comprehensive entry-point guide (CLAUDE.md or equivalent) with conventions and navigation hints |

---

### C2 — Development Environment Reproducibility

The degree to which an agent can set up a working development environment without human intervention.

| ID | Criterion | 0 | 1 | 2 | 3 |
|----|-----------|---|---|---|---|
| C2.1 | Setup automation | No setup instructions | Written step-by-step instructions | Single script installs all dependencies | Containerised environment (devcontainer, Nix, etc.) |

---

### C3 — Architecture Documentation

The degree to which an agent can understand the structure, boundaries, and responsibilities of the system. All documentation must live in-repo (or be accessible via MCP) to count.

| ID | Criterion | 0 | 1 | 2 | 3 |
|----|-----------|---|---|---|---|
| C3.1 | Architecture depth | No in-repo architecture docs | System context documented (users, external systems) | Container/service level documented | Component level documented + critical flows documented |

---

### C4 — Requirements and Specifications

The degree to which an agent can understand what the system is supposed to do and access the work backlog.

| ID | Criterion | 0 | 1 | 2 | 3 |
|----|-----------|---|---|---|---|
| C4.1 | Requirements access | No documented requirements | Product vision and goals documented | User stories or acceptance criteria accessible | Full programmatic access via MCP server or API |

---

### C5 — Testing and Feedback Loops

The degree to which an agent can verify that changes are correct and have not caused regressions.

| ID | Criterion | 0 | 1 | 2 | 3 |
|----|-----------|---|---|---|---|
| C5.1 | Runnability | Project does not build | Project builds without errors | App can be run locally or in an ephemeral environment | — |
| C5.2 | Unit test coverage | No unit tests | Some tests present (<50% coverage) | ≥50% coverage | ≥80% coverage |
| C5.3 | Integration and E2E coverage | No automated integration or E2E tests | Integration tests cover key boundaries | E2E tests cover critical flows | E2E + UI visual regression (if UI present) |

---

### C6 — Code Quality Tooling

The degree to which automated tools can give an agent immediate, actionable feedback on code quality.

| ID | Criterion | 0 | 1 | 2 | 3 |
|----|-----------|---|---|---|---|
| C6.1 | Static analysis | No quality tooling | Linting and/or formatting configured | + Type checking enforced | + Security scanning (SAST) |

---

### C7 — Data and External Dependencies

The degree to which an agent can work with realistic data and test integrations with external systems.

| ID | Criterion | 0 | 1 | 2 |
|----|-----------|---|---|---|
| C7.1 | Test isolation (if applicable) | No isolation from external systems or data | In-code mocks/stubs and basic fixtures | Reproducible DB state via seed scripts + sandbox environments from vendors |

---

### C8 — Deployment and Operations

The degree to which an agent can deploy, monitor, and verify changes in production-like environments.

| ID | Criterion | 0 | 1 | 2 | 3 |
|----|-----------|---|---|---|---|
| C8.1 | CI/CD automation | No access to pipeline | Agents can read pipeline status | Agents can trigger pipeline runs | Full pipeline control including deployment |
| C8.2 | Observability | No access to logs or metrics | Read-only access to logs/metrics | Queryable monitoring and logs | Automated anomaly detection and alerting |

---

## Level–Criteria Mapping (Preliminary)

Minimum fulfillment levels required to reach each readiness level.

| Criterion | Level 1 | Level 2 | Level 3 |
|-----------|---------|---------|---------|
| C1.1 Codebase accessibility | 1 | 2 | 2 |
| C2.1 Setup automation | 1 | 2 | 3 |
| C3.1 Architecture depth | — | 1 | 2 |
| C4.1 Requirements access | — | 1 | 2 |
| C5.1 Runnability | 1 | 2 | 2 |
| C5.2 Unit test coverage | 1 | 2 | 3 |
| C5.3 Integration and E2E coverage | — | 1 | 2 |
| C6.1 Static analysis | — | 1 | 2 |
| C7.1 Test isolation | — | — | 2 |
| C8.1 CI/CD automation | — | 1 | 2 |
| C8.2 Observability | — | — | 1 |

---

## Notes and Assumptions

- **Applicability**: Not all criteria apply to every project type. C5.3 level 3 (UI visual regression) and C7.1 may be omitted for projects without a frontend or external dependencies, and their omission does not reduce the level.
- **Human in the loop**: Even at Level 3, humans remain in the loop. The model describes the degree of autonomy that is *possible*, not the degree that is *required* or *safe* in any given context.
- **Model evolution**: This is a living document. As the practice of agentic coding matures, the criteria and thresholds will be revised.
