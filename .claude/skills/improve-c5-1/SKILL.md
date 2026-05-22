---
name: improve-c5-1
description: Improve readiness criterion C5.1 (Runnability) in the current project by adding run configuration. Raises the fulfillment level by one step.
allowed-tools: Bash Read Write Edit
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Improve C5.1 — Runnability

## Current State

Examine the project to understand its current state:

- Identify the language and build system from the dependency manifest.
- Look for build and run scripts in the build manifest, Makefile, or equivalent.
- Look for runtime configuration (Procfile, docker-compose, Dockerfile, .env.example, etc.).
- Look for the main entry point to understand how the app is started.

## Instructions

**Step 1 — Determine current level:**
- Level 0: Project does not build or build system is missing
- Level 1: Project builds without errors
- Level 2: App can be run locally or in an ephemeral environment

Note: Improving Level 0 → 1 (fixing a broken build) requires understanding the specific build failures and is too project-specific for automated improvement. If at Level 0, report the limitation and skip to recommendations.

**Step 2 — Implement the improvement:**

**If current level is 0 → cannot automate:**
Report that C5.1 Level 0 (broken build) cannot be automatically fixed — fixing build errors requires project-specific diagnosis. Recommend running the build manually, reading error output, and fixing the root cause. Suggest checking: missing dependencies, wrong Node/Python/Java version, missing environment variables.

**If current level is 1 → raise to 2:**
Add run configuration based on the detected project type:

- **Node.js (package.json)**: If no `start` script exists, add one to `package.json`. Detect the entry point from `main` field or look for `src/index.{js,ts}`, `app.{js,ts}`. Also create a `.env.example` if environment variables are referenced in code but no example file exists.

- **Python**: If no run script exists, create a `Makefile` (or add a target if Makefile exists) with a `run` target: `python -m <module>` or `uvicorn main:app` or `flask run` depending on detected framework. Create `.env.example` if needed.

- **Docker-based**: If a Dockerfile exists but no docker-compose, create a minimal `docker-compose.yml` that builds and runs the app with appropriate port mapping (detect port from code or use 3000/8000/8080 as defaults for web apps).

- **Any project**: Create a `Procfile` if none exists, listing the web process: `web: <start command>`.

Also create `.env.example` if the code references environment variables but no example file exists.

**If already at level 2:**
Report that C5.1 is already at its maximum level (2) and no improvement is needed.

**Step 3 — Report:**
State what file(s) were created or modified, the before and after level.
