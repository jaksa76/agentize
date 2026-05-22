---
name: improve-readiness
description: Assess the current readiness level of the project and implement all improvements needed to raise it to the next level. Delegates to /assess-readiness for scoring and to the relevant /improve-c* skills for each blocking criterion.
allowed-tools: Bash Read Write Edit
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Improve Readiness Level

This skill assesses the current readiness level, identifies which criteria block the next level, and implements improvements for each blocking criterion.

---

## Instructions

### Step 1 — Assess current readiness level

Follow the `/assess-readiness` skill to score all 11 criteria and determine the current readiness level. Record all criterion scores.

---

### Step 2 — Identify the target level and blocking criteria

- If current level is 3: Report "This project is already at Level 3 — Supervised Autonomy. No further readiness improvements are possible." Stop here.
- Otherwise, target level = current level + 1.
- Using the table below, list every criterion where the score is below the target level's threshold. These are the **blocking criteria**.

| Criterion | Level 1 requires | Level 2 requires | Level 3 requires |
|-----------|-----------------|-----------------|-----------------|
| C1.1 Codebase Accessibility | ≥ 1 | ≥ 2 | ≥ 2 |
| C2.1 Setup Automation | ≥ 1 | ≥ 2 | ≥ 3 |
| C3.1 Architecture Depth | — | ≥ 1 | ≥ 3 |
| C4.1 Requirements Access | — | ≥ 1 | ≥ 3 |
| C5.1 Runnability | ≥ 1 | ≥ 2 | ≥ 2 |
| C5.2 Unit Test Coverage | ≥ 1 | ≥ 2 | ≥ 3 |
| C5.3 Integration and E2E Coverage | — | ≥ 1 | ≥ 2 |
| C6.1 Static Analysis | — | ≥ 1 | ≥ 2 |
| C7.1 Test Isolation | — | — | ≥ 2 (skip if N/A) |
| C8.1 CI/CD Automation | — | ≥ 1 | ≥ 3 |
| C8.2 Observability | — | — | ≥ 2 |

Level names: 0 = Uninstrumented, 1 = Foundation, 2 = Guided Autonomy, 3 = Supervised Autonomy

---

### Step 3 — Report the current state

Print a summary before making any changes:

```
## Current Readiness

**Level**: [N] — [Level Name]
**Target**: Level [N+1] — [Level Name]

## Blocking Criteria for Level [N+1]

| Criterion | Name | Current Score | Required |
|-----------|------|---------------|----------|
| C_._ | [Name] | [score] | ≥ [threshold] |
...

## Improvements to implement

- C_._ → /improve-c_-_ (current: [score] → target: [threshold])
...
```

---

### Step 4 — Implement improvements for each blocking criterion

For each blocking criterion identified in Step 3, follow the corresponding improvement skill. Work through them in order (lowest criterion ID first).

- **C1.1 is blocking** → follow the `/improve-c1-1` skill
- **C2.1 is blocking** → follow the `/improve-c2-1` skill
- **C3.1 is blocking** → follow the `/improve-c3-1` skill
- **C4.1 is blocking** → follow the `/improve-c4-1` skill
- **C5.1 is blocking** → follow the `/improve-c5-1` skill
- **C5.2 is blocking** → follow the `/improve-c5-2` skill
- **C5.3 is blocking** → follow the `/improve-c5-3` skill
- **C6.1 is blocking** → follow the `/improve-c6-1` skill
- **C7.1 is blocking** → follow the `/improve-c7-1` skill
- **C8.1 is blocking** → follow the `/improve-c8-1` skill
- **C8.2 is blocking** → follow the `/improve-c8-2` skill

---

### Step 5 — Final report

After completing all improvements, produce a summary:

```
## Improvement Summary

**Previous level**: Level [N] — [Name]
**New level**: Level [N+1] — [Name] (if all blocking criteria have been resolved)

### Changes made

| Criterion | Before | After | Change |
|-----------|--------|-------|--------|
| C_._ [Name] | [old score] | [new score] | [file/action] |
...

### Remaining gaps (if any)

[List any criteria that could not be fully automated, e.g., C4.1 → 3 requires MCP infrastructure, C8.2 → 2 requires external monitoring setup. Explain what manual steps the team needs to take.]

### Next steps

[If still below Level 3, note what the next improvement cycle would target.]
```
