---
name: improve-c4-1
description: Improve readiness criterion C4.1 (Requirements Access) in the current project by generating vision and user story documentation. Raises the fulfillment level by one step.
allowed-tools: Bash Read Write Edit
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Improve C4.1 — Requirements Access

## Current State

Examine the project to understand its current state:

- Look for any existing vision, requirements, or goals documents and read them.
- Check for stories, features, or backlog directories.
- Check the MCP server configuration for any project management tool connections.
- Read the README and browse key source files to understand what the system does and for whom (needed to write accurate requirements from scratch if none exist).

## Instructions

**Step 1 — Determine current level:**
- Level 0: No documented requirements, no vision
- Level 1: Product vision or goals documented
- Level 2: User stories or acceptance criteria accessible
- Level 3: Programmatic access via MCP server or API (cannot be automated — requires external infrastructure setup)

**Step 2 — Read the project thoroughly before writing:**
Read the README, source entry points, and route definitions to understand what the system does and who uses it.

**Step 3 — Implement the improvement:**

**If current level is 0 → raise to 1:**
Create `VISION.md` at the project root. Infer the product's purpose, users, and goals from the README and codebase. Write:
- **Problem**: What problem does this solve?
- **Users**: Who uses this system?
- **Goals**: What are the 3–5 key product goals?
- **Non-goals**: What is explicitly out of scope?
- **Success metrics**: How would we know it's working?

Base the content on actual evidence from the code — do not write generic placeholders.

**If current level is 1 → raise to 2:**
Create a `stories/` directory and populate it with user stories inferred from the codebase (routes, controllers, features). Create:
- `stories/README.md` — explanation of the stories directory and story format
- One `.md` file per major feature area, each containing 3–5 user stories in the format:
  ```
  ## [Feature Name]
  
  **As a** [user type],
  **I want to** [action],
  **so that** [benefit].
  
  **Acceptance criteria:**
  - [ ] [specific, testable criterion]
  - [ ] [specific, testable criterion]
  ```

Infer features from route definitions, controller names, and existing code. Aim for 10–20 stories total covering the main functionality.

**If current level is 2 → raise to 3:**
Level 3 requires programmatic access via MCP server or API, which requires external infrastructure (a running MCP server connected to a project management tool). This cannot be fully automated.

Explain what would be needed: configure an MCP server connection to GitHub Issues, Linear, Jira, or Notion in `.claude/settings.json`, and ensure stories are importable from that tool.

**If already at level 3:**
Report that C4.1 is already at its maximum level (3) and no improvement is needed.

**Step 4 — Report:**
State what file(s) were created or modified, the before and after level.
