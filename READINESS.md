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

Criteria are grouped into thematic categories. Each criterion is assessed independently; the level assignment rules (defined separately) specify which criteria and at which fulfillment levels are required for each readiness level.

---

### C1 — Codebase Accessibility

The degree to which an agent can see and navigate the entire codebase relevant to a task.

| ID   | Criterion | Notes |
|------|-----------|-------|
| C1.1 | All source code reachable from a single root | Monorepo or git submodules configured; no hidden/private sub-repos required to run the project |
| C1.2 | Clear project structure with an entry-point document | README, CLAUDE.md, or equivalent at the root that orients a new reader |
| C1.3 | Dependency graph is explicit and navigable | Package manifests (package.json, pyproject.toml, etc.) are present and up to date |
| C1.4 | No hard-coded absolute paths or environment-specific assumptions in source | Code can be checked out anywhere and still understood |

---

### C2 — Development Environment Reproducibility

The degree to which an agent can set up a working development environment without human intervention.

| ID   | Criterion | Notes |
|------|-----------|-------|
| C2.1 | Written setup instructions exist | README or docs contain step-by-step setup guide |
| C2.2 | Setup is scriptable | A single script (e.g., `make setup`, `./scripts/bootstrap.sh`) installs all dependencies and configures the environment |
| C2.3 | Containerised development environment | Devcontainer, Docker Compose, or Nix flake provides a fully reproducible environment |
| C2.4 | Local environment mirrors production | Same runtime versions, same OS, same service topology; no "works on my machine" gaps |
| C2.5 | Environment setup is idempotent | Running setup multiple times does not break or duplicate configuration |

---

### C3 — Architecture Documentation

The degree to which an agent can understand the structure, boundaries, and responsibilities of the system.

| ID   | Criterion | Notes |
|------|-----------|-------|
| C3.1 | System context documented (C4 Level 1) | Diagram or prose describing the system, its users, and external dependencies |
| C3.2 | Container/service level documented (C4 Level 2) | Major services, their responsibilities, and how they communicate |
| C3.3 | Component level documented (C4 Level 3) | Internal structure of each major service; module/package responsibilities |
| C3.4 | Critical business flows documented | End-to-end descriptions of the most important user journeys through the system |
| C3.5 | Architecture documentation is stored in the repository | Docs live in-repo (or accessible via MCP server), not just in wikis or Confluence pages |
| C3.6 | Architecture documentation is kept current | Docs are updated as part of the development workflow (e.g., enforced in PR checklist) |

---

### C4 — Requirements and Specifications

The degree to which an agent can understand what the system is supposed to do and access the work backlog.

| ID   | Criterion | Notes |
|------|-----------|-------|
| C4.1 | Product vision and goals documented | High-level statement of purpose, target users, and success criteria |
| C4.2 | User stories or acceptance criteria accessible | Stories include enough context for an agent to understand intent, not just implementation |
| C4.3 | Requirements are linked to code | Stories/tickets reference the code or files they affect (or vice versa) |
| C4.4 | Requirements management tool accessible via MCP or API | Agent can query tickets, epics, or stories programmatically (e.g., Jira MCP, Linear MCP) |
| C4.5 | Stakeholders are reachable | A mechanism exists for an agent (or the human overseeing it) to ask clarifying questions |

---

### C5 — Testing and Feedback Loops

The degree to which an agent can verify that changes are correct and have not caused regressions.

| ID   | Criterion | Notes |
|------|-----------|-------|
| C5.1 | Project builds without errors | Compilation or parsing succeeds on a clean checkout |
| C5.2 | Unit tests are present | At least some unit tests cover business logic |
| C5.3 | Unit test coverage ≥ 50% | Line or branch coverage as reported by a coverage tool |
| C5.4 | Unit test coverage ≥ 80% | High coverage enables confident refactoring |
| C5.5 | Integration tests cover key service boundaries | Tests that span at least two components or a component and its datastore |
| C5.6 | End-to-end tests cover critical flows | Automated tests that drive the system from the outside (API, UI) through complete user journeys |
| C5.7 | UI tests with visual verification | Screenshot diffing or visual regression testing for projects with a frontend |
| C5.8 | Tests run in under 10 minutes | Fast feedback; agents do not have to wait long to know if a change is correct |
| C5.9 | Test suite is deterministic | Flaky tests are tracked and suppressed; failures are reliable signals |
| C5.10 | Performance or load tests exist | Agents can detect performance regressions, not just functional ones |

---

### C6 — Code Quality Tooling

The degree to which automated tools can give an agent immediate, actionable feedback on code quality.

| ID   | Criterion | Notes |
|------|-----------|-------|
| C6.1 | Linting is configured and automated | Linter runs on every change (pre-commit hook or CI) and reports issues clearly |
| C6.2 | Type checking is enforced | Static type analysis (TypeScript strict, mypy, etc.) runs and must pass |
| C6.3 | Code formatting is automated | Formatter (Prettier, Black, gofmt) runs automatically; diffs are not polluted with style changes |
| C6.4 | Static analysis / security scanning | SAST tool (Semgrep, Bandit, etc.) runs and flags security issues |
| C6.5 | Dependency vulnerability scanning | Automated check for known CVEs in dependencies (Dependabot, Snyk, etc.) |
| C6.6 | Pre-commit hooks configured | All quality checks run locally before a commit is created |

---

### C7 — Data and External Dependencies

The degree to which an agent can work with realistic data and test integrations with external systems.

| ID   | Criterion | Notes |
|------|-----------|-------|
| C7.1 | Test database or data store is reproducible | Seed scripts or migration-based setup creates a known database state on demand |
| C7.2 | Test fixtures cover representative scenarios | Data fixtures cover happy paths, edge cases, and error states |
| C7.3 | External APIs have sandbox/mock environments | Third-party services (payments, auth, email) provide test modes or can be mocked |
| C7.4 | Contract tests for external integrations | Consumer-driven contracts or recorded interactions verify integration correctness |
| C7.5 | Feature flags allow safe partial rollouts | New behaviour can be toggled without a deployment; agents can test in production-like conditions |

---

### C8 — Deployment and Operations

The degree to which an agent can deploy, monitor, and verify changes in production-like environments.

| ID   | Criterion | Notes |
|------|-----------|-------|
| C8.1 | Automated CI pipeline | Every push triggers build and test; results are visible in the repository |
| C8.2 | Automated deployment to staging | Merges to main/staging branch trigger an automatic deployment to a staging environment |
| C8.3 | Automated deployment to production | Production deployments are triggered by a pipeline, not manual steps |
| C8.4 | Rollback mechanism exists | A deployment can be reverted in under 15 minutes with a documented procedure |
| C8.5 | Structured application logs accessible | Logs are queryable (e.g., via MCP server connecting to a log aggregation platform) |
| C8.6 | Metrics and alerting configured | Key system metrics are tracked; anomalies trigger alerts that an agent can read |

---

### C9 — Tooling and IDE Compatibility

The degree to which the project's tooling stack is compatible with AI-assisted development workflows.

| ID   | Criterion | Notes |
|------|-----------|-------|
| C9.1 | AI coding CLI or IDE extension is supported | The project can be worked on with Claude Code, Cursor, Copilot, or equivalent |
| C9.2 | CLAUDE.md or equivalent agent instructions file | A file at the repository root gives agents project-specific instructions and conventions |
| C9.3 | MCP servers configured for key integrations | Agents can interact with project management, databases, or deployment tools via MCP |
| C9.4 | Version control history is clean and informative | Commit messages are descriptive; history is not a sequence of "fix" or "wip" entries |
| C9.5 | Branch and PR workflow is documented | Agents know how to create branches, open PRs, and follow the team's review process |

---

### C10 — Team and Process Readiness

The degree to which the team and its processes are prepared to work alongside AI agents.

| ID   | Criterion | Notes |
|------|-----------|-------|
| C10.1 | Team members have baseline AI tooling familiarity | At least one team member can set up and operate an AI coding agent |
| C10.2 | Code review process accommodates AI-generated code | Reviewers understand how to evaluate agent output; review criteria are documented |
| C10.3 | Security policy for AI-generated code exists | Policy covers secrets handling, licence compliance, and acceptable use |
| C10.4 | Escalation path for agent uncertainty | A process exists for an agent to surface ambiguity to a human rather than guessing |
| C10.5 | Agent activity is logged and auditable | Changes made by agents are distinguishable from human changes in the git history |

---

## Level–Criteria Mapping (Preliminary)

The following table gives a first-pass assignment of minimum criteria required for each level. Detailed fulfillment thresholds for each criterion are defined in a separate document.

| Level | Required Criteria |
|-------|-------------------|
| **0 → 1** (Foundation) | C1.1, C1.2, C2.1, C5.1, C5.2 |
| **1 → 2** (Guided Autonomy) | C1.3, C2.2, C3.1, C3.2, C4.1, C4.2, C5.3, C5.5, C6.1, C6.2, C9.1, C9.2, C10.1 |
| **2 → 3** (Supervised Autonomy) | C2.3, C3.3, C3.4, C3.5, C4.4, C5.4, C5.6, C5.7 (if UI), C5.8, C6.4, C7.1, C7.2, C7.3, C8.1, C8.2, C9.3, C10.2, C10.3 |

---

## Notes and Assumptions

- **Applicability**: Not all criteria apply to every project type. Criteria marked "if UI" or "if applicable" may be omitted for projects without a frontend, and their omission does not reduce the level.
- **Partial credit**: Most criteria have graduated fulfillment levels (e.g., C5.3 vs C5.4 for coverage). The fulfillment levels and their mapping to readiness levels will be defined in a subsequent revision.
- **Human in the loop**: Even at Level 3, humans remain in the loop. The model describes the degree of autonomy that is *possible*, not the degree that is *required* or *safe* in any given context.
- **Model evolution**: This is a living document. As the practice of agentic coding matures, the criteria and thresholds will be revised.
