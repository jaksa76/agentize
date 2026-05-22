---
name: verify-a3
description: Verify adoption criterion A3 (Feedback Loop Closure) in the current project. Reports fulfillment level 0–3.
allowed-tools: Bash Read
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Verify A3 — Feedback Loop Closure

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | Agents produce output and hand it directly to the human; no self-verification |
| 1 | Agents run basic checks (compilation, syntax) but do not iterate on failures before presenting results |
| 2 | Agents run the full test suite and linter, iterate on failures, and present only passing results to the human |
| 3 | Agents have access to CI pipeline results, production monitoring, and MCP-connected tool outputs; verification is fully automated and includes post-deployment checks |

## Evidence

### AGENTS.md / CLAUDE.md — documented agent verification workflow
!`grep -i "test\|build\|verify\|check\|lint\|run\|before.*submit\|before.*pr\|validate" CLAUDE.md AGENTS.md 2>/dev/null | head -20 || echo "(no verification guidance in agent context files)"`

### Skills with verification steps
!`find .claude/skills/ -name "SKILL.md" 2>/dev/null | xargs grep -l -i "test\|lint\|build\|verify\|check" 2>/dev/null | head -10 || echo "(no skills with verification steps found)"`
!`find .claude/skills/ -name "SKILL.md" 2>/dev/null | xargs grep -h -i "run.*test\|npm test\|pytest\|go test\|cargo test\|lint\|build" 2>/dev/null | head -15 || echo "(no test/lint commands in skills)"`

### Test suite presence (agents need tests to run)
!`find . -maxdepth 5 -type d \( -name "test" -o -name "tests" -o -name "__tests__" -o -name "spec" \) 2>/dev/null | grep -v node_modules | head -10 || echo "(no test directories)"`

### CI pipeline access for agents (MCP or API)
!`cat .claude/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); mcp=d.get('mcpServers',{}); ci=[k for k in mcp if any(x in k.lower() for x in ['github','gitlab','ci','pipeline','jenkins'])]; print('CI-related MCP servers:', ci if ci else 'none')" 2>/dev/null || echo "(no CI MCP servers)"`

### Production monitoring access for agents
!`cat .claude/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); mcp=d.get('mcpServers',{}); obs=[k for k in mcp if any(x in k.lower() for x in ['grafana','datadog','sentry','cloudwatch','log','metric','monitor','newrelic'])]; print('Monitoring MCP servers:', obs if obs else 'none')" 2>/dev/null || echo "(no monitoring MCP servers)"`

### Hooks configured to run verification automatically
!`cat .claude/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); hooks=d.get('hooks',{}); print('Hooks configured:', list(hooks.keys()) if hooks else 'none')" 2>/dev/null || echo "(no hooks in settings)"`

### CI workflows that agents can read results from
!`ls .github/workflows/ 2>/dev/null && ls .github/workflows/ | head -10 || echo "(no GitHub Actions workflows)"`

## Instructions

Analyse the evidence above and determine the fulfillment level for A3.

This criterion measures the degree to which agents close their own feedback loops before handing work to a human. Look for evidence that the workflow (skills, CLAUDE.md, AGENTS.md) instructs or enables agents to verify their own output.

Scoring guide:
- **Level 0**: No verification guidance in agent context files or skills. Agents produce output and pass it directly to humans with no self-check.
- **Level 1**: Agent context files mention compilation or syntax checks, or skills run basic build commands, but there is no instruction to run the full test suite or iterate on failures.
- **Level 2**: Agent context files or skills explicitly instruct agents to run the full test suite and linter before presenting results, and to iterate on failures until they pass. A CLAUDE.md that says "always run `npm test` before completing" qualifies.
- **Level 3**: Level 2 is met AND agents have programmatic access to CI pipeline results (via GitHub/GitLab MCP server) AND production monitoring access (via observability MCP server) enabling post-deployment verification without human involvement.

Report in exactly this format:

**A3 — Feedback Loop Closure**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [one or two sentences citing the specific evidence]
