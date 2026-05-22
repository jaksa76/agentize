---
name: verify-a8
description: Verify adoption criterion A8 (Planning Integration) in the current project. Reports fulfillment level 0–3.
allowed-tools: Bash Read
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Verify A8 — Planning Integration

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | Agents play no role in planning or requirements; all planning is done by humans |
| 1 | Agents assist with planning when explicitly prompted (e.g., help break down a story on request) |
| 2 | Agents participate in story generation or decomposition as a configured step in the planning workflow |
| 3 | Agents automatically generate, refine, and decompose stories from high-level goals and participate in backlog grooming without human initiation |

## Evidence

### Skills for planning / story generation
!`find .claude/skills/ -name "SKILL.md" 2>/dev/null | xargs grep -l -i "story\|planning\|backlog\|decompose\|grooming\|epic\|requirements\|generate.*task\|break.*down" 2>/dev/null | head -10 || echo "(no planning-related skills found)"`
!`find .claude/skills/ -name "SKILL.md" 2>/dev/null | xargs grep -h -i "story\|planning\|backlog\|decompose\|generate.*task" 2>/dev/null | head -20 || echo "(no planning content in skills)"`

### MCP servers connected to project management tools
!`cat .claude/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); mcp=d.get('mcpServers',{}); pm=[k for k in mcp if any(x in k.lower() for x in ['jira','linear','github','trello','notion','asana','monday','clickup','shortcut','basecamp'])]; print('PM-related MCP servers:', pm if pm else 'none')" 2>/dev/null || echo "(no PM MCP servers in settings)"`
!`cat .mcp.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); servers=list(d.get('mcpServers',{}).keys()); print('All MCP servers:', servers)" 2>/dev/null || echo "(no .mcp.json)"`

### AGENTS.md / CLAUDE.md — planning workflow guidance
!`grep -i "story\|planning\|backlog\|decompose\|grooming\|epic\|requirements\|sprint\|ticket\|issue" CLAUDE.md AGENTS.md 2>/dev/null | head -20 || echo "(no planning guidance in agent context files)"`

### Scheduled workflows for automated story generation / backlog grooming
!`find .github/workflows/ -name "*.yml" -o -name "*.yaml" 2>/dev/null | xargs grep -l -i "story\|backlog\|grooming\|planning\|decompose\|epic" 2>/dev/null | head -5 || echo "(no planning-related workflows)"`

### Backlog / story files
!`ls TODO.md BACKLOG.md stories/ features/ backlog/ 2>/dev/null || echo "(no backlog/story files or directories)"`
!`head -20 TODO.md 2>/dev/null || head -20 BACKLOG.md 2>/dev/null || echo "(no backlog content)"`
!`ls stories/ 2>/dev/null | head -10 || echo "(no stories directory)"`

### Evidence of agent-generated stories in git history
!`git log --since="90 days ago" --format="%s %b" 2>/dev/null | grep -i "story\|user story\|generate.*task\|decompose\|backlog\|planning" | head -10 || echo "(no planning-related commits in recent history)"`

## Instructions

Analyse the evidence above and determine the fulfillment level for A8.

Scoring guide:
- **Level 0**: Agents play no role in planning — no planning-related skills, no PM tool MCP servers, no planning guidance in CLAUDE.md/AGENTS.md, no evidence in git history of agent involvement in story creation or backlog management.
- **Level 1**: Agents can assist with planning when a developer explicitly asks — e.g., a general-purpose agent can be asked to "break down this epic" but there is no configured planning step or workflow. No dedicated planning skill or MCP PM integration is present; agents help ad-hoc.
- **Level 2**: A configured step exists for agent participation in planning — a dedicated story-generation or backlog-decomposition skill, a MCP server connection to Jira/Linear/GitHub Issues that agents can query and update, or a planning workflow described in CLAUDE.md/AGENTS.md that agents follow as part of the development process.
- **Level 3**: Automated planning without human initiation — a scheduled workflow that generates stories from high-level goals, an agent that automatically grooms the backlog, or a pipeline that decomposes incoming epics into tasks and creates the tickets in the PM tool without a human prompt.

Report in exactly this format:

**A8 — Planning Integration**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [one or two sentences citing the specific evidence]
