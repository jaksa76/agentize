---
name: improve-c4-1
description: Improve readiness criterion C4.1 (Requirements Access) in the current project by generating vision and user story documentation. Raises the fulfillment level by one step.
allowed-tools: Bash Read Write Edit
---

# Improve C4.1 — Requirements Access

## Current State

### Existing requirements docs
!`ls VISION.md REQUIREMENTS.md requirements.md GOALS.md 2>/dev/null || echo "(none at root)"`
!`cat VISION.md 2>/dev/null || cat REQUIREMENTS.md 2>/dev/null || echo "(no vision/requirements file)"`

### Stories / backlog directory
!`ls -d stories/ features/ user-stories/ backlog/ 2>/dev/null || echo "(no stories directory)"`
!`ls stories/ features/ user-stories/ backlog/ 2>/dev/null | head -20 || echo "(no files)"`

### MCP server config
!`cat .claude/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); mcp=d.get('mcpServers',{}); print('MCP:', list(mcp.keys()) if mcp else 'none')" 2>/dev/null || echo "(no MCP servers)"`

### README (for inferring purpose and features)
!`cat README.md 2>/dev/null | head -100 || echo "(no README)"`

### Source code entry points (for inferring features)
!`head -50 src/index.ts src/index.js src/main.py app/main.py main.go cmd/main.go 2>/dev/null || find . -maxdepth 3 -name "main.*" -o -name "index.*" -o -name "app.*" 2>/dev/null | grep -v node_modules | head -10 || echo "(no obvious entry points)"`

### Route / endpoint detection (reveals features)
!`find . -maxdepth 5 \( -name "*.routes.*" -o -name "*router*" -o -name "*controller*" \) 2>/dev/null | grep -v node_modules | head -10 || echo "(no route files)"`
!`grep -r "app\.\(get\|post\|put\|delete\|patch\)\|router\.\(get\|post\)" --include="*.js" --include="*.ts" -h . 2>/dev/null | grep -v node_modules | head -20 || echo "(no route definitions found)"`

## Instructions

**Step 1 — Determine current level:**
- Level 0: No documented requirements, no vision
- Level 1: Product vision or goals documented
- Level 2: User stories or acceptance criteria accessible
- Level 3: Programmatic access via MCP server or API (cannot be automated — requires external infrastructure setup)

**Step 2 — Read the project thoroughly before writing:**
Read the README, source entry points, and route definitions to understand what the system does and who uses it.

**Step 3 — Implement the improvement:**

**If current level is 0 → raise to 1:**
Create `VISION.md` at the project root. Infer the product's purpose, users, and goals from the README and codebase. Write:
- **Problem**: What problem does this solve?
- **Users**: Who uses this system?
- **Goals**: What are the 3–5 key product goals?
- **Non-goals**: What is explicitly out of scope?
- **Success metrics**: How would we know it's working?

Base the content on actual evidence from the code — do not write generic placeholders.

**If current level is 1 → raise to 2:**
Create a `stories/` directory and populate it with user stories inferred from the codebase (routes, controllers, features). Create:
- `stories/README.md` — explanation of the stories directory and story format
- One `.md` file per major feature area, each containing 3–5 user stories in the format:
  ```
  ## [Feature Name]
  
  **As a** [user type],
  **I want to** [action],
  **so that** [benefit].
  
  **Acceptance criteria:**
  - [ ] [specific, testable criterion]
  - [ ] [specific, testable criterion]
  ```

Infer features from route definitions, controller names, and existing code. Aim for 10–20 stories total covering the main functionality.

**If current level is 2 → raise to 3:**
Level 3 requires programmatic access via MCP server or API, which requires external infrastructure (a running MCP server connected to a project management tool). This cannot be fully automated.

Explain what would be needed: configure an MCP server connection to GitHub Issues, Linear, Jira, or Notion in `.claude/settings.json`, and ensure stories are importable from that tool.

**If already at level 3:**
Report that C4.1 is already at its maximum level (3) and no improvement is needed.

**Step 4 — Report:**
State what file(s) were created or modified, the before and after level.
