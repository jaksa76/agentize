# Agentize

A framework for evaluating and improving AI agent readiness and adoption in software projects. Two complementary maturity models assess structural project properties (Agent Readiness) and how deeply agents are embedded in development workflows (Agent Adoption), with Claude Code skills to assess and raise both dimensions automatically.

Agentic coding amplifies what is already there — Agentize lets teams assess their starting point, understand exactly what is blocking the next level, and implement improvements systematically.

---

## Agent Readiness Maturity Model

Measures structural, environmental, and documentary properties that determine how effectively an AI agent can understand, navigate, modify, and verify the project.

| Level | Name | What it means |
|-------|------|---------------|
| 0 | Uninstrumented | No meaningful context or feedback for an agent. |
| 1 | Foundation | Enough structure for small, targeted steps. Human must verify every output. |
| 2 | Guided Autonomy | Humans guide at the feature level. Agents can plan, write tests, and navigate architecture. |
| 3 | Supervised Autonomy | Humans operate strategically. Agents implement most stories end-to-end autonomously. |

Scored across **11 criteria**:

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

See [READINESS.md](READINESS.md) for full level definitions and criterion fulfillment tables.

---

## Agent Adoption Maturity Model

Measures how deeply AI agents are embedded in a team's development process.

| Level | Name | What it means |
|-------|------|---------------|
| 0 | Unassisted | Agents play no meaningful role. |
| 1 | Vibe Coding | Agents assist with bounded coding tasks, directed step-by-step. |
| 2 | Agentic Engineering | Agents plan and implement complete features. Developers review outcomes. |
| 3 | Software Factory | Agents continuously pull stories from the backlog with minimal per-story human involvement. |
| 4 | Sustainable Autonomy | Agents proactively address tech debt, security, and dependencies without human initiation. |

Scored across **8 criteria**:

| ID | Criterion | What it measures |
|----|-----------|-----------------|
| A1 | Agent Context Availability | Project-specific guidance available to agents (CLAUDE.md, MCP servers) |
| A2 | Agent-Authored Contributions | Proportion of changes with significant agent involvement |
| A3 | Feedback Loop Closure | Degree to which agents verify their own work |
| A4 | Task Scope | Granularity of work agents handle end-to-end |
| A5 | Workflow Integration | How embedded agents are in PRs, code review, CI, and deployment |
| A6 | Autonomous Operation | Whether agents are triggered by events/schedules or always started manually |
| A7 | Proactive Quality Management | Whether agents improve codebase health on their own initiative |
| A8 | Planning Integration | Whether agents participate in story generation and backlog grooming |

See [ADOPTION.md](ADOPTION.md) for full level definitions and criterion fulfillment tables.

---

## How to Use

**Assess** your current level:
- `/assess-readiness` — score all 11 readiness criteria with gaps and recommendations
- `/assess-adoption` — score all 8 adoption criteria with gaps and recommendations

**Raise your level** (implements all blocking improvements in one step):
- `/improve-readiness`
- `/improve-adoption`

**Verify or improve a single criterion:**
- `/verify-c1-1` … `/verify-c8-2`, `/verify-a1` … `/verify-a8`
- `/improve-c1-1` … `/improve-c8-2`, `/improve-a1` … `/improve-a8`

---

## Installation

Clone the repository and copy the skills to your Claude Code skills directory.

**Personal install** (skills available in all your projects):

```bash
git clone https://github.com/jaksa76/agentize.git
cp -r agentize/.claude/skills/* ~/.claude/skills/
```

**Project install** (skills available only in one project):

```bash
cp -r agentize/.claude/skills/* /your/project/.claude/skills/
```

Once installed, open any project in Claude Code and run `/assess-readiness` or `/assess-adoption`.

---

## File Structure

| File / Directory | Purpose |
|-----------------|---------|
| `READINESS.md` | Full Agent Readiness Maturity Model specification. |
| `ADOPTION.md` | Full Agent Adoption Maturity Model specification. |
| `VISION.md` | Original project vision document. |
| `.claude/skills/` | Claude Code skills for assessing and improving readiness and adoption. |
