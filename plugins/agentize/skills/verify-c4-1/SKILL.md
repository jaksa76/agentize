---
name: verify-c4-1
description: Verify readiness criterion C4.1 (Requirements Access) in the current project. Reports fulfillment level 0–3.
allowed-tools: Bash Read
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Verify C4.1 — Requirements Access

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | No documented requirements |
| 1 | Product vision and goals documented |
| 2 | User stories or acceptance criteria accessible |
| 3 | Full programmatic access via MCP server or API |

## Evidence to Gather

- Look for vision or requirements files at the project root (VISION.md, REQUIREMENTS.md, GOALS.md, etc.) and read them to assess depth.
- Check a `docs/` directory for requirement or specification documents.
- Look for a `stories/`, `features/`, `backlog/`, or `specs/` directory with user stories or acceptance criteria.
- Check the MCP server configuration for any connections to project management tools that would provide programmatic requirements access.
- Read the README for a product purpose or overview section.

## Instructions

Gather the evidence described above and determine the fulfillment level for C4.1.

Scoring guide:
- **Level 0**: No requirements documentation exists — no README description of the product's purpose, no vision document, no user stories anywhere in the repo.
- **Level 1**: Product vision and goals are documented — a VISION.md, a README "About" or "Overview" section, or a goals document that explains what the product does and why it exists. No structured user stories required.
- **Level 2**: User stories or acceptance criteria are accessible within the repo or via linked tooling — e.g., a `stories/` directory, a `backlog.md`, structured specs, or clearly linked GitHub/Jira issues with acceptance criteria.
- **Level 3**: Programmatic access exists — an MCP server or API endpoint exposes requirements in a structured, queryable form that an agent can call without reading flat files.

Report in exactly this format:

**C4.1 — Requirements Access**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [one or two sentences citing the specific evidence]
