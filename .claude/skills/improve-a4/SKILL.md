---
name: improve-a4
description: Improve adoption criterion A4 (Task Scope) by creating skills and guidance that enable agents to handle progressively larger tasks. Raises the fulfillment level by one step.
allowed-tools: Bash Read Write Edit
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Improve A4 — Task Scope

## Current State

Examine the project to understand its current state:

- Check `.claude/skills/` and list existing skills with their descriptions to understand what scope they target.
- Read `CLAUDE.md` or `AGENTS.md` for any task scope guidance.
- Look at recent agent-co-authored commits to assess the scope of work agents currently handle.
- Look at the project structure and any backlog/task files to understand feasible task scope.

## Instructions

**Step 1 — Determine current level:**
- Level 0: No agent code changes; agents only answer questions
- Level 1: Agent commits are 1–2 files; single-function or bug-fix scope
- Level 2: Agent commits span 3+ files including tests; feature-level scope
- Level 3: Agent commits span services/packages; story-level scope with migrations and docs

**Step 2 — Implement the improvement:**

**If current level is 0 → raise to 1:**
Agents aren't making changes yet. Create the infrastructure for bounded contributions:

1. Create `.claude/skills/fix-bug/SKILL.md` — a skill for agents to fix a specific bug:
```markdown
---
name: fix-bug
description: Fix a specific bug described by the user. Makes targeted changes to the minimum number of files needed.
allowed-tools: Bash Read Write Edit
---

# Fix Bug

## Instructions
1. Read the bug description from the user's prompt carefully.
2. Locate the relevant code using Read and Bash (grep/find).
3. Understand the root cause before making any changes.
4. Make the minimal targeted change to fix the bug.
5. Run the test suite: `[test command from CLAUDE.md]`
6. If tests fail, fix them or adjust your approach.
7. Report: what was changed, why, and how to verify the fix.
```

2. Update CLAUDE.md to encourage using agents for bug fixes and small tasks.

**If current level is 1 → raise to 2:**
Agents are making small changes. Create a feature implementation skill for multi-file work:

Create `.claude/skills/implement-feature/SKILL.md`:
```markdown
---
name: implement-feature
description: Implement a complete feature spanning multiple files. Includes writing tests and running the full suite before completing.
allowed-tools: Bash Read Write Edit
---

# Implement Feature

## Instructions
1. Read the feature description carefully.
2. Read CLAUDE.md for project conventions and key commands.
3. Plan the implementation: identify which files to create/modify.
4. Read existing code in the affected areas before making changes.
5. Implement the feature across all necessary files.
6. Write tests for the new functionality (unit + integration if applicable).
7. Run: build → lint → tests. Fix any failures.
8. Report: files changed, tests added, how to verify.
```

Also update CLAUDE.md to state that feature-level tasks should be assigned to agents as a whole.

**If current level is 2 → raise to 3:**
Agents implement features. Elevate to story-level scope:

Create or update `.claude/skills/implement-story/SKILL.md` (similar to do-next-task) for end-to-end story implementation:
```markdown
---
name: implement-story
description: Implement a complete user story end-to-end, including all services, tests, documentation, and database migrations.
allowed-tools: Bash Read Write Edit
---

# Implement Story

## Instructions
1. Read the story description and acceptance criteria carefully.
2. Read CLAUDE.md for conventions, architecture, and commands.
3. Read VISION.md or relevant requirements docs.
4. Read all files in the affected service(s) before implementing.
5. Plan the full scope: API changes, DB migrations, frontend changes, tests, docs.
6. Implement all changes across all services/packages.
7. Write comprehensive tests: unit, integration, and E2E if applicable.
8. Update relevant documentation.
9. Run: build → lint → typecheck → tests. Fix any failures.
10. Report: all files changed, tests added, acceptance criteria verified.
```

Also create a `TODO.md` (if absent) with story-level items to make the story-scope expectation concrete.

**If already at level 3:**
Report that A4 is already at its maximum level (3) and no improvement is needed.

**Step 3 — Report:**
State what skills were created or modified, what CLAUDE.md sections were added, the before and after level.
