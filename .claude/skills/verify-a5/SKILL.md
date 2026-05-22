---
name: verify-a5
description: Verify adoption criterion A5 (Workflow Integration) in the current project. Reports fulfillment level 0–3.
allowed-tools: Bash Read
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Verify A5 — Workflow Integration

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | Agents are used in isolation; all handoffs (PRs, reviews, CI, deployments) are managed by humans |
| 1 | Agents assist with individual tasks but humans handle all handoffs; agent output is manually incorporated |
| 2 | Agents create pull requests with generated descriptions; agents observe CI results as part of their workflow |
| 3 | Agents are fully embedded: create PRs, post review comments, monitor CI, trigger and observe deployments |

## Evidence to Gather

- Check `CLAUDE.md`, `AGENTS.md`, and skill files in `.claude/skills/` for instructions to create pull requests.
- Look at CI workflow files for automated PR-creation steps or review automation.
- Check recent merge commit history for signs of agent-created PRs.
- Check the MCP server configuration for CI pipeline or GitHub/GitLab servers that would allow agents to observe pipeline results.
- Look for workflow steps where agents trigger or observe deployments.

## Instructions

Gather the evidence described above and determine the fulfillment level for A5.

Scoring guide:
- **Level 0**: Agents are used locally in isolation — no PR creation in skills or CLAUDE.md, no agent-authored merge patterns in git history. All handoffs (PRs, reviews, CI, deployments) are human-managed.
- **Level 1**: Agents assist with tasks but a human manually creates the PR or incorporates the output. CLAUDE.md may mention git push but does not instruct agents to create PRs. No automated PR-creation steps.
- **Level 2**: Skills or CLAUDE.md instruct agents to create PRs (e.g., `gh pr create`), and/or CI MCP server access allows agents to observe pipeline results. Both conditions strengthen the evidence but either alone may qualify.
- **Level 3**: All of: agents create PRs, agents post review comments or trigger review workflows, agents monitor CI results, AND agents trigger or observe deployments. Evidence from multiple workflow files and skill definitions is expected.

Report in exactly this format:

**A5 — Workflow Integration**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [one or two sentences citing the specific evidence]
