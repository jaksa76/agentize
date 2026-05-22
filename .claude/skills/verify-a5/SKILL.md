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

## Evidence

### PR creation tooling / agent-created PR patterns
!`git log --since="90 days ago" --merges --format="%s" 2>/dev/null | head -20 || echo "(no recent merge commits)"`
!`ls .github/PULL_REQUEST_TEMPLATE.md .github/pull_request_template.md 2>/dev/null || echo "(no PR template)"`
!`cat .github/PULL_REQUEST_TEMPLATE.md 2>/dev/null | head -20 || cat .github/pull_request_template.md 2>/dev/null | head -20 || echo "(no PR template content)"`

### Workflows that create PRs automatically
!`find .github/workflows/ -name "*.yml" -o -name "*.yaml" 2>/dev/null | xargs grep -l "pull_request\|create.*pr\|gh pr create\|hub pull-request" 2>/dev/null | head -5 || echo "(no PR-creating workflows found)"`
!`grep -r "gh pr create\|hub pull-request\|create-pull-request\|peter-evans/create-pull-request" .github/workflows/ 2>/dev/null | head -10 || echo "(no automated PR creation steps)"`

### CLAUDE.md / AGENTS.md — instructions to create PRs
!`grep -i "pull request\|PR\|gh pr\|create.*branch\|push.*branch" CLAUDE.md AGENTS.md 2>/dev/null | head -15 || echo "(no PR creation guidance in agent context files)"`

### Skills with PR creation steps
!`find .claude/skills/ -name "SKILL.md" 2>/dev/null | xargs grep -l -i "pull request\|gh pr create\|push" 2>/dev/null | head -10 || echo "(no skills with PR creation steps)"`
!`find .claude/skills/ -name "SKILL.md" 2>/dev/null | xargs grep -h -i "git push\|gh pr create\|pull request" 2>/dev/null | head -10 || echo "(no PR-related commands in skills)"`

### CI observation — MCP or API access
!`cat .claude/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); mcp=d.get('mcpServers',{}); ci=[k for k in mcp if any(x in k.lower() for x in ['github','gitlab','ci','pipeline'])]; print('CI MCP servers:', ci if ci else 'none')" 2>/dev/null || echo "(no CI MCP servers)"`

### Review automation (agent posts review comments)
!`grep -r "review\|comment\|gh api.*reviews\|pull_request_review" .github/workflows/ 2>/dev/null | head -10 || echo "(no review automation in workflows)"`

### Deployment triggering by agents
!`grep -r "deploy\|kubectl\|helm\|terraform apply\|release" .github/workflows/ 2>/dev/null | grep -i "agent\|claude\|workflow_dispatch" | head -10 || echo "(no agent-triggered deployment steps)"`

## Instructions

Analyse the evidence above and determine the fulfillment level for A5.

Scoring guide:
- **Level 0**: Agents are used locally in isolation — no PR creation in skills or CLAUDE.md, no agent-authored merge patterns in git history. All handoffs (PRs, reviews, CI, deployments) are human-managed.
- **Level 1**: Agents assist with tasks but a human manually creates the PR or incorporates the output. CLAUDE.md may mention git push but does not instruct agents to create PRs. No automated PR-creation steps.
- **Level 2**: Skills or CLAUDE.md instruct agents to create PRs (e.g., `gh pr create`), and/or CI MCP server access allows agents to observe pipeline results. Both conditions strengthen the evidence but either alone may qualify.
- **Level 3**: All of: agents create PRs, agents post review comments or trigger review workflows, agents monitor CI results, AND agents trigger or observe deployments. Evidence from multiple workflow files and skill definitions is expected.

Report in exactly this format:

**A5 — Workflow Integration**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [one or two sentences citing the specific evidence]
