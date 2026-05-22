---
name: verify-a1
description: Verify adoption criterion A1 (Agent Context Availability) in the current project. Reports fulfillment level 0–3.
allowed-tools: Bash Read
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Verify A1 — Agent Context Availability

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | No agent context files; agents must infer everything from raw code |
| 1 | Basic README or project description exists; agents have a starting point but no conventions or navigation guidance |
| 2 | CLAUDE.md or AGENTS.md provides project-specific guidance: conventions, architecture overview, key commands |
| 3 | Comprehensive agent context including architecture docs structured for agent consumption AND MCP servers exposing project knowledge (requirements, diagrams, runbooks) |

## Evidence to Gather

- Check for agent context files (`CLAUDE.md`, `AGENTS.md`, or equivalent) at the project root and in `.claude/`. Read their content and assess depth — look for sections covering conventions, key commands, architecture overview, and navigation hints.
- Check for a `README.md` and assess whether it gives an agent a meaningful starting point.
- Check the MCP server configuration (`.claude/settings.json`, `.mcp.json`) for any servers that expose project knowledge such as requirements, diagrams, or runbooks.
- Look for a `docs/` directory or architecture documentation files that are structured for agent consumption.

## Instructions

Gather the evidence described above and determine the fulfillment level for A1.

Scoring guide:
- **Level 0**: No CLAUDE.md, AGENTS.md, or equivalent exists. No README, or a README so minimal it provides no meaningful starting point.
- **Level 1**: A README or basic project description exists that tells an agent what the project is and how to navigate it at a high level. No project-specific conventions, key commands, or architecture guidance is present.
- **Level 2**: A CLAUDE.md or AGENTS.md (or equivalent) exists with substantive project-specific content: coding conventions, key commands (how to build, test, run), an architecture overview, or navigation hints. The file must go meaningfully beyond a README.
- **Level 3**: Level 2 is met AND architecture documentation is structured for agent consumption (e.g., machine-readable or well-organised in-repo docs) AND at least one MCP server exposes project knowledge (requirements, diagrams, runbooks) programmatically.

Report in exactly this format:

**A1 — Agent Context Availability**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [one or two sentences citing the specific evidence]
