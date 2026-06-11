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

This skill runs all 11 criterion checks and produces a structured readiness report.

---

## Instructions

### Step 1 — Score each criterion

For each criterion, read the corresponding skill file and follow its evidence-gathering and scoring instructions. Record the score before moving to the next criterion.

- **C1.1 Codebase Accessibility** — follow the `/agentize:verify-c1-1` skill
- **C2.1 Setup Automation** — follow the `/agentize:verify-c2-1` skill
- **C3.1 Architecture Depth** — follow the `/agentize:verify-c3-1` skill
- **C4.1 Requirements Access** — follow the `/agentize:verify-c4-1` skill
- **C5.1 Runnability** — follow the `/agentize:verify-c5-1` skill
- **C5.2 Unit Test Coverage** — follow the `/agentize:verify-c5-2` skill
- **C5.3 Integration and E2E Coverage** — follow the `/agentize:verify-c5-3` skill
- **C6.1 Static Analysis** — follow the `/agentize:verify-c6-1` skill
- **C7.1 Test Isolation** — follow the `/agentize:verify-c7-1` skill
- **C8.1 CI/CD Automation** — follow the `/agentize:verify-c8-1` skill
- **C8.2 Observability** — follow the `/agentize:verify-c8-2` skill

---

### Step 2 — Determine the readiness level

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

### Step 3 — Produce the report

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
