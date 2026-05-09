# Agent Adoption Maturity Model

## Overview

This model evaluates the degree to which a software team has integrated AI agents into its development process. "Adoption" measures how agents are used — not just whether individual developers experiment with them, but whether agents are embedded into the team's workflows, delivery pipeline, and continuous improvement practices.

Readiness (structural project properties) and adoption (how agents are actually used) are complementary: a highly-ready project enables higher adoption, but adoption can still lag even when the technical foundations are strong. This model allows teams to assess where they are and identify concrete next steps.

---

## Levels

### Level 0 — Unassisted

Agents play no meaningful role in the team's development process. Development is entirely human-driven. Individual developers may occasionally ask a chatbot a question, but there is no systematic or habitual agent use.

**Typical state:**
- No developer uses an AI coding agent as part of their regular workflow
- All code is written, reviewed, tested, and deployed by humans
- No agent tooling is installed or configured in the repository

---

### Level 1 — Vibe Coding

Developers use agents as interactive assistants for individual coding tasks. Agents accelerate human work (autocomplete, code generation, explanation, debugging) but are directed step-by-step. The human remains the author; the agent is a smart tool.

**Typical state:**
- Most developers use an AI coding assistant regularly (completions, chat, inline edits)
- Agents are used for bounded tasks: writing a function, explaining an error, generating a test for a specific case
- Humans review every line the agent produces before accepting it
- No agent autonomously runs tools, executes tests, or makes multi-file changes

---

### Level 2 — Agentic Engineering

Agents can plan and implement complete features or user stories with the developer providing high-level direction and reviewing outcomes rather than directing every step. Agents run their own feedback loops (tests, linting, compilation) and iterate before presenting results.

**Typical state:**
- Developers assign whole stories or tasks to agents and review the resulting diff
- Agents autonomously write, run, and fix tests as part of implementation
- Agents operate across multiple files and exercise independent judgment about structure
- Humans review completed work rather than each individual step
- Agent use is the default, not the exception, for most implementation work

---

### Level 3 — Software Factory

Agents continuously pull stories from the backlog and implement them with minimal per-story human involvement. The team's role shifts from writing code to defining requirements, reviewing agent output, and handling exceptions. Multiple agents may work in parallel.

**Typical state:**
- A continuous pipeline of agent workers pulls and implements backlog items
- Agents create pull requests; humans review and merge
- Agent throughput is a primary delivery metric alongside human throughput
- Agents participate in or trigger code review, CI, and deployment workflows
- The team actively manages agent capacity, queue depth, and output quality

---

### Level 4 — Sustainable Autonomy

The team has automated not only feature delivery but also the long-term health of the codebase. Agents proactively address tech debt, security vulnerabilities, and dependency hygiene without human initiation. Production issues trigger automated analysis and remediation attempts.

**Typical state:**
- Agents regularly open PRs to reduce tech debt, update dependencies, and resolve security findings — unprompted
- Automated security reviews run on every change and flag or fix issues before merge
- Production incidents trigger agent-driven diagnosis and, where safe, automated remediation
- Agents participate in requirements generation and story decomposition, reducing manual planning overhead

---

## Criteria

Each criterion describes a behavioral dimension of adoption. Evidence for each may come from multiple artifact types — AGENTS.md, skills, MCP server configurations, git history, CI/CD configs — rather than any single source. Fulfillment levels for each criterion are defined separately.

---

### A1 — Agent Context Availability

The degree to which agents are given sufficient project-specific context to act effectively: understanding the codebase purpose, conventions, architecture, and how to navigate the project.

**Evidence:** CLAUDE.md or AGENTS.md with project-specific guidance; architecture documentation written or structured for agent consumption; MCP servers exposing project knowledge.

| Level | Description |
|-------|-------------|
| 0 | No agent context files; agents must infer everything from raw code |
| 1 | Basic README or project description exists; agents have a starting point but no conventions or navigation guidance |
| 2 | CLAUDE.md or AGENTS.md provides project-specific guidance: conventions, architecture overview, key commands |
| 3 | Comprehensive agent context including architecture docs structured for agent consumption AND MCP servers exposing project knowledge (requirements, diagrams, runbooks) |

---

### A2 — Agent-Authored Contributions

The degree to which agents meaningfully contribute to the codebase, from occasional co-authored edits through to agents autonomously creating pull requests.

**Evidence:** Co-authored commits in git history; PR descriptions indicating agent implementation; proportion of recent changes with agent involvement.

| Level | Description |
|-------|-------------|
| 0 | No agent-authored code in git history; all commits are purely human-written |
| 1 | Occasional co-authored commits; agents contributed to fewer than 25% of recent changes |
| 2 | Regular agent contributions; agents co-authored 25–75% of recent changes; agent use is habitual for many developers |
| 3 | Agents autonomously create pull requests; more than 75% of implementation work has significant agent involvement |

---

### A3 — Feedback Loop Closure

The degree to which agents can verify their own work before presenting results to a human — running tests, checking compilation, iterating on failures — rather than relying on the human to close the loop.

**Evidence:** AGENTS.md documenting test and build commands for agent use; MCP server access to test runners or build output; skills that include verification steps as part of their workflow.

| Level | Description |
|-------|-------------|
| 0 | Agents produce output and hand it directly to the human; no self-verification |
| 1 | Agents run basic checks (compilation, syntax) but do not iterate on failures before presenting results |
| 2 | Agents run the full test suite and linter, iterate on failures, and present only passing results to the human |
| 3 | Agents have access to CI pipeline results, production monitoring, and MCP-connected tool outputs; verification is fully automated and includes post-deployment checks |

---

### A4 — Task Scope

The granularity of work that agents handle end-to-end: from bounded edits (a function, a fix) through to complete story implementation spanning multiple files, services, and test suites.

**Evidence:** Skill definitions describing the scope of tasks; AGENTS.md describing expected task granularity; size and complexity of agent-authored PRs in git history.

| Level | Description |
|-------|-------------|
| 0 | Agents only answer questions or explain code; they do not make changes |
| 1 | Agents handle bounded edits: a single function, a bug fix, a single-file change |
| 2 | Agents implement complete features spanning multiple files, writing and running tests as part of the implementation |
| 3 | Agents implement entire user stories end-to-end, including cross-service changes, test suites, documentation, and migration scripts |

---

### A5 — Workflow Integration

The degree to which agents are embedded in team handoffs and delivery rituals rather than used in isolation: creating pull requests, participating in code review, monitoring CI results, and triggering or observing deployments.

**Evidence:** Automated PR creation patterns; CI pipeline configurations invoking agent tasks; review automation configuration; agent-generated PR descriptions or review comments.

| Level | Description |
|-------|-------------|
| 0 | Agents are used in isolation; all handoffs (PRs, reviews, CI, deployments) are managed by humans |
| 1 | Agents assist with individual tasks but humans handle all handoffs; agent output is manually incorporated |
| 2 | Agents create pull requests with generated descriptions; agents observe CI results as part of their workflow |
| 3 | Agents are fully embedded: create PRs, post review comments, monitor CI, trigger and observe deployments |

---

### A6 — Autonomous Operation

The degree to which agents operate without human initiation — triggered by events (a push, a PR opened, a failing monitor) or running on a schedule — rather than always requiring a developer to start them.

**Evidence:** Scheduled CI/CD workflows that invoke agents; event-triggered agent jobs; cron-based agent pipelines pulling from a backlog.

| Level | Description |
|-------|-------------|
| 0 | Agents are always manually started by a developer; no automated triggering |
| 1 | Agents are occasionally triggered by events (e.g., on PR creation for a specific task) but are mostly started manually |
| 2 | Agents are systematically event-triggered for common workflows (push hooks, PR events, failing monitors) |
| 3 | A continuous agent pipeline pulls from the backlog and implements stories on a schedule, with no per-story human initiation |

---

### A7 — Proactive Quality Management

The degree to which agents improve codebase health on their own initiative: opening PRs for tech debt, updating dependencies, remediating security vulnerabilities, and enforcing standards — without being asked.

**Evidence:** Scheduled or bot-authored PRs for dependency updates, security fixes, or refactoring; automated security review jobs that run on every change.

| Level | Description |
|-------|-------------|
| 0 | No proactive quality management by agents; quality work is entirely human-initiated |
| 1 | Agents run quality checks (security scans, dependency audits) when explicitly asked by a developer |
| 2 | Agents automatically flag or report tech debt, security issues, and dependency updates, but do not open PRs to fix them |
| 3 | Agents proactively open PRs for tech debt reduction, dependency updates, security remediations, and standards enforcement without human initiation |

---

### A8 — Planning Integration

The degree to which agents participate upstream of coding: generating or refining user stories from high-level goals, decomposing epics into tasks, and contributing to backlog grooming.

**Evidence:** Skills for story generation or decomposition; MCP server connections to backlog or project management tools; AGENTS.md describing agent involvement in planning workflows.

| Level | Description |
|-------|-------------|
| 0 | Agents play no role in planning or requirements; all planning is done by humans |
| 1 | Agents assist with planning when explicitly prompted (e.g., help break down a story on request) |
| 2 | Agents participate in story generation or decomposition as a configured step in the planning workflow |
| 3 | Agents automatically generate, refine, and decompose stories from high-level goals and participate in backlog grooming without human initiation |

---

## Notes and Assumptions

- **Independence from readiness**: A team can adopt agents aggressively on a low-readiness project, but the results will be unpredictable. High adoption on a high-readiness project is the target state.
- **Evidence over artifacts**: Criteria are defined as behavioral dimensions. The same evidence (e.g. an AGENTS.md entry about running tests) may support multiple criteria. When assessing, look for the behavior, not just the presence of a file.
- **Team size**: Criteria like A5 (workflow integration) and A6 (autonomous operation) may look different in a solo project versus a team of twenty. Interpretation should be adjusted accordingly.
- **Model evolution**: This is a living document. As the practice of agentic development matures, the levels and criteria will be revised.
