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

This skill runs all 8 criterion checks and produces a structured adoption report.

---

## Instructions

### Step 1 — Score each criterion

For each criterion, read the corresponding skill file and follow its evidence-gathering and scoring instructions. Record the score before moving to the next criterion.

- **A1 Agent Context Availability** — follow the `/verify-a1` skill
- **A2 Agent-Authored Contributions** — follow the `/verify-a2` skill
- **A3 Feedback Loop Closure** — follow the `/verify-a3` skill
- **A4 Task Scope** — follow the `/verify-a4` skill
- **A5 Workflow Integration** — follow the `/verify-a5` skill
- **A6 Autonomous Operation** — follow the `/verify-a6` skill
- **A7 Proactive Quality Management** — follow the `/verify-a7` skill
- **A8 Planning Integration** — follow the `/verify-a8` skill

---

### Step 2 — Determine the adoption level

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

### Step 3 — Produce the report

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
