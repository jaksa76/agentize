---
name: assess-adoption
description: Assess the Agent Adoption level of the current project across all 8 criteria (A1–A8) and produce a structured report with the achieved level, per-criterion scores, gaps, and recommendations.
allowed-tools: Bash Read
---

# Agent Adoption Assessment

This skill collects evidence for all 8 adoption criteria and instructs you to
score each one, determine the overall adoption level, and produce a full report.

---

## Evidence Collection

### A1 — Agent Context Availability
!`ls CLAUDE.md AGENTS.md .claude/CLAUDE.md 2>/dev/null || echo "(no agent context file)"`
!`wc -l CLAUDE.md 2>/dev/null || wc -l AGENTS.md 2>/dev/null || echo "(no agent context file)"`
!`head -60 CLAUDE.md 2>/dev/null || head -60 AGENTS.md 2>/dev/null || echo "(no content)"`
!`grep -i "convention\|command\|architecture\|run\|test\|build\|navigate\|workflow" CLAUDE.md AGENTS.md 2>/dev/null | head -15 || echo "(no key sections found)"`
!`cat .claude/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); mcp=d.get('mcpServers',{}); print('MCP servers:', list(mcp.keys()) if mcp else 'none')" 2>/dev/null || echo "(no MCP servers)"`
!`find docs/ -name "*.md" 2>/dev/null | head -10 || echo "(no docs/ directory)"`

### A2 — Agent-Authored Contributions
!`git log --oneline --since="90 days ago" 2>/dev/null | wc -l || echo "(no git history)"`
!`git log -50 --oneline 2>/dev/null | wc -l || echo "0"`
!`git log --since="90 days ago" --format="%B" 2>/dev/null | grep -ic "co-authored-by\|🤖\|generated with\|claude\|copilot\|github-actions\[bot\]" 2>/dev/null || echo "0"`
!`git log --since="90 days ago" --format="%s%n%b" 2>/dev/null | grep -i "co-authored-by\|🤖\|generated with claude\|copilot" | head -15 || echo "(no agent co-authorship markers found)"`
!`git log -50 --format="%B" 2>/dev/null | grep -ic "co-authored-by.*claude\|co-authored-by.*copilot\|co-authored-by.*anthropic\|🤖" 2>/dev/null || echo "0"`
!`git log --since="90 days ago" --merges --format="%s" 2>/dev/null | grep -i "claude\|copilot\|agent\|🤖" | head -10 || echo "(no agent-attributed merge commits)"`

### A3 — Feedback Loop Closure
!`grep -i "test\|build\|verify\|check\|lint\|run\|before.*submit\|before.*pr\|validate" CLAUDE.md AGENTS.md 2>/dev/null | head -15 || echo "(no verification guidance in agent context files)"`
!`find .claude/skills/ -name "SKILL.md" 2>/dev/null | xargs grep -h -i "run.*test\|npm test\|pytest\|go test\|cargo test\|lint\|build" 2>/dev/null | head -10 || echo "(no test/build commands in skills)"`
!`cat .claude/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); mcp=d.get('mcpServers',{}); ci=[k for k in mcp if any(x in k.lower() for x in ['github','gitlab','ci','pipeline'])]; obs=[k for k in mcp if any(x in k.lower() for x in ['grafana','datadog','sentry','monitor','metric'])]; print('CI MCP:', ci if ci else 'none'); print('Observability MCP:', obs if obs else 'none')" 2>/dev/null || echo "(no relevant MCP servers)"`
!`cat .claude/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); hooks=d.get('hooks',{}); print('Hooks:', list(hooks.keys()) if hooks else 'none')" 2>/dev/null || echo "(no hooks)"`

### A4 — Task Scope
!`find .claude/skills/ -name "SKILL.md" 2>/dev/null | xargs grep -h -i "story\|feature\|implement\|multi-file\|cross-service\|end-to-end\|migration" 2>/dev/null | head -15 || echo "(no scope-related content in skills)"`
!`grep -i "story\|feature\|task\|scope\|multi-file\|cross-service\|function\|file" CLAUDE.md AGENTS.md 2>/dev/null | head -10 || echo "(no task scope guidance in agent context)"`
!`head -10 TODO.md 2>/dev/null || head -10 BACKLOG.md 2>/dev/null || echo "(no TODO/BACKLOG)"`
!`git log --since="90 days ago" --format="%H %s" 2>/dev/null | head -80 | while read hash msg; do
  body=$(git show --format="%B" --no-patch "$hash" 2>/dev/null)
  if echo "$body" | grep -qi "co-authored-by\|claude\|copilot"; then
    files=$(git show --stat "$hash" 2>/dev/null | tail -1 | grep -o "[0-9]* file" | grep -o "[0-9]*")
    if [ -n "$files" ] 2>/dev/null; then echo "Agent commit ($files files): $msg"; fi
  fi
done 2>/dev/null | head -15 || echo "(could not compute agent commit sizes)"`

### A5 — Workflow Integration
!`find .claude/skills/ -name "SKILL.md" 2>/dev/null | xargs grep -h -i "git push\|gh pr create\|pull request" 2>/dev/null | head -10 || echo "(no PR creation steps in skills)"`
!`grep -i "pull request\|PR\|gh pr\|push" CLAUDE.md AGENTS.md 2>/dev/null | head -10 || echo "(no PR guidance in agent context)"`
!`grep -r "gh pr create\|peter-evans/create-pull-request\|hub pull-request" .github/workflows/ 2>/dev/null | head -5 || echo "(no automated PR creation in workflows)"`
!`cat .claude/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); mcp=d.get('mcpServers',{}); ci=[k for k in mcp if any(x in k.lower() for x in ['github','gitlab','ci'])]; print('CI MCP servers:', ci if ci else 'none')" 2>/dev/null || echo "(no CI MCP servers)"`
!`grep -r "deploy\|kubectl\|helm\|terraform apply" .github/workflows/ 2>/dev/null | grep -i "agent\|claude\|workflow_dispatch" | head -5 || echo "(no agent-triggered deployments)"`

### A6 — Autonomous Operation
!`grep -r -A3 "schedule:\|cron:" .github/workflows/ 2>/dev/null | head -20 || echo "(no scheduled workflows)"`
!`find .github/workflows/ -name "*.yml" -o -name "*.yaml" 2>/dev/null | xargs grep -l -i "claude\|copilot\|agent\|openai\|anthropic" 2>/dev/null | head -10 || echo "(no agent-invoking workflow files)"`
!`grep -r -i "claude\|copilot\|anthropic" .github/workflows/ 2>/dev/null | head -15 || echo "(no agent invocations in workflows)"`
!`grep -r "^on:" -A10 .github/workflows/ 2>/dev/null | head -40 || echo "(no workflow trigger configs)"`
!`find .github/workflows/ -name "*.yml" -o -name "*.yaml" 2>/dev/null | xargs grep -l -i "backlog\|todo\|next.*task\|pick.*task\|queue" 2>/dev/null | head -5 || echo "(no backlog-pulling workflows)"`

### A7 — Proactive Quality Management
!`ls .github/dependabot.yml .github/dependabot.yaml renovate.json .renovaterc 2>/dev/null || echo "(no Dependabot or Renovate config)"`
!`cat .github/dependabot.yml 2>/dev/null | head -15 || cat renovate.json 2>/dev/null | head -15 || echo "(no dependency update config)"`
!`find .github/workflows/ -name "*.yml" -o -name "*.yaml" 2>/dev/null | xargs grep -l -i "schedule.*security\|schedule.*audit\|schedule.*quality\|codeql\|snyk\|trivy" 2>/dev/null | head -5 || echo "(no scheduled security/quality workflows)"`
!`git log --since="90 days ago" --author="dependabot\[bot\]\|renovate\[bot\]\|github-actions\[bot\]" --oneline 2>/dev/null | head -15 || echo "(no bot-authored commits)"`
!`find .claude/skills/ -name "SKILL.md" 2>/dev/null | xargs grep -l -i "security\|tech.debt\|dependency\|audit\|vulnerability" 2>/dev/null | head -5 || echo "(no quality-focused skills)"`

### A8 — Planning Integration
!`find .claude/skills/ -name "SKILL.md" 2>/dev/null | xargs grep -l -i "story\|planning\|backlog\|decompose\|grooming\|epic" 2>/dev/null | head -5 || echo "(no planning-related skills)"`
!`cat .claude/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); mcp=d.get('mcpServers',{}); pm=[k for k in mcp if any(x in k.lower() for x in ['jira','linear','github','trello','notion','asana','clickup','shortcut'])]; print('PM MCP servers:', pm if pm else 'none')" 2>/dev/null || echo "(no PM MCP servers)"`
!`grep -i "story\|planning\|backlog\|grooming\|epic\|sprint\|ticket" CLAUDE.md AGENTS.md 2>/dev/null | head -10 || echo "(no planning guidance in agent context)"`
!`find .github/workflows/ -name "*.yml" -o -name "*.yaml" 2>/dev/null | xargs grep -l -i "story\|backlog\|grooming\|planning\|decompose" 2>/dev/null | head -5 || echo "(no planning workflows)"`

---

## Scoring Instructions

Using the evidence collected above, assign a fulfillment level to each criterion.

### Criterion scoring guides

**A1 Agent Context Availability (0–3)**
- 0: No CLAUDE.md, AGENTS.md, or equivalent; no meaningful README
- 1: Basic README exists; no conventions, commands, or navigation guidance
- 2: CLAUDE.md or AGENTS.md with conventions, key commands, architecture overview
- 3: Level 2 PLUS architecture docs structured for agent consumption AND MCP servers exposing project knowledge (requirements, diagrams, runbooks)

**A2 Agent-Authored Contributions (0–3)**
Divide agent-co-authored commit count by total recent commits (last 90 days or 50 commits):
- 0: 0% — no co-authorship markers in git history
- 1: < 25% of recent commits have agent co-authorship markers
- 2: 25–75% of recent commits have agent co-authorship markers
- 3: > 75%, or evidence of autonomous PR creation (bot-authored PRs, agent-creating workflows)

**A3 Feedback Loop Closure (0–3)**
- 0: No verification guidance in agent context files or skills
- 1: Agents run basic checks (build/compile) but not the full test suite
- 2: CLAUDE.md/AGENTS.md or skills explicitly instruct agents to run the full test suite, iterate on failures, and present only passing results
- 3: Level 2 PLUS CI pipeline access via MCP AND production monitoring access via MCP enabling post-deployment verification

**A4 Task Scope (0–3)**
Assess the largest scope routinely handled end-to-end:
- 0: No agent-authored changes; agents only answer questions
- 1: Agent commits are consistently 1–2 files; bounded single-function or bug-fix tasks
- 2: Agent commits regularly span 3+ files including test files; skills describe feature-level scope
- 3: Agent commits span services/packages; include migrations, docs, comprehensive tests; TODO items are story-level

**A5 Workflow Integration (0–3)**
- 0: Agents used in isolation; no PR creation in skills or workflows
- 1: Agents assist with tasks; humans manually create PRs and handle all handoffs
- 2: Skills or CLAUDE.md instruct agents to create PRs (`gh pr create`); CI MCP access for observing pipeline results
- 3: All of: agents create PRs, post review comments or trigger review workflows, monitor CI, trigger or observe deployments

**A6 Autonomous Operation (0–3)**
- 0: Agents always manually started; no automated triggering
- 1: At least one event-triggered workflow invokes an agent; most work is still manual
- 2: Agents systematically event-triggered for common events (push, PR, failing monitors)
- 3: Continuous pipeline pulls from backlog on a schedule; no per-story human initiation

**A7 Proactive Quality Management (0–3)**
- 0: No automated quality workflows; no Dependabot/Renovate; no bot-authored quality commits
- 1: Quality-check skills exist that developers explicitly invoke; no automated triggering
- 2: Scheduled workflows flag/report quality issues without opening PRs to fix them
- 3: Agents proactively open PRs — Dependabot/Renovate auto-PR, scheduled security fix workflows, bot-authored commits in git history

**A8 Planning Integration (0–3)**
- 0: No planning-related skills, no PM MCP servers, no planning guidance in agent context
- 1: Agents assist with planning ad-hoc when prompted; no configured planning step
- 2: Configured planning step exists — dedicated story/backlog skill, PM MCP server (Jira/Linear/GitHub Issues), or planning workflow in CLAUDE.md
- 3: Automated planning without human initiation — scheduled story generation, automatic backlog grooming, or autonomous epic decomposition

---

## Level–Criteria Mapping

After scoring all criteria, determine the highest adoption level where **all** thresholds are met:

| Criterion | Level 1 | Level 2 | Level 3 | Level 4 |
|-----------|---------|---------|---------|---------|
| A1 | ≥ 1 | ≥ 2 | ≥ 3 | ≥ 3 |
| A2 | ≥ 1 | ≥ 2 | ≥ 3 | ≥ 3 |
| A3 | — | ≥ 2 | ≥ 2 | ≥ 3 |
| A4 | ≥ 1 | ≥ 2 | ≥ 3 | ≥ 3 |
| A5 | — | ≥ 1 | ≥ 3 | ≥ 3 |
| A6 | — | — | ≥ 3 | ≥ 3 |
| A7 | — | — | — | ≥ 3 |
| A8 | — | — | — | ≥ 2 |

Check Level 1 first. If all Level 1 thresholds are met, check Level 2, and so on. The achieved level is the highest where all thresholds pass.

---

## Report Format

Produce a report in exactly this structure:

---

# Agent Adoption Assessment Report

**Project**: [name from README or directory name]
**Date**: [today's date]

## Result: Level [0/1/2/3/4] — [Level Name]

Level names: 0 = Unassisted, 1 = Vibe Coding, 2 = Agentic Engineering, 3 = Software Factory, 4 = Sustainable Autonomy

## Criterion Scores

| Criterion | Name | Score | Max |
|-----------|------|-------|-----|
| A1 | Agent Context Availability | [score] | 3 |
| A2 | Agent-Authored Contributions | [score] | 3 |
| A3 | Feedback Loop Closure | [score] | 3 |
| A4 | Task Scope | [score] | 3 |
| A5 | Workflow Integration | [score] | 3 |
| A6 | Autonomous Operation | [score] | 3 |
| A7 | Proactive Quality Management | [score] | 3 |
| A8 | Planning Integration | [score] | 3 |

## Gaps Blocking the Next Level

[If the project is at Level 4, write "Maximum level reached."]

[Otherwise, list each criterion below threshold for Level N+1:]

To reach Level [N+1] ([Name]), improve:
- **A_ [Name]**: currently [score], need [required] — [one sentence on what to improve]

## Readiness–Adoption Compatibility

[State the minimum recommended readiness level for the current adoption level:
- Adoption 0–1: Readiness 1+ recommended
- Adoption 2: Readiness 2+ recommended
- Adoption 3–4: Readiness 3 required

If the project's readiness level is known, note whether it supports the adoption level. If readiness is unknown, recommend running `/assess-readiness`.]

## Recommendations

[3–5 prioritised, actionable recommendations based on the gaps. Order by impact: criteria blocking a level increase first, then easiest wins.]

---
