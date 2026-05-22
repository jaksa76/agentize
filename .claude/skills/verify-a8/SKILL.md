---
name: verify-a8
description: Verify adoption criterion A8 (Planning Integration) in the current project. Reports fulfillment level 0–3.
allowed-tools: Bash Read
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Verify A8 — Planning Integration

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | Agents play no role in planning or requirements; all planning is done by humans |
| 1 | Agents assist with planning when explicitly prompted (e.g., help break down a story on request) |
| 2 | Agents participate in story generation or decomposition as a configured step in the planning workflow |
| 3 | Agents automatically generate, refine, and decompose stories from high-level goals and participate in backlog grooming without human initiation |

## Evidence to Gather

- Check `.claude/skills/` for any skills related to story generation, backlog decomposition, or planning.
- Check the MCP server configuration (`.claude/settings.json`, `.mcp.json`) for any connections to project management tools (Jira, Linear, GitHub Issues, Trello, Notion, etc.).
- Read `CLAUDE.md` or `AGENTS.md` for planning-related workflow guidance.
- Look in CI workflow files for any scheduled workflows that generate stories or groom the backlog.
- Look for backlog or story files (`TODO.md`, `BACKLOG.md`, `stories/`) and assess how granular the items are.

## Instructions

Gather the evidence described above and determine the fulfillment level for A8.

Scoring guide:
- **Level 0**: Agents play no role in planning — no planning-related skills, no PM tool MCP servers, no planning guidance in CLAUDE.md/AGENTS.md, no evidence in git history of agent involvement in story creation or backlog management.
- **Level 1**: Agents can assist with planning when a developer explicitly asks — e.g., a general-purpose agent can be asked to "break down this epic" but there is no configured planning step or workflow. No dedicated planning skill or MCP PM integration is present; agents help ad-hoc.
- **Level 2**: A configured step exists for agent participation in planning — a dedicated story-generation or backlog-decomposition skill, a MCP server connection to Jira/Linear/GitHub Issues that agents can query and update, or a planning workflow described in CLAUDE.md/AGENTS.md that agents follow as part of the development process.
- **Level 3**: Automated planning without human initiation — a scheduled workflow that generates stories from high-level goals, an agent that automatically grooms the backlog, or a pipeline that decomposes incoming epics into tasks and creates the tickets in the PM tool without a human prompt.

Report in exactly this format:

**A8 — Planning Integration**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [one or two sentences citing the specific evidence]
