---
name: improve-adoption
description: Assess the current Agent Adoption level of the project, identify which criteria block the next level, and implement improvements for each blocking criterion to raise the project to the next adoption level. Delegates to /assess-adoption for scoring and to the relevant /improve-a* skills for each blocking criterion.
allowed-tools: Bash Read Write Edit
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Improve Adoption Level

This skill assesses the current adoption level, identifies which criteria block the next level, and implements improvements for each blocking criterion.

---

## Instructions

### Step 1 — Assess current adoption level

Follow the `/assess-adoption` skill to score all 8 criteria and determine the current adoption level. Record all criterion scores.

---

### Step 2 — Identify the target level and blocking criteria

- If current level is 4: Report "This project is already at Level 4 — Sustainable Autonomy. No further adoption improvements are possible." Stop here.
- Otherwise, target level = current level + 1.
- Using the table below, list every criterion where the score is below the target level's threshold. These are the **blocking criteria**.

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

Level names: 0 = Unassisted, 1 = Vibe Coding, 2 = Agentic Engineering, 3 = Software Factory, 4 = Sustainable Autonomy

---

### Step 3 — Report the current state

Print a summary before making any changes:

```
## Current Adoption Level

**Level**: [N] — [Level Name]
**Target**: Level [N+1] — [Level Name]

## Blocking Criteria for Level [N+1]

| Criterion | Name | Current Score | Required |
|-----------|------|---------------|----------|
| A_ | [Name] | [score] | ≥ [threshold] |
...

## Improvements to implement

- A_ → /improve-a_ (current: [score] → target: [threshold])
...
```

---

### Step 4 — Implement improvements for each blocking criterion

For each blocking criterion identified in Step 3, follow the corresponding improvement skill. Work through them in order (lowest criterion ID first).

- **A1 is blocking** → follow the `/improve-a1` skill
- **A2 is blocking** → follow the `/improve-a2` skill
- **A3 is blocking** → follow the `/improve-a3` skill
- **A4 is blocking** → follow the `/improve-a4` skill
- **A5 is blocking** → follow the `/improve-a5` skill
- **A6 is blocking** → follow the `/improve-a6` skill
- **A7 is blocking** → follow the `/improve-a7` skill
- **A8 is blocking** → follow the `/improve-a8` skill

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
| A_ [Name] | [old score] | [new score] | [file/action] |
...

### Remaining gaps (if any)

[List any criteria that could not be fully automated, e.g., A2 → 2 or 3 requires genuine changes in team behaviour that tooling alone cannot achieve. Explain what manual steps the team needs to take.]

### Next steps

[If still below Level 4, note what the next improvement cycle would target.]
```
