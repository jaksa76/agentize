---
name: verify-a3
description: Verify adoption criterion A3 (Feedback Loop Closure) in the current project. Reports fulfillment level 0–3.
allowed-tools: Bash Read
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Verify A3 — Feedback Loop Closure

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | Agents produce output and hand it directly to the human; no self-verification |
| 1 | Agents run basic checks (compilation, syntax) but do not iterate on failures before presenting results |
| 2 | Agents run the full test suite and linter, iterate on failures, and present only passing results to the human |
| 3 | Agents have access to CI pipeline results, production monitoring, and MCP-connected tool outputs; verification is fully automated and includes post-deployment checks |

## Evidence to Gather

- Read `CLAUDE.md` or `AGENTS.md` and look for sections that instruct agents to run tests, linters, or other quality checks before presenting results.
- Check the `.claude/skills/` directory — read skill files and assess whether they include verification steps (build, test, lint) before reporting results.
- Check the MCP server configuration (`.claude/settings.json`, `.mcp.json`) for any CI pipeline or production monitoring servers that give agents programmatic access.
- Check `.claude/settings.json` for hooks that automatically run quality checks.
- Look for a test suite (test directories or test files) that an agent could run.

## Instructions

Gather the evidence described above and determine the fulfillment level for A3.

This criterion measures the degree to which agents close their own feedback loops before handing work to a human. Look for evidence that the workflow (skills, CLAUDE.md, AGENTS.md) instructs or enables agents to verify their own output.

Scoring guide:
- **Level 0**: No verification guidance in agent context files or skills. Agents produce output and pass it directly to humans with no self-check.
- **Level 1**: Agent context files mention compilation or syntax checks, or skills run basic build commands, but there is no instruction to run the full test suite or iterate on failures.
- **Level 2**: Agent context files or skills explicitly instruct agents to run the full test suite and linter before presenting results, and to iterate on failures until they pass. A CLAUDE.md that says "always run `npm test` before completing" qualifies.
- **Level 3**: Level 2 is met AND agents have programmatic access to CI pipeline results (via GitHub/GitLab MCP server) AND production monitoring access (via observability MCP server) enabling post-deployment verification without human involvement.

Report in exactly this format:

**A3 — Feedback Loop Closure**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [one or two sentences citing the specific evidence]
