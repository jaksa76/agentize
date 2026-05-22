---
name: verify-a2
description: Verify adoption criterion A2 (Agent-Authored Contributions) in the current project. Reports fulfillment level 0–3.
allowed-tools: Bash Read
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Verify A2 — Agent-Authored Contributions

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | No agent-authored code in git history; all commits are purely human-written |
| 1 | Occasional co-authored commits; agents contributed to fewer than 25% of recent changes |
| 2 | Regular agent contributions; agents co-authored 25–75% of recent changes |
| 3 | Agents autonomously create pull requests; more than 75% of implementation work has significant agent involvement |

"Recent" = last 90 days or last 50 commits, whichever covers more changes.

## Evidence to Gather

- Look at recent git history (last 90 days or last 50 commits) and count commits with agent co-authorship markers — lines containing "Co-Authored-By", references to Claude/Copilot/Anthropic, the 🤖 emoji, or "Generated with".
- Calculate the ratio of agent-co-authored commits to total recent commits.
- Check merge commits and CI workflow files for signs of automated PR creation by an agent.

## Instructions

Gather the evidence described above and determine the fulfillment level for A2.

Key calculation: divide agent-co-authored commit count by total recent commit count to get the percentage.

Scoring guide:
- **Level 0**: Zero agent-authored commits in git history — no co-authorship markers, no bot commits, no agent-attributed changes.
- **Level 1**: Agent co-authorship markers exist in fewer than 25% of recent commits. Occasional use, not yet habitual.
- **Level 2**: Agent co-authorship markers exist in 25–75% of recent commits. Habitual use across a significant portion of implementation work.
- **Level 3**: Agent co-authorship markers exist in more than 75% of recent commits, OR evidence of autonomous PR creation (bot-authored PRs, agent-triggering workflows that open PRs).

Report in exactly this format:

**A2 — Agent-Authored Contributions**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [one or two sentences citing the specific evidence, including the calculated percentage if possible]
