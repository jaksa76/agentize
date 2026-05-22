---
name: verify-a4
description: Verify adoption criterion A4 (Task Scope) in the current project. Reports fulfillment level 0–3.
allowed-tools: Bash Read
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Verify A4 — Task Scope

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | Agents only answer questions or explain code; they do not make changes |
| 1 | Agents handle bounded edits: a single function, a bug fix, a single-file change |
| 2 | Agents implement complete features spanning multiple files, writing and running tests as part of the implementation |
| 3 | Agents implement entire user stories end-to-end, including cross-service changes, test suites, documentation, and migration scripts |

## Evidence to Gather

- Look at agent-co-authored commits in recent git history and assess how many files each changed — this indicates the scope of tasks agents routinely handle.
- Read skill definitions in `.claude/skills/` to understand the scope of tasks they describe (single-function fixes vs. multi-file features vs. story-level work).
- Read `CLAUDE.md` or `AGENTS.md` for any guidance on expected task granularity.
- Look for task tracking files (`TODO.md`, `BACKLOG.md`, `stories/`) and assess the granularity of items in them.

## Instructions

Gather the evidence described above and determine the fulfillment level for A4.

This criterion measures the largest scope of work that agents routinely handle end-to-end in this project. Look for evidence in git history (file counts per agent commit), skill definitions, and CLAUDE.md/AGENTS.md guidance.

Scoring guide:
- **Level 0**: No evidence of agents making code changes — no co-authored commits in git history, skills only describe Q&A or explanation tasks.
- **Level 1**: Agent-authored commits exist but are consistently small — 1–2 files changed, targeted bug fixes, single-function additions. Skill definitions describe bounded tasks.
- **Level 2**: Agent-authored commits regularly span multiple files (3+), include test files alongside implementation files, and/or skills describe full feature implementation as the expected scope.
- **Level 3**: Agent-authored commits span services or packages, include migrations, documentation, and comprehensive test suites. Skills or CLAUDE.md describe user-story-level implementation as the target scope. TODO/backlog items are story-level, not sub-task-level.

Report in exactly this format:

**A4 — Task Scope**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [one or two sentences citing the specific evidence]
