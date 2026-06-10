---
name: verify-c5-1
description: Verify readiness criterion C5.1 (Runnability) in the current project. Reports fulfillment level 0–2.
allowed-tools: Bash Read
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Verify C5.1 — Runnability

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | Project does not build |
| 1 | Project builds without errors |
| 2 | App can be run locally or in an ephemeral environment |

## Evidence to Gather

- Identify the project's language and build system from manifest files at the root.
- Look for build and run scripts in the build manifest, Makefile, or equivalent.
- Check for runtime configuration that indicates the app can be launched (Procfile, docker-compose, run script, etc.).
- Read the README for build and run instructions.
- If the project has a devcontainer or similar, attempt to build and run the app locally within that environment to validate the evidence.
- If the app doesn't have a devcontainer but has a build and run script, attempt to execute those within a suitable container, but not on the host machine.


## Instructions

Gather the evidence described above and determine the fulfillment level for C5.1.

Scoring guide:
- **Level 0**: The project does not build or the build system is missing/broken. Indicators: no build manifest, no build instructions, CI consistently failing on build steps (if CI exists).
- **Level 1**: The project builds successfully — compilation succeeds, dependencies resolve, no build-time errors.
- **Level 2**: The application can be run locally — a server starts, a CLI executes, a container runs.

Report in exactly this format:

**C5.1 — Runnability**
- **Level**: [0 / 1 / 2]
- **Rationale**: [one or two sentences citing the specific evidence]