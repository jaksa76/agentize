---
name: improve-a3
description: Improve adoption criterion A3 (Feedback Loop Closure) by adding verification guidance to agent context files and configuring CI/monitoring MCP access. Raises the fulfillment level by one step.
allowed-tools: Bash Read Write Edit
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Improve A3 — Feedback Loop Closure

## Current State

Examine the project to understand its current state:

- Read `CLAUDE.md` or `AGENTS.md` and look for any verification or quality-check guidance already present.
- Check skill files in `.claude/skills/` for verification steps (build, test, lint commands).
- Identify the available quality commands from the build manifest, Makefile, or equivalent.
- Check the MCP server configuration for CI pipeline or monitoring access.
- Check `.claude/settings.json` for any hooks already configured.

## Instructions

**Step 1 — Determine current level:**
- Level 0: No verification guidance — agents hand output directly to humans
- Level 1: Basic checks only (build/compile) — no full test suite instruction
- Level 2: CLAUDE.md/AGENTS.md or skills explicitly instruct agents to run full test suite, iterate on failures, present only passing results
- Level 3: Level 2 PLUS CI pipeline access AND production monitoring access via MCP

**Step 2 — Implement the improvement:**

**If current level is 0 → raise to 1:**
Add a verification section to CLAUDE.md (create if absent) with at minimum the build command:

```markdown
## Before Submitting Changes

Always verify your changes compile/build before presenting them:
- Build: `[detected build command]`
- If the build fails, fix the errors before proceeding.
```

Detect the build command from the evidence above (e.g., `npm run build`, `go build ./...`, `./mvnw package -DskipTests`, `cargo build`).

**If current level is 1 → raise to 2:**
Expand the verification section in CLAUDE.md to require full test suite execution with iteration:

```markdown
## Before Submitting Changes

Run all of the following and fix any failures before creating a PR or presenting results:

1. **Build**: `[build command]`
2. **Lint**: `[lint command]`
3. **Type check**: `[typecheck command]` (if applicable)
4. **Tests**: `[test command]`

If tests fail:
- Read the failure output carefully
- Fix the root cause (not just the symptom)
- Re-run the full suite to confirm the fix does not break other tests
- Only present your work when the full suite passes

Do NOT skip this step or present results with failing tests.
```

Fill in the actual commands detected from package.json scripts or Makefile. Also update any existing skills to include these verification steps before their "Report" section.

**If current level is 2 → raise to 3:**
Add MCP server access for CI pipeline and production monitoring:

1. **CI pipeline access** — add a GitHub MCP server if not present:
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}" }
    }
  }
}
```

2. **Extend CLAUDE.md** with post-PR verification guidance:
```markdown
## Post-PR Verification

After creating a PR:
1. Check CI status using the GitHub MCP server: get workflow runs for the PR branch
2. If CI fails, read the failure logs and fix the issue
3. Re-push and confirm CI passes before requesting review
```

3. If the project has a monitoring tool (Sentry, Datadog, etc.), also add that MCP server and document how to check for post-deployment errors.

**If already at level 3:**
Report that A3 is already at its maximum level (3) and no improvement is needed.

**Step 3 — Report:**
State what files were created or modified, the before and after level.
