---
name: verify-c2-1
description: Verify readiness criterion C2.1 (Setup Automation) in the current project. Reports fulfillment level 0–3.
allowed-tools: Bash Read Write
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Verify C2.1 — Setup Automation

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | No setup instructions |
| 1 | Written step-by-step instructions |
| 2 | Single script installs all prerequisites and toolchain |
| 3 | Containerised environment (devcontainer, Nix, etc.) |

## Evidence to Gather

- Check for a containerised or declarative environment (devcontainer, Nix flake, etc.) at the project root.
- Look for setup or install scripts (at the root or in a `scripts/` directory).
- Read the README for a setup or getting-started section and assess how many manual steps it requires.
- Look through other documentation files for any additional setup instructions.
- If there is a script or setup instructions, choose the most appropriate devcontainer image and attempt to set up the dev environment within a devcontainer.

## Instructions

Gather the evidence described above and determine the fulfillment level for C2.1.

Scoring guide:
- **Level 0**: No setup instructions anywhere — no README section, no scripts, no manifest.
- **Level 1**: Written instructions exist (e.g., a README "Getting Started" section) but setup requires a human to follow steps manually; no single command does everything.
- **Level 2**: A script (setup.sh, install.sh, etc.) installs all prerequisites and toolchain with one command. Prefer evidence of actual command execution success where available.
- **Level 3**: A fully containerised or declarative environment exists and is experimentally validated. For devcontainer, require successful `devcontainer up` and `devcontainer exec` results.

Report in exactly this format:

**C2.1 — Setup Automation**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [one or two sentences citing the specific evidence]