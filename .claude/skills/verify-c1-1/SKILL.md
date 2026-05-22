---
name: verify-c1-1
description: Verify readiness criterion C1.1 (Codebase Accessibility) in the current project. Reports fulfillment level 0–2.
allowed-tools: Bash Read
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Verify C1.1 — Codebase Accessibility

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | Code split across unlinked repos with no entry point |
| 1 | All code reachable from a single root with a basic README |
| 2 | Comprehensive entry-point guide (CLAUDE.md or equivalent) with conventions and navigation hints |

## Evidence to Gather

- Look at the project root structure to understand the overall layout and whether there is a single entry point.
- Read `README.md` and assess its usefulness as a starting point for an agent or newcomer.
- Check for `CLAUDE.md`, `AGENTS.md`, or equivalent and read their content to assess quality and depth.
- Check for any indicators of a multi-repo setup (gitmodules, symlinks, references to other repos).

## Instructions

Gather the evidence described above and determine the fulfillment level for C1.1.

Scoring guide:
- **Level 0**: No single entry point; code is split across unlinked locations with no README to orient a newcomer.
- **Level 1**: A README exists at the root and all relevant code is reachable from there. The README describes the project's purpose but does not provide agent-specific conventions or navigation guidance.
- **Level 2**: A CLAUDE.md, AGENTS.md, or equivalent file exists and contains meaningful project-specific guidance: key commands, coding conventions, architecture overview, or navigation hints beyond what a basic README provides.

Report in exactly this format:

**C1.1 — Codebase Accessibility**
- **Level**: [0 / 1 / 2]
- **Rationale**: [one or two sentences citing the specific evidence]
