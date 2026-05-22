---
name: improve-c1-1
description: Improve readiness criterion C1.1 (Codebase Accessibility) in the current project by creating or enhancing the agent context file (CLAUDE.md). Raises the fulfillment level by one step.
allowed-tools: Bash Read Write Edit
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Improve C1.1 — Codebase Accessibility

## Current State

Examine the project to understand its current state:

- Check for agent context files (`CLAUDE.md`, `AGENTS.md`, or equivalent) and read their full content.
- Read `README.md` to assess its depth.
- Look at the project root structure and source directories to understand the layout and technology stack.
- Identify key build, run, and test commands from the build manifest or Makefile.

## Instructions

**Step 1 — Determine current level:**
- Level 0: No README and no CLAUDE.md/AGENTS.md
- Level 1: README exists but no CLAUDE.md/AGENTS.md (or it's minimal)
- Level 2: CLAUDE.md or AGENTS.md exists with substantive conventions, commands, and navigation guidance

**Step 2 — Implement the improvement:**

**If current level is 0 → raise to 1:**
Create a `README.md` at the project root with at minimum:
- Project name and one-paragraph description of what it does and why
- Getting started section (prerequisites, how to clone and run)
- Basic project structure overview

**If current level is 1 → raise to 2:**
Create a `CLAUDE.md` at the project root. Base it on the evidence above (README content, detected language/framework, directory structure, build scripts). Include:

```markdown
# CLAUDE.md

## Project Overview
[brief description of what this project does]

## Key Commands
[list the most important commands: build, test, run, lint — use the actual commands detected above]

## Project Structure
[describe the main directories and what lives in them]

## Coding Conventions
[list conventions: naming style, file organisation, patterns used — infer from the existing code structure]

## Important Notes
[any non-obvious constraints, environment variables required, external services, known gotchas]
```

Read enough of the actual codebase to write accurate, project-specific content. Do not write generic placeholder text.

**If already at level 2:**
Report that C1.1 is already at its maximum level (2) and no improvement is needed.

**Step 3 — Report:**
State what file was created or modified, what level it was at before, and what level it is now.
