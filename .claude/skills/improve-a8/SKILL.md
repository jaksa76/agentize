---
name: improve-a8
description: Improve adoption criterion A8 (Planning Integration) by creating story-generation skills and MCP connections to project management tools so agents participate in planning workflows. Raises the fulfillment level by one step.
allowed-tools: Bash Read Write Edit
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Improve A8 — Planning Integration

## Current State

Examine the project to understand its current state:

- Check `.claude/skills/` for any planning-related skills (story generation, backlog decomposition, etc.).
- Check `CLAUDE.md` or `AGENTS.md` for planning-related guidance.
- Check the MCP server configuration for any connections to project management tools.
- Look for backlog or story files and assess the granularity of items.

## Instructions

**Step 1 — Determine current level:**
- Level 0: Agents play no role in planning or requirements; all planning is done by humans
- Level 1: Agents assist with planning when explicitly prompted (e.g., help break down a story on request)
- Level 2: Agents participate in story generation or decomposition as a configured step in the planning workflow
- Level 3: Agents automatically generate, refine, and decompose stories from high-level goals and participate in backlog grooming without human initiation

**Assessment guide:**
- No skills or CLAUDE.md mention story/planning tasks → Level 0
- CLAUDE.md mentions agents can help plan when asked, but no dedicated skill → Level 1
- A `generate-story` or `decompose-epic` skill exists and is part of the documented workflow → Level 2
- A scheduled workflow or MCP connection to a PM tool drives autonomous backlog grooming → Level 3

**Step 2 — Implement the improvement:**

**If current level is 0 → raise to 1:**
Add planning assistance guidance to CLAUDE.md so developers know they can ask agents to help decompose tasks:

```markdown
## Planning Assistance

Agents can assist with planning tasks when asked. Examples:

- "Break this goal into user stories: [goal description]"
- "Decompose this epic into concrete tasks: [epic description]"
- "Write acceptance criteria for this story: [story description]"
- "Suggest a task breakdown for implementing: [feature description]"

Use these prompts to accelerate planning sessions. The agent will produce a structured list that can be added to TODO.md or your backlog.
```

**If current level is 1 → raise to 2:**
Create a `generate-story` skill that makes story generation a first-class, reusable workflow step:

Create `.claude/skills/generate-story/SKILL.md`:
```markdown
---
name: generate-story
description: Generate a well-formed user story with acceptance criteria and task breakdown from a high-level goal or feature description.
allowed-tools: Bash Read Write Edit
---

# Generate Story

## Instructions

1. Read the goal or feature description from the user's prompt.
2. Read CLAUDE.md and VISION.md for project context and conventions.
3. Generate a user story in this format:

   **As a** [type of user]
   **I want** [goal]
   **So that** [benefit]

   **Acceptance Criteria:**
   - [ ] [criterion 1]
   - [ ] [criterion 2]
   - [ ] [criterion 3]

   **Tasks:**
   1. [concrete implementation task]
   2. [concrete implementation task]
   3. Write tests for [specific behavior]
   4. Update documentation for [specific section]

4. Ask the user to confirm or refine the story.
5. Once confirmed, offer to append it to TODO.md or BACKLOG.md.
```

Also create `.claude/skills/decompose-epic/SKILL.md`:
```markdown
---
name: decompose-epic
description: Decompose a high-level epic or goal into a prioritised list of user stories, each with acceptance criteria.
allowed-tools: Bash Read Write Edit
---

# Decompose Epic

## Instructions

1. Read the epic description from the user's prompt.
2. Read CLAUDE.md and VISION.md for project context.
3. Identify the smallest meaningful slices that each deliver user value independently.
4. For each story:
   - Write the user story statement (As a / I want / So that)
   - List 2–4 acceptance criteria
   - Estimate relative size: S / M / L
   - Suggest priority: Must / Should / Could
5. Present the full decomposition.
6. Ask if the user wants to append all or selected stories to TODO.md.
```

Update CLAUDE.md to reference these skills:
```markdown
## Planning Workflow

Use these skills for structured planning:

- `/generate-story` — generate a single user story with acceptance criteria and tasks from a goal
- `/decompose-epic` — break a high-level epic into prioritised user stories

After generating stories, add them to `TODO.md` (one story per line, most important first).
The agent pipeline (if configured) will implement stories in TODO.md order.
```

**If current level is 2 → raise to 3:**
Add autonomous backlog grooming via a scheduled workflow and optionally a PM tool MCP connection:

1. **Scheduled backlog refinement workflow** — Create `.github/workflows/agent-backlog-grooming.yml`:
```yaml
name: Agent Backlog Grooming
on:
  schedule:
    - cron: '0 7 * * 1'  # Every Monday morning
  workflow_dispatch:

jobs:
  groom:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
    steps:
      - uses: actions/checkout@v4

      - name: Groom backlog
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          BACKLOG=$(cat TODO.md 2>/dev/null || echo "(empty)")
          VISION=$(cat VISION.md 2>/dev/null || echo "(no vision)")
          echo "Backlog items: $(wc -l < TODO.md 2>/dev/null || echo 0)"
          
          # Agent invocation to refine backlog:
          # claude --print "Review and refine this backlog. Remove duplicates, split large items,
          # add acceptance criteria to vague items. Vision: $VISION. Backlog: $BACKLOG.
          # Output the refined TODO.md content only."
          
          echo "Configure ANTHROPIC_API_KEY secret and agent invocation"

      - name: Create PR with refined backlog
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          git diff --quiet TODO.md || (
            git checkout -b "chore/backlog-grooming-$(date +%Y%m%d)"
            git add TODO.md
            git commit -m "chore: automated backlog grooming

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
            gh pr create \
              --title "Automated backlog grooming $(date +%Y-%m-%d)" \
              --body "Weekly automated backlog refinement: removed duplicates, split large items, clarified vague tasks."
          )
```

2. **Linear MCP server** (if using Linear for project management) — Add to `.claude/settings.json`:
```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@linear/mcp-server"],
      "env": { "LINEAR_API_KEY": "${LINEAR_API_KEY}" }
    }
  }
}
```

Add to CLAUDE.md:
```markdown
## Planning Integration (Autonomous)

The agent pipeline grooming runs every Monday (`.github/workflows/agent-backlog-grooming.yml`):
- Reviews TODO.md and refines entries (splits large items, removes duplicates, clarifies vague tasks)
- Opens a PR with the refined backlog for human review

If Linear is configured (via MCP server), agents can also:
- Fetch stories from Linear into TODO.md: ask "fetch backlog from Linear"
- Update Linear issues when tasks complete: ask "mark Linear issue LIN-123 done"

Required secret: `ANTHROPIC_API_KEY`.
Optional: `LINEAR_API_KEY` for Linear integration.
```

**If already at level 3:**
Report that A8 is already at its maximum level (3) and no improvement is needed.

**Step 3 — Report:**
State what files were created or modified, the before and after level.
