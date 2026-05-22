---
name: improve-c8-1
description: Improve readiness criterion C8.1 (CI/CD Automation) in the current project by creating or extending GitHub Actions workflows. Raises the fulfillment level by one step.
allowed-tools: Bash Read Write Edit
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Improve C8.1 — CI/CD Automation

## Current State

Examine the project to understand its current state:

- Look for CI configuration files and read their content to understand the pipeline structure.
- Check for `workflow_dispatch` or equivalent manual triggers.
- Check the MCP server configuration for any CI/CD pipeline access.
- Look for deployment infrastructure configuration and deployment steps in existing workflows.
- Identify the language and build system so the CI workflow can be appropriately tailored.

## Instructions

**Step 1 — Determine current level:**
- Level 0: No CI pipeline exists
- Level 1: CI pipeline exists AND agents can read pipeline status (via GitHub API / MCP)
- Level 2: Agents can trigger pipeline runs (workflow_dispatch or equivalent)
- Level 3: Full pipeline control including deployment

Note: Level 1 requires a GitHub/GitLab MCP server for agents to read pipeline status programmatically. Creating the CI workflow is necessary but not sufficient — the MCP connection must also exist or be documented.

**Step 2 — Implement the improvement:**

**If current level is 0 → raise to 1:**
Create a CI workflow appropriate to the detected language. Create `.github/workflows/ci.yml`:

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - [language-specific setup step]
      - name: Install dependencies
        run: [install command]
      - name: Lint
        run: [lint command if linting is configured]
      - name: Test
        run: [test command]
```

Fill in the language-specific steps from the evidence above. Include `workflow_dispatch` trigger from the start (it makes Level 2 easier later).

Also add a note to CLAUDE.md (if it exists) that agents can check CI status via the GitHub API.

**If current level is 1 → raise to 2:**
Ensure `workflow_dispatch` is present in the CI workflow (add it if missing). This allows agents to trigger runs via the GitHub API.

Also document in CLAUDE.md how an agent can trigger CI:
```markdown
## CI/CD
- Check CI status: use the GitHub MCP server's `get_workflow_runs` tool
- Trigger CI: use the GitHub MCP server's `create_workflow_dispatch` tool on the `ci.yml` workflow
```

If no GitHub MCP server is configured in `.claude/settings.json`, document what needs to be set up.

**If current level is 2 → raise to 3:**
Add a deployment workflow. Based on detected infrastructure:

- **Fly.io** (`fly.toml` exists): Create `.github/workflows/deploy.yml` using `superfly/flyctl-actions` to deploy on push to main.
- **Heroku** (`heroku.yml` exists): Add Heroku deploy action.
- **Docker + generic**: Create a workflow that builds and pushes a Docker image to GitHub Container Registry (ghcr.io), then triggers a deployment via webhook or kubectl.
- **No infrastructure detected**: Create a template `.github/workflows/deploy.yml` with placeholders and clear comments explaining what to fill in.

Include `workflow_dispatch` in the deploy workflow so agents can trigger deployments manually.

**If already at level 3:**
Report that C8.1 is already at its maximum level (3) and no improvement is needed.

**Step 3 — Report:**
State what files were created or modified, the before and after level.
