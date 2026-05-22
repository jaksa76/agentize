---
name: improve-c2-1
description: Improve readiness criterion C2.1 (Setup Automation) in the current project by adding or upgrading setup automation. Raises the fulfillment level by one step.
allowed-tools: Bash Read Write Edit
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Improve C2.1 — Setup Automation

## Current State

### Containerised environment
!`ls .devcontainer/ devcontainer.json flake.nix shell.nix 2>/dev/null || echo "(none)"`
!`cat .devcontainer/devcontainer.json 2>/dev/null | head -30 || echo "(no devcontainer)"`

### Setup scripts
!`ls setup.sh install.sh bootstrap.sh 2>/dev/null || echo "(none)"`
!`cat setup.sh 2>/dev/null || cat install.sh 2>/dev/null || echo "(no setup script)"`

### Makefile install targets
!`grep -i "^install\b\|^setup\b\|^dev\b\|^bootstrap\b" Makefile 2>/dev/null | head -10 || echo "(none)"`

### Language / dependency manager detection
!`ls package.json 2>/dev/null && cat package.json | python3 -c "import sys,json; d=json.load(sys.stdin); print('node version:', d.get('engines',{}).get('node','unspecified')); print('scripts:', list(d.get('scripts',{}).keys()))" 2>/dev/null || true`
!`ls requirements.txt Pipfile pyproject.toml 2>/dev/null || echo "(no Python deps)"`
!`ls pom.xml build.gradle Cargo.toml go.mod 2>/dev/null || echo "(no other build files)"`
!`ls Dockerfile .dockerignore 2>/dev/null || echo "(no Docker files)"`

### README setup section
!`grep -A15 -i "getting started\|quick start\|setup\|install\|prerequisites" README.md 2>/dev/null | head -30 || echo "(no setup section in README)"`

## Instructions

**Step 1 — Determine current level:**
- Level 0: No setup instructions anywhere
- Level 1: Written instructions exist in README but no automation script
- Level 2: A setup script (setup.sh, Makefile target, or standard `npm install` / `pip install`) installs everything with one command
- Level 3: A containerised/declarative environment exists (.devcontainer, Nix, etc.)

**Step 2 — Implement the improvement:**

**If current level is 0 → raise to 1:**
Add a "Getting Started" section to README.md (create it if missing) with step-by-step instructions for setting up the development environment. Include: prerequisites, dependency installation commands, environment variable setup, and how to verify the setup works.

**If current level is 1 → raise to 2:**
Create a `setup.sh` script at the project root that automates all the steps described in the README. Detect the language/package manager from the evidence above and write an appropriate script. For example:

- Node.js: install node version (if .nvmrc exists), run `npm install`, copy `.env.example` to `.env` if it exists
- Python: create virtualenv, install requirements, set up pre-commit hooks if present
- Java/Gradle: run `./gradlew dependencies`
- Make it executable (`chmod +x setup.sh`) and add a note to README to run `./setup.sh`

**If current level is 2 → raise to 3:**
Create a `.devcontainer/devcontainer.json`. Detect the primary language/runtime from the evidence, choose an appropriate base image from the Microsoft devcontainer base images, and include:
- Correct base image for the detected language/version
- `postCreateCommand` that runs the existing setup script or installs dependencies
- Any required VS Code extensions relevant to the detected language
- `forwardPorts` if a server port is detectable from package.json scripts or Procfile

Write the devcontainer.json with real values derived from the project, not generic placeholders.

**If already at level 3:**
Report that C2.1 is already at its maximum level (3) and no improvement is needed.

**Step 3 — Report:**
State what file(s) were created or modified, the before and after level.
