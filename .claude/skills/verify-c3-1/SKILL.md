---
name: verify-c3-1
description: Verify readiness criterion C3.1 (Architecture Depth) in the current project. Reports fulfillment level 0–3.
allowed-tools: Bash Read
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Verify C3.1 — Architecture Depth

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | No in-repo architecture docs |
| 1 | System context documented (users, external systems) |
| 2 | Container/service level documented |
| 3 | Component level documented + critical flows documented |

All documentation must live in-repo or be accessible via MCP to count.

## Evidence to Gather

- Look for architecture documentation files at the project root and in a `docs/` directory.
- Look for diagram files (PlantUML, C4, draw.io, Mermaid, or similar) anywhere in the project.
- Check the README for architecture keywords or sections.
- Read any primary architecture document to assess its depth — does it cover system context, containers/services, components, or critical flows?

## Instructions

Gather the evidence described above and determine the fulfillment level for C3.1.

Scoring guide:
- **Level 0**: No architecture documentation exists in the repo — no dedicated architecture file, no architecture section in the README, no diagrams.
- **Level 1**: System-context level documentation exists: who the users are, what external systems interact with this project, and the high-level purpose. A README paragraph or a simple context diagram qualifies.
- **Level 2**: Container or service-level documentation exists — shows the major services, processes, or containers that make up the system and how they interact (e.g., a C4 container diagram, a services overview, API boundary docs).
- **Level 3**: Component-level documentation exists (internal structure of individual services/containers) AND critical flows or sequence diagrams are documented (e.g., key request paths, authentication flow, data pipeline).

Report in exactly this format:

**C3.1 — Architecture Depth**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [one or two sentences citing the specific evidence]
