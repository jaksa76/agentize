---
name: improve-a3
description: Improve adoption criterion A3 (Feedback Loop Closure) by adding verification guidance to agent context files and configuring CI/monitoring MCP access. Raises the fulfillment level by one step.
allowed-tools: Bash Read Write Edit
---

# Improve A3 — Feedback Loop Closure

## Current State

### Agent context and verification guidance
!`cat CLAUDE.md 2>/dev/null || cat AGENTS.md 2>/dev/null || echo "(no agent context file)"`

### Skills with verification steps
!`find .claude/skills/ -name "SKILL.md" 2>/dev/null | xargs grep -h -i "run.*test\|npm test\|pytest\|go test\|lint\|build\|verify" 2>/dev/null | head -15 || echo "(no test commands in skills)"`

### Test commands available
!`cat package.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); s=d.get('scripts',{}); print({k:v for k,v in s.items() if any(x in k for x in ['test','lint','build','typecheck','check'])})" 2>/dev/null || true`
!`grep -i "^test\b\|^lint\b\|^build\b\|^check\b" Makefile 2>/dev/null | head -10 || echo "(no Makefile quality targets)"`

### CI / monitoring MCP access
!`cat .claude/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); mcp=d.get('mcpServers',{}); print('MCP servers:', list(mcp.keys()) if mcp else 'none')" 2>/dev/null || echo "(no MCP servers)"`

### Hooks configured
!`cat .claude/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); hooks=d.get('hooks',{}); print('Hooks:', list(hooks.keys()) if hooks else 'none')" 2>/dev/null || echo "(no hooks)"`

## Instructions

**Step 1 — Determine current level:**
- Level 0: No verification guidance — agents hand output directly to humans
- Level 1: Basic checks only (build/compile) — no full test suite instruction
- Level 2: CLAUDE.md/AGENTS.md or skills explicitly instruct agents to run full test suite, iterate on failures, present only passing results
- Level 3: Level 2 PLUS CI pipeline access AND production monitoring access via MCP

**Step 2 — Implement the improvement:**

**If current level is 0 → raise to 1:**
Add a verification section to CLAUDE.md (create if absent) with at minimum the build command:

```markdown
## Before Submitting Changes

Always verify your changes compile/build before presenting them:
- Build: `[detected build command]`
- If the build fails, fix the errors before proceeding.
```

Detect the build command from the evidence above (e.g., `npm run build`, `go build ./...`, `./mvnw package -DskipTests`, `cargo build`).

**If current level is 1 → raise to 2:**
Expand the verification section in CLAUDE.md to require full test suite execution with iteration:

```markdown
## Before Submitting Changes

Run all of the following and fix any failures before creating a PR or presenting results:

1. **Build**: `[build command]`
2. **Lint**: `[lint command]`
3. **Type check**: `[typecheck command]` (if applicable)
4. **Tests**: `[test command]`

If tests fail:
- Read the failure output carefully
- Fix the root cause (not just the symptom)
- Re-run the full suite to confirm the fix does not break other tests
- Only present your work when the full suite passes

Do NOT skip this step or present results with failing tests.
```

Fill in the actual commands detected from package.json scripts or Makefile. Also update any existing skills to include these verification steps before their "Report" section.

**If current level is 2 → raise to 3:**
Add MCP server access for CI pipeline and production monitoring:

1. **CI pipeline access** — add a GitHub MCP server if not present:
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}" }
    }
  }
}
```

2. **Extend CLAUDE.md** with post-PR verification guidance:
```markdown
## Post-PR Verification

After creating a PR:
1. Check CI status using the GitHub MCP server: get workflow runs for the PR branch
2. If CI fails, read the failure logs and fix the issue
3. Re-push and confirm CI passes before requesting review
```

3. If the project has a monitoring tool (Sentry, Datadog, etc.), also add that MCP server and document how to check for post-deployment errors.

**If already at level 3:**
Report that A3 is already at its maximum level (3) and no improvement is needed.

**Step 3 — Report:**
State what files were created or modified, the before and after level.
