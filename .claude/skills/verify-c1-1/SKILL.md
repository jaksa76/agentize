---
name: verify-c1-1
description: Verify readiness criterion C1.1 (Codebase Accessibility) in the current project. Reports fulfillment level 0–2.
allowed-tools: Bash Read
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Verify C1.1 — Codebase Accessibility

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | Code split across unlinked repos with no entry point |
| 1 | All code reachable from a single root with a basic README |
| 2 | Comprehensive entry-point guide (CLAUDE.md or equivalent) with conventions and navigation hints |

## Evidence

### Root structure
!`ls -la 2>/dev/null | head -30`

### README presence and content
!`head -40 README.md 2>/dev/null || echo "(no README.md found)"`

### Agent context file (CLAUDE.md / AGENTS.md)
!`ls CLAUDE.md AGENTS.md .claude/CLAUDE.md 2>/dev/null || echo "(none found)"`

### Agent context file content (first 60 lines)
!`head -60 CLAUDE.md 2>/dev/null || head -60 AGENTS.md 2>/dev/null || echo "(no agent context file)"`

### Multi-repo indicators
!`cat .gitmodules 2>/dev/null || echo "(no .gitmodules)"`

## Instructions

Analyse the evidence above and determine the fulfillment level for C1.1.

Scoring guide:
- **Level 0**: No single entry point; code is split across unlinked locations with no README to orient a newcomer.
- **Level 1**: A README exists at the root and all relevant code is reachable from there. The README describes the project's purpose but does not provide agent-specific conventions or navigation guidance.
- **Level 2**: A CLAUDE.md, AGENTS.md, or equivalent file exists and contains meaningful project-specific guidance: key commands, coding conventions, architecture overview, or navigation hints beyond what a basic README provides.

Report in exactly this format:

**C1.1 — Codebase Accessibility**
- **Level**: [0 / 1 / 2]
- **Rationale**: [one or two sentences citing the specific evidence]
