---
name: verify-c2-1
description: Verify readiness criterion C2.1 (Setup Automation) in the current project. Reports fulfillment level 0–3.
allowed-tools: Bash Read
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
| 2 | Single script installs all dependencies |
| 3 | Containerised environment (devcontainer, Nix, etc.) |

## Evidence to Gather

- Check for a containerised or declarative environment (devcontainer, Nix flake, etc.) at the project root.
- Look for setup or install scripts (at the root or in a `scripts/` directory) and any relevant Makefile targets.
- Check for standard dependency manifests (package.json, requirements.txt, go.mod, etc.) that imply one-command installation.
- Read the README for a setup or getting-started section and assess how many manual steps it requires.

## Instructions

Gather the evidence described above and determine the fulfillment level for C2.1.

Scoring guide:
- **Level 0**: No setup instructions anywhere — no README section, no scripts, no manifest.
- **Level 1**: Written instructions exist (e.g., a README "Getting Started" section) but setup requires a human to follow steps manually; no single command does everything.
- **Level 2**: A script (setup.sh, Makefile target, etc.) or standard tooling (`npm install`, `pip install -r requirements.txt`) installs all dependencies with one command. The README may still exist but the script is the primary mechanism.
- **Level 3**: A fully containerised or declarative environment exists — devcontainer (.devcontainer/devcontainer.json), Nix (flake.nix / shell.nix), or equivalent — that reproduces the environment completely without manual steps.

Report in exactly this format:

**C2.1 — Setup Automation**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [one or two sentences citing the specific evidence]
