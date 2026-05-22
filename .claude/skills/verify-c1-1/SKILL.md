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
| 0 | Code split across unlinked repos |
| 1 | Repos linked through submodules or other mechanisms |
| 2 | Monolith or Mono-repo |

## Evidence to Gather

- Look at the project root structure to understand the overall layout and whether there is a single entry point.
- Read `README.md` and assess whether this repository is part of a larger multi-repo setup.
- Check for dependencies and references to other repositories in documentation, build files, or configuration files.
- Check for any indicators of a multi-repo setup (gitmodules, symlinks, references to other repos).
- Check if the project is a back-end for a missing front-end or vice versa. Front-end and back-end should be in the same repository for better accessibility.

## Instructions

Gather the evidence described above and determine the fulfillment level for C1.1.

Scoring guide:
- **Level 0**: No single entry point; code is split across unlinked locations with no README to orient a newcomer.
- **Level 1**: Repos linked through submodules or other mechanisms.
- **Level 2**: Monolith or Mono-repo.

Report in exactly this format:

**C1.1 — Codebase Accessibility**
- **Level**: [0 / 1 / 2]
- **Rationale**: [one or two sentences citing the specific evidence]
