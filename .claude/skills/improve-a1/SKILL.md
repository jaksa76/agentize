---
name: improve-a1
description: Improve adoption criterion A1 (Agent Context Availability) in the current project by creating or enriching agent context files and MCP configuration. Raises the fulfillment level by one step.
allowed-tools: Bash Read Write Edit
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Improve A1 — Agent Context Availability

## Current State

Examine the project to understand its current state:

- Check for agent context files (`CLAUDE.md`, `AGENTS.md`, or equivalent) and read their content.
- Check the MCP server configuration for any servers that expose project knowledge.
- Look for architecture documentation or a `docs/` directory.
- Read `README.md` to assess its current depth and usefulness.
- Look at the project root to understand the structure and technology stack.

## Instructions

**Step 1 — Determine current level:**
- Level 0: No agent context file; no meaningful README
- Level 1: Basic README only; no CLAUDE.md/AGENTS.md
- Level 2: CLAUDE.md or AGENTS.md with conventions, commands, architecture overview
- Level 3: Level 2 PLUS architecture docs for agent consumption AND MCP servers exposing project knowledge

**Step 2 — Implement the improvement:**

**If current level is 0 → raise to 1:**
The README is too minimal or absent. Create or substantially expand `README.md` to include:
- Project name and clear one-paragraph description
- Who uses this system (users/actors)
- Getting started (prerequisites, installation, first run)
- High-level project structure

**If current level is 1 → raise to 2:**
Create `CLAUDE.md` at the project root. Read the codebase thoroughly first, then write a substantive file covering:

```markdown
# CLAUDE.md

## Project Overview
[what this system does and for whom — inferred from code]

## Key Commands
[actual commands for building, testing, running, linting — from package.json scripts, Makefile, etc.]

## Project Structure
[what each main directory contains — inferred from the file tree]

## Coding Conventions
[naming style, file organisation, patterns — inferred from existing code]

## Workflow
[how to make changes: branch naming, commit style, PR process if detectable]

## Important Notes
[non-obvious constraints, required env vars, external services, known gotchas]
```

Do not write placeholder text — every section must be based on actual project evidence.

**If current level is 2 → raise to 3:**
Two things are needed: architecture docs and MCP access. Do both:

1. **Architecture docs for agent consumption**: If `docs/ARCHITECTURE.md` doesn't exist, create it with system-context and service-level documentation (use the same approach as `improve-c3-1`). Ensure it is referenced from CLAUDE.md.

2. **MCP server configuration**: Add a GitHub MCP server (or the most relevant MCP for this project) to `.claude/settings.json`. Create the file if it doesn't exist:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```

Add `GITHUB_PERSONAL_ACCESS_TOKEN=` to `.env.example` with a comment.

Update CLAUDE.md to mention what MCP servers are available and what they expose.

**If already at level 3:**
Report that A1 is already at its maximum level (3) and no improvement is needed.

**Step 3 — Report:**
State what files were created or modified, the before and after level.
