# Agentize

Agentize is a framework for evaluating and improving the readiness and adoption of AI agents in software projects. It provides two complementary maturity models — one that measures structural project properties (Agent Readiness) and one that measures how deeply agents are embedded in development workflows (Agent Adoption) — along with a full suite of Claude Code skills to assess and raise both dimensions automatically.

Applying agentic coding to a project amplifies what is already there: a well-structured, well-tested, well-documented codebase benefits enormously; a chaotic one becomes harder to manage. Agentize lets teams assess their starting point, understand exactly what is blocking the next level, and implement improvements systematically.

---

## Agent Readiness Maturity Model

Readiness measures the structural, environmental, and documentary properties of a codebase that determine how effectively an AI agent can understand, navigate, modify, and verify the project. It has four levels spanning zero meaningful agent benefit through to full supervised autonomy.

| Level | Name | What it means |
|-------|------|---------------|
| 0 | Uninstrumented | No meaningful context or feedback for an agent. Applying agents produces little benefit and risks introducing hard-to-detect regressions. |
| 1 | Foundation | Enough structure for an agent to take small, targeted steps. A human must micromanage each step and verify every output. |
| 2 | Guided Autonomy | Humans guide at the story or feature level. Agents can plan implementations, write tests, and navigate the architecture. |
| 3 | Supervised Autonomy | Humans operate at a strategic level. Agents can autonomously implement most stories end-to-end with comprehensive feedback loops. |

Readiness is scored across **11 criteria** in 8 groups:

| ID | Criterion | Max level |
|----|-----------|-----------|
| C1.1 | Codebase Accessibility | 2 |
| C2.1 | Setup Automation | 3 |
| C3.1 | Architecture Depth | 3 |
| C4.1 | Requirements Access | 3 |
| C5.1 | Runnability | 2 |
| C5.2 | Unit Test Coverage | 3 |
| C5.3 | Integration and E2E Coverage | 3 |
| C6.1 | Static Analysis | 3 |
| C7.1 | Test Isolation | 2 |
| C8.1 | CI/CD Automation | 3 |
| C8.2 | Observability | 3 |

See [READINESS.md](READINESS.md) for full level definitions, criterion fulfillment tables, and the level-criteria mapping with rationale.

---

## Agent Adoption Maturity Model

Adoption measures how deeply AI agents are embedded in a team's development process — not just whether individual developers experiment with them, but whether agents are integrated into workflows, delivery pipelines, and continuous improvement practices. It has five levels spanning no agent use through to a self-sustaining autonomous system.

| Level | Name | What it means |
|-------|------|---------------|
| 0 | Unassisted | Agents play no meaningful role. Development is entirely human-driven. |
| 1 | Vibe Coding | Developers use agents as interactive assistants for bounded coding tasks, directing them step-by-step. |
| 2 | Agentic Engineering | Agents plan and implement complete features. Developers review outcomes rather than directing every step. |
| 3 | Software Factory | Agents continuously pull stories from the backlog and implement them with minimal per-story human involvement. |
| 4 | Sustainable Autonomy | Agents proactively address tech debt, security vulnerabilities, and dependency hygiene without human initiation. |

Adoption is scored across **8 criteria**:

| ID | Criterion | What it measures |
|----|-----------|-----------------|
| A1 | Agent Context Availability | Project-specific guidance available to agents (CLAUDE.md, MCP servers) |
| A2 | Agent-Authored Contributions | Proportion of codebase changes with significant agent involvement |
| A3 | Feedback Loop Closure | Degree to which agents verify their own work before presenting results |
| A4 | Task Scope | Granularity of work agents handle end-to-end |
| A5 | Workflow Integration | How embedded agents are in PRs, code review, CI, and deployment |
| A6 | Autonomous Operation | Whether agents are triggered by events/schedules or always started manually |
| A7 | Proactive Quality Management | Whether agents improve codebase health on their own initiative |
| A8 | Planning Integration | Whether agents participate in story generation and backlog grooming |

See [ADOPTION.md](ADOPTION.md) for full level definitions, criterion fulfillment tables, and the level-criteria mapping with rationale.

---

## How to Use This Framework

### Step 1: Run the assessment skills

Use the Claude Code assessment skills for detailed, evidence-based scoring with per-criterion scores and recommendations:

- `/assess-readiness` — full readiness assessment across all 11 criteria
- `/assess-adoption` — full adoption assessment across all 8 criteria

### Step 2: Raise your level

Use the level-raising skills to implement all improvements needed to reach the next level in one step:

- `/improve-readiness` — identifies blocking criteria and implements all required improvements
- `/improve-adoption` — identifies blocking criteria and implements all required improvements

### Step 3: Verify specific criteria

Use individual verify skills to check a single criterion in isolation:

- `/verify-c1-1`, `/verify-c2-1`, ... `/verify-c8-2` — verify individual readiness criteria
- `/verify-a1`, `/verify-a2`, ... `/verify-a8` — verify individual adoption criteria

### Step 4: Improve specific criteria

Use individual improve skills for targeted, one-criterion-at-a-time improvements:

- `/improve-c1-1`, `/improve-c2-1`, ... `/improve-c8-2` — improve a specific readiness criterion
- `/improve-a1`, `/improve-a2`, ... `/improve-a8` — improve a specific adoption criterion

---

## Skills Reference

### Assessment

| Skill | Description |
|-------|-------------|
| `assess-readiness` | Assess the Agent Readiness level of the current project across all 11 criteria (C1.1–C8.2) and produce a structured report with the achieved level, per-criterion scores, gaps, and recommendations. |
| `assess-adoption` | Assess the Agent Adoption level of the current project across all 8 criteria (A1–A8) and produce a structured report with the achieved level, per-criterion scores, gaps, and recommendations. |
| `verify-c1-1` | Verify readiness criterion C1.1 (Codebase Accessibility) in the current project. Reports fulfillment level 0–2. |
| `verify-c2-1` | Verify readiness criterion C2.1 (Setup Automation) in the current project. Reports fulfillment level 0–3. |
| `verify-c3-1` | Verify readiness criterion C3.1 (Architecture Depth) in the current project. Reports fulfillment level 0–3. |
| `verify-c4-1` | Verify readiness criterion C4.1 (Requirements Access) in the current project. Reports fulfillment level 0–3. |
| `verify-c5-1` | Verify readiness criterion C5.1 (Runnability) in the current project. Reports fulfillment level 0–2. |
| `verify-c5-2` | Verify readiness criterion C5.2 (Unit Test Coverage) in the current project. Reports fulfillment level 0–3. |
| `verify-c5-3` | Verify readiness criterion C5.3 (Integration and E2E Coverage) in the current project. Reports fulfillment level 0–3. |
| `verify-c6-1` | Verify readiness criterion C6.1 (Static Analysis) in the current project. Reports fulfillment level 0–3. |
| `verify-c7-1` | Verify readiness criterion C7.1 (Test Isolation) in the current project. Reports fulfillment level 0–2. |
| `verify-c8-1` | Verify readiness criterion C8.1 (CI/CD Automation) in the current project. Reports fulfillment level 0–3. |
| `verify-c8-2` | Verify readiness criterion C8.2 (Observability) in the current project. Reports fulfillment level 0–3. |
| `verify-a1` | Verify adoption criterion A1 (Agent Context Availability) in the current project. Reports fulfillment level 0–3. |
| `verify-a2` | Verify adoption criterion A2 (Agent-Authored Contributions) in the current project. Reports fulfillment level 0–3. |
| `verify-a3` | Verify adoption criterion A3 (Feedback Loop Closure) in the current project. Reports fulfillment level 0–3. |
| `verify-a4` | Verify adoption criterion A4 (Task Scope) in the current project. Reports fulfillment level 0–3. |
| `verify-a5` | Verify adoption criterion A5 (Workflow Integration) in the current project. Reports fulfillment level 0–3. |
| `verify-a6` | Verify adoption criterion A6 (Autonomous Operation) in the current project. Reports fulfillment level 0–3. |
| `verify-a7` | Verify adoption criterion A7 (Proactive Quality Management) in the current project. Reports fulfillment level 0–3. |
| `verify-a8` | Verify adoption criterion A8 (Planning Integration) in the current project. Reports fulfillment level 0–3. |

### Improvement (Readiness)

| Skill | Description |
|-------|-------------|
| `improve-readiness` | Assess the current readiness level of the project and implement all improvements needed to raise it to the next level. Runs the relevant improve-c* logic for each blocking criterion inline. |
| `improve-c1-1` | Improve readiness criterion C1.1 (Codebase Accessibility) in the current project by creating or enhancing the agent context file (CLAUDE.md). Raises the fulfillment level by one step. |
| `improve-c2-1` | Improve readiness criterion C2.1 (Setup Automation) in the current project by adding or upgrading setup automation. Raises the fulfillment level by one step. |
| `improve-c3-1` | Improve readiness criterion C3.1 (Architecture Depth) in the current project by generating architecture documentation. Raises the fulfillment level by one step. |
| `improve-c4-1` | Improve readiness criterion C4.1 (Requirements Access) in the current project by generating vision and user story documentation. Raises the fulfillment level by one step. |
| `improve-c5-1` | Improve readiness criterion C5.1 (Runnability) in the current project by adding run configuration. Raises the fulfillment level by one step. |
| `improve-c5-2` | Improve readiness criterion C5.2 (Unit Test Coverage) in the current project by generating unit tests for untested code. Raises the fulfillment level by one step. |
| `improve-c5-3` | Improve readiness criterion C5.3 (Integration and E2E Coverage) in the current project by adding integration or E2E test infrastructure. Raises the fulfillment level by one step. |
| `improve-c6-1` | Improve readiness criterion C6.1 (Static Analysis) in the current project by adding linting, type checking, or security scanning. Raises the fulfillment level by one step. |
| `improve-c7-1` | Improve readiness criterion C7.1 (Test Isolation) in the current project by adding mocks, fixtures, or seed scripts. Raises the fulfillment level by one step. |
| `improve-c8-1` | Improve readiness criterion C8.1 (CI/CD Automation) in the current project by creating or extending GitHub Actions workflows. Raises the fulfillment level by one step. |
| `improve-c8-2` | Improve readiness criterion C8.2 (Observability) in the current project by adding structured logging and monitoring configuration. Raises the fulfillment level by one step. |

### Improvement (Adoption)

| Skill | Description |
|-------|-------------|
| `improve-adoption` | Assess the current Agent Adoption level of the project, identify which criteria block the next level, and implement improvements for each blocking criterion to raise the project to the next adoption level. Embeds all improve-a* logic inline. |
| `improve-a1` | Improve adoption criterion A1 (Agent Context Availability) in the current project by creating or enriching agent context files and MCP configuration. Raises the fulfillment level by one step. |
| `improve-a2` | Improve adoption criterion A2 (Agent-Authored Contributions) by setting up the tooling and guidance that enables and tracks agent contributions. Raises the fulfillment level by one step. |
| `improve-a3` | Improve adoption criterion A3 (Feedback Loop Closure) by adding verification guidance to agent context files and configuring CI/monitoring MCP access. Raises the fulfillment level by one step. |
| `improve-a4` | Improve adoption criterion A4 (Task Scope) by creating skills and guidance that enable agents to handle progressively larger tasks. Raises the fulfillment level by one step. |
| `improve-a5` | Improve adoption criterion A5 (Workflow Integration) by embedding agents into pull request creation, CI observation, and review processes. Raises the fulfillment level by one step. |
| `improve-a6` | Improve adoption criterion A6 (Autonomous Operation) by creating event-triggered and scheduled GitHub Actions workflows that invoke agents without human initiation. Raises the fulfillment level by one step. |
| `improve-a7` | Improve adoption criterion A7 (Proactive Quality Management) by configuring automated dependency updates, security scanning, and agent-driven tech debt PRs. Raises the fulfillment level by one step. |
| `improve-a8` | Improve adoption criterion A8 (Planning Integration) by creating story-generation skills and MCP connections to project management tools so agents participate in planning workflows. Raises the fulfillment level by one step. |

### Workflow

| Skill | Description |
|-------|-------------|
| `do-next-task` | Pick the top task from TODO.md, implement it fully, commit and push to git, then mark it complete. Use when you want to work on the next item in the project task list. |

---

## Getting Started

1. **Clone the repository:**

   ```bash
   git clone https://github.com/jaksa76/agentize.git
   cd agentize
   ```

2. **Try a skill in Claude Code.** Open any software project in Claude Code and run:

   ```
   /assess-readiness
   ```

   Claude Code will score the project across all 11 readiness criteria and tell you exactly what is blocking the next level.

---

## File Structure

| File / Directory | Purpose |
|-----------------|---------|
| `READINESS.md` | Full specification of the Agent Readiness Maturity Model: levels 0–3, all 11 criteria with fulfillment tables, and the level-criteria mapping with rationale. |
| `ADOPTION.md` | Full specification of the Agent Adoption Maturity Model: levels 0–4, all 8 criteria with fulfillment tables, and the level-criteria mapping with rationale. |
| `VISION.md` | Original project vision document describing the goals and scope of both models. |
| `.claude/skills/` | Claude Code skills for assessing, verifying, and improving both readiness and adoption. Each skill lives in its own subdirectory with a `SKILL.md` file. |
