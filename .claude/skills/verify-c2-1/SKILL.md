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

## Evidence

### Containerised environment
!`ls .devcontainer/ devcontainer.json flake.nix shell.nix default.nix 2>/dev/null || echo "(none found)"`
!`ls .devcontainer/ 2>/dev/null && cat .devcontainer/devcontainer.json 2>/dev/null | head -20 || true`

### Setup / install scripts
!`ls setup.sh install.sh bootstrap.sh Makefile scripts/setup.sh scripts/install.sh 2>/dev/null || echo "(none found)"`
!`grep -i "^install\b\|^setup\b\|^bootstrap\b\|^dev\b\|^deps\b" Makefile 2>/dev/null | head -10 || echo "(no relevant Makefile targets)"`

### Dependency manifest (indicates automated install is possible)
!`ls package.json requirements.txt Pipfile pyproject.toml pom.xml build.gradle Cargo.toml go.mod 2>/dev/null || echo "(no standard dependency manifests)"`

### README setup / getting-started section
!`grep -A15 -i "getting started\|quick start\|setup\|install\|prerequisites" README.md 2>/dev/null | head -40 || echo "(no setup section in README)"`

## Instructions

Analyse the evidence above and determine the fulfillment level for C2.1.

Scoring guide:
- **Level 0**: No setup instructions anywhere — no README section, no scripts, no manifest.
- **Level 1**: Written instructions exist (e.g., a README "Getting Started" section) but setup requires a human to follow steps manually; no single command does everything.
- **Level 2**: A script (setup.sh, Makefile target, etc.) or standard tooling (`npm install`, `pip install -r requirements.txt`) installs all dependencies with one command. The README may still exist but the script is the primary mechanism.
- **Level 3**: A fully containerised or declarative environment exists — devcontainer (.devcontainer/devcontainer.json), Nix (flake.nix / shell.nix), or equivalent — that reproduces the environment completely without manual steps.

Report in exactly this format:

**C2.1 — Setup Automation**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [one or two sentences citing the specific evidence]
