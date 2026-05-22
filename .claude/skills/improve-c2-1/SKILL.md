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

Examine the project to understand its current state:

- Check for a containerised or declarative environment (devcontainer, Nix, etc.).
- Look for setup or install scripts and relevant Makefile targets.
- Identify the dependency manager and installation command from the build manifest.
- Read the README setup section to understand the current manual steps required.

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
