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

The following criteria are used to assess adoption level. Fulfillment levels for each criterion will be defined separately.

---

### A1 — Developer Agent Adoption Rate

The fraction of the development team that actively uses AI agents as a regular part of their daily workflow (not occasional experimentation).

---

### A2 — Implementation Autonomy

The granularity at which agents operate: from line-level completions and edits, through function- and class-level generation, to full story or feature implementation across multiple files with self-directed feedback loops.

---

### A3 — Test Authoring and Maintenance

The degree to which agents write, update, and maintain automated tests as an integral part of development — not just generating tests on request, but doing so automatically as part of implementing any change.

---

### A4 — Code Review Integration

The degree to which agents participate in pull request review: flagging issues, suggesting improvements, enforcing conventions, and providing a quality gate before human reviewers engage.

---

### A5 — Delivery Pipeline Integration

The degree to which agents are embedded in the team's delivery workflow: creating pull requests, monitoring CI results, triggering deployments, and verifying production outcomes as part of the standard flow — not as ad-hoc actions.

---

### A6 — Continuous Quality Management

The degree to which agents proactively and autonomously address codebase health: tech debt reduction, dependency updates, security vulnerability remediation, and code standard enforcement — initiated by agents rather than humans.

---

### A7 — Planning and Discovery Automation

The degree to which agents participate upstream of implementation: generating or refining user stories from high-level goals, decomposing epics into tasks, and contributing to backlog grooming — reducing the manual overhead of the planning process.

---

## Notes and Assumptions

- **Independence from readiness**: A team can adopt agents aggressively on a low-readiness project, but the results will be unpredictable. High adoption on a high-readiness project is the target state.
- **Team size**: Criteria like A1 (adoption rate) and A5 (pipeline integration) may look different in a solo project versus a team of twenty. Interpretation should be adjusted accordingly.
- **Model evolution**: This is a living document. As the practice of agentic development matures, the levels and criteria will be revised.
