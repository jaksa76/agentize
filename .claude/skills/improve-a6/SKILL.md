---
name: improve-a6
description: Improve adoption criterion A6 (Autonomous Operation) by creating event-triggered and scheduled GitHub Actions workflows that invoke agents without human initiation. Raises the fulfillment level by one step.
allowed-tools: Bash Read Write Edit
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Improve A6 — Autonomous Operation

## Current State

### GitHub Actions workflows (event and schedule triggers)
!`ls .github/workflows/ 2>/dev/null | head -20 || echo "(no GitHub Actions workflows)"`
!`find .github/workflows/ -name "*.yml" 2>/dev/null | xargs grep -h "on:" 2>/dev/null | head -20 || echo "(no trigger configs)"`
!`find .github/workflows/ -name "*.yml" 2>/dev/null | xargs grep -l "schedule\|workflow_dispatch\|issues\|label" 2>/dev/null || echo "(no scheduled or event-triggered workflows)"`

### Evidence of agent-triggering patterns
!`find .github/workflows/ -name "*.yml" 2>/dev/null | xargs grep -h -i "claude\|agent\|implement\|llm\|ai" 2>/dev/null | head -10 || echo "(no agent invocation in CI)"`

### Cron / scheduled jobs
!`find .github/workflows/ -name "*.yml" 2>/dev/null | xargs grep -h "cron:" 2>/dev/null | head -10 || echo "(no cron schedules)"`

### Agent context — autonomous operation guidance
!`grep -i "trigger\|schedule\|event\|cron\|autonomous\|initiat\|backlog" CLAUDE.md AGENTS.md 2>/dev/null | head -10 || echo "(no autonomous operation guidance)"`

## Instructions

**Step 1 — Determine current level:**
- Level 0: Agents are always manually started by a developer; no automated triggering
- Level 1: Agents are occasionally triggered by events (e.g., on PR creation for a specific task) but are mostly started manually
- Level 2: Agents are systematically event-triggered for common workflows (push hooks, PR events, failing monitors)
- Level 3: A continuous agent pipeline pulls from the backlog and implements stories on a schedule, with no per-story human initiation

**Assessment guide:**
- No workflows that invoke agents → Level 0
- 1–2 workflows with agent invocation on narrow events → Level 1
- Workflows on `push`, `pull_request`, and `issues` events that systematically invoke agents → Level 2
- A scheduled workflow that reads from a backlog and implements stories → Level 3

**Step 2 — Implement the improvement:**

**If current level is 0 → raise to 1:**
Create a minimal event-triggered workflow: when an issue is labeled `agent-implement`, a workflow runs to implement it.

Create `.github/workflows/agent-on-label.yml`:
```yaml
name: Agent on Label
on:
  issues:
    types: [labeled]

jobs:
  implement:
    if: github.event.label.name == 'agent-implement'
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
    steps:
      - uses: actions/checkout@v4

      - name: Set up environment
        run: echo "Setting up..."  # replace with actual setup steps

      - name: Implement issue with agent
        # To use Claude Code CLI here, install it and authenticate:
        # npm install -g @anthropic-ai/claude-code
        # Export ANTHROPIC_API_KEY as a GitHub Actions secret
        run: |
          echo "Issue #${{ github.event.issue.number }}: ${{ github.event.issue.title }}"
          echo "Body: ${{ github.event.issue.body }}"
          # Implement using claude --print or your preferred invocation
          # Example: claude --print "Implement the following issue: ${{ github.event.issue.body }}"
          echo "Configure agent invocation here (see CLAUDE.md)"
```

Add `agent-implement` label instructions to CLAUDE.md:
```markdown
## Autonomous Agent Trigger

To trigger the agent to implement an issue automatically:
1. Create or open an issue describing the task
2. Add the label `agent-implement` to the issue
3. The CI pipeline will invoke an agent to implement it and open a PR
```

**If current level is 1 → raise to 2:**
Expand to systematic event-triggered workflows for common patterns:

1. **On PR open/sync — run agent review**: Create `.github/workflows/agent-pr-review.yml`:
```yaml
name: Agent PR Review
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Check diff size and quality
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          DIFF=$(git diff origin/${{ github.base_ref }}...HEAD --stat)
          echo "Changed files: $DIFF"
          # Agent invocation point: analyze diff and post review comment
          # Example: gh pr comment ${{ github.event.pull_request.number }} \
          #   --body "$(claude --print 'Review this diff: $DIFF')"
```

2. **On failing CI — agent diagnosis**: Create `.github/workflows/agent-on-failure.yml`:
```yaml
name: Agent on CI Failure
on:
  workflow_run:
    workflows: ["*"]
    types: [completed]

jobs:
  diagnose:
    if: github.event.workflow_run.conclusion == 'failure'
    runs-on: ubuntu-latest
    permissions:
      issues: write
    steps:
      - name: Create diagnosis issue
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          gh issue create \
            --title "CI failure in ${{ github.event.workflow_run.name }}" \
            --body "Run: ${{ github.event.workflow_run.html_url }}
          Branch: ${{ github.event.workflow_run.head_branch }}
          Label: agent-implement to trigger auto-diagnosis." \
            --label "ci-failure"
```

**If current level is 2 → raise to 3:**
Create a continuous scheduled pipeline that reads from TODO.md or GitHub issues and implements the next story:

Create `.github/workflows/agent-pipeline.yml`:
```yaml
name: Agent Continuous Pipeline
on:
  schedule:
    - cron: '0 */4 * * 1-5'  # Every 4 hours on weekdays
  workflow_dispatch:
    inputs:
      max_tasks:
        description: 'Maximum number of tasks to implement'
        default: '1'
        type: string

jobs:
  implement-next:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
    steps:
      - uses: actions/checkout@v4

      - name: Find next task
        id: next-task
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          # Option A: Read from TODO.md
          NEXT=$(head -1 TODO.md 2>/dev/null || echo "")
          # Option B: Read from GitHub issues with a label
          # NEXT=$(gh issue list --label "backlog" --limit 1 --json number,title --jq '.[0].title' 2>/dev/null || echo "")
          echo "task=$NEXT" >> $GITHUB_OUTPUT
          echo "Next task: $NEXT"

      - name: Implement task with agent
        if: steps.next-task.outputs.task != ''
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          TASK="${{ steps.next-task.outputs.task }}"
          echo "Implementing: $TASK"
          # Install Claude Code CLI and invoke:
          # npm install -g @anthropic-ai/claude-code
          # claude --print "Implement this task: $TASK. Run tests. Create a PR."
          echo "Configure agent invocation here"

      - name: Skip if no tasks
        if: steps.next-task.outputs.task == ''
        run: echo "No tasks found in backlog — pipeline idle."
```

Update CLAUDE.md:
```markdown
## Continuous Agent Pipeline

The agent pipeline runs every 4 hours on weekdays (`.github/workflows/agent-pipeline.yml`).
It reads the top task from TODO.md and implements it autonomously.

To feed the pipeline:
1. Add tasks to the top of TODO.md, or
2. Create GitHub issues with the `backlog` label

To trigger manually: GitHub → Actions → "Agent Continuous Pipeline" → Run workflow.

Required secret: `ANTHROPIC_API_KEY` (set in GitHub repo settings → Secrets).
```

**If already at level 3:**
Report that A6 is already at its maximum level (3) and no improvement is needed.

**Step 3 — Report:**
State what files were created or modified, the before and after level.
