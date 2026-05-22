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

## Evidence

### Scheduled workflows (cron-based agent triggering)
!`grep -r -A3 "schedule:\|cron:" .github/workflows/ 2>/dev/null | head -30 || echo "(no scheduled workflows found)"`
!`find .github/workflows/ -name "*.yml" -o -name "*.yaml" 2>/dev/null | xargs grep -l "schedule" 2>/dev/null | head -10 || echo "(no files with schedule trigger)"`

### Event-triggered workflows that invoke agents
!`find .github/workflows/ -name "*.yml" -o -name "*.yaml" 2>/dev/null | xargs grep -l -i "claude\|copilot\|agent\|openai\|anthropic" 2>/dev/null | head -10 || echo "(no agent-invoking workflow files)"`
!`grep -r -i "claude\|copilot\|openai\|anthropic\|agent" .github/workflows/ 2>/dev/null | head -20 || echo "(no agent invocations in workflows)"`

### Workflow triggers (push, PR, issues, schedule)
!`grep -r -A5 "^on:" .github/workflows/ 2>/dev/null | head -60 || echo "(no workflow trigger configs)"`

### Claude Code / agent cron or loop configuration
!`cat .claude/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); hooks=d.get('hooks',{}); print('Hooks:', list(hooks.keys()) if hooks else 'none')" 2>/dev/null || echo "(no settings)"`
!`find . -maxdepth 3 \( -name "*.cron" -o -name "crontab" -o -name "*.timer" \) 2>/dev/null | head -10 || echo "(no cron files)"`

### Backlog-pulling pipeline evidence
!`ls TODO.md BACKLOG.md 2>/dev/null && head -5 TODO.md 2>/dev/null || echo "(no TODO/BACKLOG file)"`
!`find .github/workflows/ -name "*.yml" -o -name "*.yaml" 2>/dev/null | xargs grep -l -i "backlog\|todo\|pick.*task\|next.*task\|queue" 2>/dev/null | head -5 || echo "(no backlog-pulling workflow)"`

### Issue/PR event triggers
!`grep -r "on:.*issues\|on:.*pull_request\|issues:\|pull_request:" .github/workflows/ 2>/dev/null | head -15 || echo "(no issue/PR event triggers)"`

## Instructions

Analyse the evidence above and determine the fulfillment level for A6.

Scoring guide:
- **Level 0**: No automated agent triggering — no scheduled workflows, no event hooks invoking agents, no CI steps that invoke an agent. Agents are always started manually by a developer typing a command.
- **Level 1**: At least one event-triggered workflow invokes an agent for a specific scenario (e.g., on PR opened, run an agent review), but most agent work is still started manually.
- **Level 2**: Agents are systematically event-triggered for common development events — push hooks that trigger agent tasks, PR event handlers that invoke agents, failing monitor alerts that start agents. Multiple trigger types are in use.
- **Level 3**: A continuous pipeline pulls from a backlog (TODO.md, GitHub Issues, Jira, Linear) on a schedule or continuously, and implements stories with no per-story human initiation. A scheduled workflow that picks and implements the next task qualifies.

Report in exactly this format:

**A6 — Autonomous Operation**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [one or two sentences citing the specific evidence]
