---
name: verify-c4-1
description: Verify readiness criterion C4.1 (Requirements Access) in the current project. Reports fulfillment level 0–3.
allowed-tools: Bash Read
---

# Verify C4.1 — Requirements Access

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | No documented requirements |
| 1 | Product vision and goals documented |
| 2 | User stories or acceptance criteria accessible |
| 3 | Full programmatic access via MCP server or API |

## Evidence

### Vision / requirements files at root
!`ls VISION.md REQUIREMENTS.md requirements.md GOALS.md goals.md PRODUCT.md 2>/dev/null || echo "(none found)"`
!`head -40 VISION.md 2>/dev/null || echo "(no VISION.md)"`

### Requirements in docs/
!`find docs/ -maxdepth 3 \( -iname "*requirement*" -o -iname "*vision*" -o -iname "*story*" -o -iname "*spec*" -o -iname "*acceptance*" -o -iname "*backlog*" \) 2>/dev/null | head -20 || echo "(none found in docs/)"`

### Stories / features directory
!`ls -d stories/ features/ user-stories/ backlog/ specs/ 2>/dev/null || echo "(no dedicated stories/features directory)"`
!`ls stories/ features/ user-stories/ backlog/ 2>/dev/null | head -20 || true`

### MCP server configuration (programmatic access)
!`cat .mcp.json 2>/dev/null || cat mcp.json 2>/dev/null || echo "(no .mcp.json / mcp.json)"`
!`cat .claude/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); mcp=d.get('mcpServers',{}); print('MCP servers:', list(mcp.keys()) if mcp else 'none')" 2>/dev/null || echo "(no .claude/settings.json or no MCP servers configured)"`

### README product/purpose section
!`grep -A10 -i "about\|overview\|purpose\|what is\|why\|goals\|features" README.md 2>/dev/null | head -30 || echo "(no purpose/overview section in README)"`

## Instructions

Analyse the evidence above and determine the fulfillment level for C4.1.

Scoring guide:
- **Level 0**: No requirements documentation exists — no README description of the product's purpose, no vision document, no user stories anywhere in the repo.
- **Level 1**: Product vision and goals are documented — a VISION.md, a README "About" or "Overview" section, or a goals document that explains what the product does and why it exists. No structured user stories required.
- **Level 2**: User stories or acceptance criteria are accessible within the repo or via linked tooling — e.g., a `stories/` directory, a `backlog.md`, structured specs, or clearly linked GitHub/Jira issues with acceptance criteria.
- **Level 3**: Programmatic access exists — an MCP server or API endpoint exposes requirements in a structured, queryable form that an agent can call without reading flat files.

Report in exactly this format:

**C4.1 — Requirements Access**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [one or two sentences citing the specific evidence]
