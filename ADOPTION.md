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
- Developers regularly use an AI coding assistant (completions, chat, inline edits); agent use may not yet be universal across the team
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
- Agent use is habitual across the team and covers a substantial portion of implementation work

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

**Evidence:** Co-authored commits in git history; PR descriptions indicating agent implementation; proportion of recent changes with agent involvement. "Recent" is defined as the last 90 days or last 50 commits, whichever covers more changes.

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

## Level–Criteria Mapping

Minimum fulfillment levels required to attain each adoption level. A project must meet **all** minimum thresholds for a given level (and all lower levels) to be assigned that level. A dash (—) means the criterion is not required at that level.

| Criterion | Level 0 | Level 1 | Level 2 | Level 3 | Level 4 |
|-----------|---------|---------|---------|---------|---------|
| A1 Agent Context Availability | — | 1 | 2 | 3 | 3 |
| A2 Agent-Authored Contributions | — | 1 | 2 | 3 | 3 |
| A3 Feedback Loop Closure | — | — | 2 | 2 | 3 |
| A4 Task Scope | — | 1 | 2 | 3 | 3 |
| A5 Workflow Integration | — | — | 1 | 3 | 3 |
| A6 Autonomous Operation | — | — | — | 3 | 3 |
| A7 Proactive Quality Management | — | — | — | — | 3 |
| A8 Planning Integration | — | — | — | — | 2 |

### Rationale

**Level 0** has no requirements. Any project not meeting Level 1 thresholds falls here by default.

**Level 1 — Vibe Coding** requires the minimum behavioral signals that distinguish habitual agent use from occasional chatbot queries:

- **A1 ≥ 1**: A basic README or project description is the minimum for meaningful agent assistance. Without any project context, agent suggestions are purely generic — indistinguishable from a general-purpose chatbot rather than a project-integrated tool.
- **A2 ≥ 1**: Agent-authored contributions in git history (even occasional, fewer than 25% of changes) are the core behavioral signal of vibe coding. Explanation and Q&A alone, with no agent-written code merged, does not constitute Level 1.
- **A4 ≥ 1**: Agents must be making bounded code changes (a function, a bug fix, a single-file edit). Agents that only answer questions and never touch the codebase do not qualify.

A3, A5, A6, A7, and A8 are not required at Level 1 because developers direct agents step-by-step, close all feedback loops manually, and handle all workflow handoffs themselves.

**Level 2 — Agentic Engineering** requires enough context, contribution depth, and self-verification for agents to own complete feature implementation:

- **A1 ≥ 2**: CLAUDE.md or AGENTS.md with project-specific guidance is essential for agents to plan multi-file implementations without human narration. Conventions, architecture overview, and key commands let the agent operate autonomously within the project context. A bare README (A1 = 1) does not provide enough for independent judgment.
- **A2 ≥ 2**: Regular agent contributions (25–75% of recent changes) reflect that agent use has become the default for most implementation work, not a sporadic experiment.
- **A3 ≥ 2**: The ability to run the full test suite, iterate on failures, and present only passing results is the defining behavioral difference between Level 1 and Level 2. At Level 1, the human closes the feedback loop; at Level 2, the agent does. Without self-verification, "assigning a story" is just a longer prompt.
- **A4 ≥ 2**: Complete feature implementation spanning multiple files is the minimum task scope for Agentic Engineering. Bounded single-file edits (A4 = 1) are Level 1 behavior regardless of how often they occur.
- **A5 ≥ 1**: Agents assist with the full task scope even if humans still handle handoffs. This minimum ensures agents are integrated into the development workflow — not just used in isolation — without requiring autonomous PR creation.

A6, A7, and A8 are not required at Level 2 because agents are still manually initiated per task, proactive quality work is not expected, and planning integration is not yet part of the workflow.

**Level 3 — Software Factory** requires the infrastructure for continuous, parallel, low-touch agent delivery:

- **A1 ≥ 3**: Comprehensive agent context — including architecture docs structured for agent consumption AND MCP servers exposing requirements and runbooks — is necessary for agents to pull stories from the backlog and implement them without per-story human briefing. A static CLAUDE.md (A1 = 2) is insufficient when agents must independently understand requirements and navigate the full system.
- **A2 ≥ 3**: Autonomous PR creation and more than 75% agent involvement in implementation reflects that the team operates as a factory, not as individual developers who sometimes delegate. Agent throughput must be a primary delivery metric alongside human throughput.
- **A3 ≥ 2**: Agents must present only passing results to human reviewers. At factory scale, passing unverified work to human reviewers creates unacceptable review burden. (Full CI and production verification — A3 = 3 — is deferred to Level 4 because post-deployment verification is a distinct capability from pre-review verification.)
- **A4 ≥ 3**: Full user story implementation end-to-end — including cross-service changes, test suites, documentation, and migration scripts — is required. Partial feature implementation (A4 = 2) still requires significant human completion work and is Level 2 behavior.
- **A5 ≥ 3**: Full workflow embedding — creating PRs, posting review comments, monitoring CI, triggering and observing deployments — is what makes the factory pattern work at scale without per-task human coordination. Partial workflow integration (A5 = 1 or 2) still requires humans to close too many handoff loops.
- **A6 ≥ 3**: A continuous pipeline pulling from the backlog on a schedule is the defining characteristic of Level 3. Without this, each story still requires a human to initiate it — which is Level 2, regardless of how capable the agent is once started.

A7 and A8 are not required at Level 3 because proactive quality management and planning integration represent a separate dimension of autonomy (long-term codebase health and upstream participation) that is not part of the core delivery factory pattern.

**Level 4 — Sustainable Autonomy** adds the proactive and planning dimensions that make the system self-sustaining over time:

- **A1 ≥ 3**: Full context remains necessary (same as Level 3); proactive quality agents must understand the system deeply to identify and remediate tech debt and security issues without being prompted.
- **A2 ≥ 3**: Same as Level 3; agents remain the primary implementers, now also for proactive quality work.
- **A3 ≥ 3**: Level 4 agents verify post-deployment behavior and respond to production incidents. This requires access to CI pipeline results, production monitoring, and MCP-connected tool outputs — not just the local test suite. Without this, automated remediation of production issues is impossible.
- **A4 ≥ 3**: Same as Level 3; story-level implementation scope is required for proactive quality PRs and autonomous planning contributions.
- **A5 ≥ 3**: Same as Level 3; full workflow embedding is required for proactive PRs to flow through review, CI, and deployment without human coordination.
- **A6 ≥ 3**: Same as Level 3; continuous autonomous operation is the foundation on which proactive and planning behaviors run.
- **A7 ≥ 3**: Proactive PR creation for tech debt reduction, dependency updates, and security remediations — without human initiation — is the defining characteristic of Level 4. Without this, the team must still manually schedule all quality work, and the system degrades over time regardless of delivery throughput.
- **A8 ≥ 2**: Agents participate in story generation or decomposition as a configured step in the planning workflow. Level 4's typical state includes requirements generation and story decomposition; full autonomous planning (A8 = 3) is a stretch goal, but structured participation in planning (A8 = 2) is required to reduce the manual overhead of feeding the factory.

---

## Notes and Assumptions

- **Independence from readiness**: A team can adopt agents aggressively on a low-readiness project, but the results will be unpredictable. High adoption on a high-readiness project is the target state. As a rough guide: Adoption Level 1 is viable from Readiness Level 1; Adoption Level 2 benefits strongly from Readiness Level 2; Adoption Levels 3 and 4 effectively require Readiness Level 3.
- **Evidence over artifacts**: Criteria are defined as behavioral dimensions. The same evidence (e.g. an AGENTS.md entry about running tests) may support multiple criteria. When assessing, look for the behavior, not just the presence of a file.
- **"Recent changes" baseline**: A2 percentage thresholds apply to the last 90 days or last 50 commits, whichever covers more changes. For very young projects with fewer than 50 commits total, use all available history.
- **Team size**: Criteria like A5 (workflow integration) and A6 (autonomous operation) may look different in a solo project versus a team of twenty. Interpretation should be adjusted accordingly.
- **Output quality**: This model measures what agents do and how autonomously they operate, not the quality of individual agent outputs. Quality is implicitly captured through A3 (self-verification) and A5 (CI and review integration), but teams should track agent error rates and PR rejection rates separately.
- **Model evolution**: This is a living document. As the practice of agentic development matures, the levels and criteria will be revised.


---

*Copyright (c) 2026 Codomain D.O.O. All rights reserved. Licensed under [CC BY-NC 4.0](LICENSE.md). Licensed clients may use and modify this material for internal business purposes.*
