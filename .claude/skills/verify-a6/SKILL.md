---
name: verify-a6
description: Verify adoption criterion A6 (Autonomous Operation) in the current project. Reports fulfillment level 0–3.
allowed-tools: Bash Read
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Verify A6 — Autonomous Operation

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | Agents are always manually started by a developer; no automated triggering |
| 1 | Agents are occasionally triggered by events (e.g., on PR creation for a specific task) but are mostly started manually |
| 2 | Agents are systematically event-triggered for common workflows (push hooks, PR events, failing monitors) |
| 3 | A continuous agent pipeline pulls from the backlog and implements stories on a schedule, with no per-story human initiation |

## Evidence to Gather

- Look at CI workflow files for scheduled (cron-based) triggers and for event triggers (push, PR, issues) that invoke an agent.
- Check workflow files for any that reference an agent (Claude, Copilot, or similar AI tools).
- Check `.claude/settings.json` for hooks that trigger agents automatically.
- Look for backlog-pulling workflow indicators — workflows that read from `TODO.md`, GitHub Issues, or a PM tool and pick tasks to implement.

## Instructions

Gather the evidence described above and determine the fulfillment level for A6.

Scoring guide:
- **Level 0**: No automated agent triggering — no scheduled workflows, no event hooks invoking agents, no CI steps that invoke an agent. Agents are always started manually by a developer typing a command.
- **Level 1**: At least one event-triggered workflow invokes an agent for a specific scenario (e.g., on PR opened, run an agent review), but most agent work is still started manually.
- **Level 2**: Agents are systematically event-triggered for common development events — push hooks that trigger agent tasks, PR event handlers that invoke agents, failing monitor alerts that start agents. Multiple trigger types are in use.
- **Level 3**: A continuous pipeline pulls from a backlog (TODO.md, GitHub Issues, Jira, Linear) on a schedule or continuously, and implements stories with no per-story human initiation. A scheduled workflow that picks and implements the next task qualifies.

Report in exactly this format:

**A6 — Autonomous Operation**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [one or two sentences citing the specific evidence]
