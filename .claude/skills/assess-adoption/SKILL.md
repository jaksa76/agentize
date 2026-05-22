---
name: assess-adoption
description: Assess the Agent Adoption level of the current project across all 8 criteria (A1–A8) and produce a structured report with the achieved level, per-criterion scores, gaps, and recommendations.
allowed-tools: Bash Read
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Agent Adoption Assessment

This skill collects evidence for all 8 adoption criteria and instructs you to
score each one, determine the overall adoption level, and produce a full report.

---

## Evidence to Gather

Before scoring, examine the project for evidence relevant to each criterion. Use your knowledge of the project structure and tech stack to look in the right places.

### A1 — Agent Context Availability
Check for agent context files (`CLAUDE.md`, `AGENTS.md`, or equivalent) and read their content — assess depth and coverage of conventions, commands, and architecture. Check the MCP server configuration for any servers exposing project knowledge. Look for architecture documentation or a `docs/` directory.

### A2 — Agent-Authored Contributions
Look at recent git history (last 90 days or last 50 commits) and count commits with agent co-authorship markers (Co-Authored-By, Claude/Copilot references, 🤖 emoji, "Generated with"). Calculate the ratio against total recent commits. Check for workflows or merge patterns indicating autonomous PR creation.

### A3 — Feedback Loop Closure
Read `CLAUDE.md` or `AGENTS.md` for verification or quality-check guidance. Check skill files in `.claude/skills/` for verification steps. Check the MCP server configuration for CI pipeline or production monitoring access. Check `.claude/settings.json` for hooks.

### A4 — Task Scope
Look at agent-co-authored commits and assess how many files each changed. Read skill definitions to understand the scope they target. Read `CLAUDE.md`/`AGENTS.md` for task granularity guidance. Look at any backlog or task files to assess item granularity.

### A5 — Workflow Integration
Check `CLAUDE.md`, `AGENTS.md`, and skill files for PR creation instructions. Look at CI workflow files for automated PR creation or review automation. Check the MCP server configuration for CI/pipeline access. Look for evidence of agent-triggered deployments.

### A6 — Autonomous Operation
Look at CI workflow files for scheduled triggers and event triggers that invoke agents. Check for backlog-pulling workflow patterns. Check `.claude/settings.json` for hooks that trigger agents automatically.

### A7 — Proactive Quality Management
Check for Dependabot or Renovate configuration. Look at CI workflow files for scheduled quality or security workflows. Check git history for bot-authored commits. Look in `.claude/skills/` for quality-focused skills.

### A8 — Planning Integration
Check `.claude/skills/` for planning-related skills. Check the MCP server configuration for PM tool connections (Jira, Linear, GitHub Issues, etc.). Read `CLAUDE.md`/`AGENTS.md` for planning guidance. Look for backlog or story files and assess granularity.

---

## Scoring Instructions

Using the evidence collected above, assign a fulfillment level to each criterion.

### Criterion scoring guides

**A1 Agent Context Availability (0–3)**
- 0: No CLAUDE.md, AGENTS.md, or equivalent; no meaningful README
- 1: Basic README exists; no conventions, commands, or navigation guidance
- 2: CLAUDE.md or AGENTS.md with conventions, key commands, architecture overview
- 3: Level 2 PLUS architecture docs structured for agent consumption AND MCP servers exposing project knowledge (requirements, diagrams, runbooks)

**A2 Agent-Authored Contributions (0–3)**
Divide agent-co-authored commit count by total recent commits (last 90 days or 50 commits):
- 0: 0% — no co-authorship markers in git history
- 1: < 25% of recent commits have agent co-authorship markers
- 2: 25–75% of recent commits have agent co-authorship markers
- 3: > 75%, or evidence of autonomous PR creation (bot-authored PRs, agent-creating workflows)

**A3 Feedback Loop Closure (0–3)**
- 0: No verification guidance in agent context files or skills
- 1: Agents run basic checks (build/compile) but not the full test suite
- 2: CLAUDE.md/AGENTS.md or skills explicitly instruct agents to run the full test suite, iterate on failures, and present only passing results
- 3: Level 2 PLUS CI pipeline access via MCP AND production monitoring access via MCP enabling post-deployment verification

**A4 Task Scope (0–3)**
Assess the largest scope routinely handled end-to-end:
- 0: No agent-authored changes; agents only answer questions
- 1: Agent commits are consistently 1–2 files; bounded single-function or bug-fix tasks
- 2: Agent commits regularly span 3+ files including test files; skills describe feature-level scope
- 3: Agent commits span services/packages; include migrations, docs, comprehensive tests; TODO items are story-level

**A5 Workflow Integration (0–3)**
- 0: Agents used in isolation; no PR creation in skills or workflows
- 1: Agents assist with tasks; humans manually create PRs and handle all handoffs
- 2: Skills or CLAUDE.md instruct agents to create PRs (`gh pr create`); CI MCP access for observing pipeline results
- 3: All of: agents create PRs, post review comments or trigger review workflows, monitor CI, trigger or observe deployments

**A6 Autonomous Operation (0–3)**
- 0: Agents always manually started; no automated triggering
- 1: At least one event-triggered workflow invokes an agent; most work is still manual
- 2: Agents systematically event-triggered for common events (push, PR, failing monitors)
- 3: Continuous pipeline pulls from backlog on a schedule; no per-story human initiation

**A7 Proactive Quality Management (0–3)**
- 0: No automated quality workflows; no Dependabot/Renovate; no bot-authored quality commits
- 1: Quality-check skills exist that developers explicitly invoke; no automated triggering
- 2: Scheduled workflows flag/report quality issues without opening PRs to fix them
- 3: Agents proactively open PRs — Dependabot/Renovate auto-PR, scheduled security fix workflows, bot-authored commits in git history

**A8 Planning Integration (0–3)**
- 0: No planning-related skills, no PM MCP servers, no planning guidance in agent context
- 1: Agents assist with planning ad-hoc when prompted; no configured planning step
- 2: Configured planning step exists — dedicated story/backlog skill, PM MCP server (Jira/Linear/GitHub Issues), or planning workflow in CLAUDE.md
- 3: Automated planning without human initiation — scheduled story generation, automatic backlog grooming, or autonomous epic decomposition

---

## Level–Criteria Mapping

After scoring all criteria, determine the highest adoption level where **all** thresholds are met:

| Criterion | Level 1 | Level 2 | Level 3 | Level 4 |
|-----------|---------|---------|---------|---------|
| A1 | ≥ 1 | ≥ 2 | ≥ 3 | ≥ 3 |
| A2 | ≥ 1 | ≥ 2 | ≥ 3 | ≥ 3 |
| A3 | — | ≥ 2 | ≥ 2 | ≥ 3 |
| A4 | ≥ 1 | ≥ 2 | ≥ 3 | ≥ 3 |
| A5 | — | ≥ 1 | ≥ 3 | ≥ 3 |
| A6 | — | — | ≥ 3 | ≥ 3 |
| A7 | — | — | — | ≥ 3 |
| A8 | — | — | — | ≥ 2 |

Check Level 1 first. If all Level 1 thresholds are met, check Level 2, and so on. The achieved level is the highest where all thresholds pass.

---

## Report Format

Produce a report in exactly this structure:

---

# Agent Adoption Assessment Report

**Project**: [name from README or directory name]
**Date**: [today's date]

## Result: Level [0/1/2/3/4] — [Level Name]

Level names: 0 = Unassisted, 1 = Vibe Coding, 2 = Agentic Engineering, 3 = Software Factory, 4 = Sustainable Autonomy

## Criterion Scores

| Criterion | Name | Score | Max |
|-----------|------|-------|-----|
| A1 | Agent Context Availability | [score] | 3 |
| A2 | Agent-Authored Contributions | [score] | 3 |
| A3 | Feedback Loop Closure | [score] | 3 |
| A4 | Task Scope | [score] | 3 |
| A5 | Workflow Integration | [score] | 3 |
| A6 | Autonomous Operation | [score] | 3 |
| A7 | Proactive Quality Management | [score] | 3 |
| A8 | Planning Integration | [score] | 3 |

## Gaps Blocking the Next Level

[If the project is at Level 4, write "Maximum level reached."]

[Otherwise, list each criterion below threshold for Level N+1:]

To reach Level [N+1] ([Name]), improve:
- **A_ [Name]**: currently [score], need [required] — [one sentence on what to improve]

## Readiness–Adoption Compatibility

[State the minimum recommended readiness level for the current adoption level:
- Adoption 0–1: Readiness 1+ recommended
- Adoption 2: Readiness 2+ recommended
- Adoption 3–4: Readiness 3 required

If the project's readiness level is known, note whether it supports the adoption level. If readiness is unknown, recommend running `/assess-readiness`.]

## Recommendations

[3–5 prioritised, actionable recommendations based on the gaps. Order by impact: criteria blocking a level increase first, then easiest wins.]

---
