---
name: improve-adoption
description: Assess the current Agent Adoption level of the project, identify which criteria block the next level, and implement improvements for each blocking criterion to raise the project to the next adoption level. Embeds all improve-a* logic inline.
allowed-tools: Bash Read Write Edit
---

# Improve Adoption Level

This skill assesses the current adoption level of the project, identifies which criteria block the next level, and then implements the improvements for each blocking criterion directly — embedding the relevant improve-a* logic inline.

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

### A3 — Feedback Loop Closure
!`grep -i "test\|build\|verify\|check\|lint\|run\|before.*submit\|before.*pr\|validate" CLAUDE.md AGENTS.md 2>/dev/null | head -15 || echo "(no verification guidance in agent context files)"`
!`find .claude/skills/ -name "SKILL.md" 2>/dev/null | xargs grep -h -i "run.*test\|npm test\|pytest\|go test\|cargo test\|lint\|build" 2>/dev/null | head -10 || echo "(no test/build commands in skills)"`
!`cat .claude/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); mcp=d.get('mcpServers',{}); ci=[k for k in mcp if any(x in k.lower() for x in ['github','gitlab','ci','pipeline'])]; obs=[k for k in mcp if any(x in k.lower() for x in ['grafana','datadog','sentry','monitor','metric'])]; print('CI MCP:', ci if ci else 'none'); print('Observability MCP:', obs if obs else 'none')" 2>/dev/null || echo "(no relevant MCP servers)"`

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

### A6 — Autonomous Operation
!`grep -r -A3 "schedule:\|cron:" .github/workflows/ 2>/dev/null | head -20 || echo "(no scheduled workflows)"`
!`find .github/workflows/ -name "*.yml" -o -name "*.yaml" 2>/dev/null | xargs grep -l -i "claude\|copilot\|agent\|openai\|anthropic" 2>/dev/null | head -10 || echo "(no agent-invoking workflow files)"`
!`grep -r -i "claude\|copilot\|anthropic" .github/workflows/ 2>/dev/null | head -15 || echo "(no agent invocations in workflows)"`
!`find .github/workflows/ -name "*.yml" -o -name "*.yaml" 2>/dev/null | xargs grep -l -i "backlog\|todo\|next.*task\|pick.*task\|queue" 2>/dev/null | head -5 || echo "(no backlog-pulling workflows)"`

### A7 — Proactive Quality Management
!`ls .github/dependabot.yml .github/dependabot.yaml renovate.json .renovaterc 2>/dev/null || echo "(no Dependabot or Renovate config)"`
!`cat .github/dependabot.yml 2>/dev/null | head -15 || cat renovate.json 2>/dev/null | head -15 || echo "(no dependency update config)"`
!`find .github/workflows/ -name "*.yml" -o -name "*.yaml" 2>/dev/null | xargs grep -l -i "schedule.*security\|schedule.*audit\|schedule.*quality\|codeql\|snyk\|trivy" 2>/dev/null | head -5 || echo "(no scheduled security/quality workflows)"`
!`git log --since="90 days ago" --author="dependabot\[bot\]\|renovate\[bot\]\|github-actions\[bot\]" --oneline 2>/dev/null | head -15 || echo "(no bot-authored commits)"`

### A8 — Planning Integration
!`find .claude/skills/ -name "SKILL.md" 2>/dev/null | xargs grep -l -i "story\|planning\|backlog\|decompose\|grooming\|epic" 2>/dev/null | head -5 || echo "(no planning-related skills)"`
!`cat .claude/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); mcp=d.get('mcpServers',{}); pm=[k for k in mcp if any(x in k.lower() for x in ['jira','linear','github','trello','notion','asana','clickup','shortcut'])]; print('PM MCP servers:', pm if pm else 'none')" 2>/dev/null || echo "(no PM MCP servers)"`
!`grep -i "story\|planning\|backlog\|grooming\|epic\|sprint\|ticket" CLAUDE.md AGENTS.md 2>/dev/null | head -10 || echo "(no planning guidance in agent context)"`
!`find .github/workflows/ -name "*.yml" -o -name "*.yaml" 2>/dev/null | xargs grep -l -i "story\|backlog\|grooming\|planning\|decompose" 2>/dev/null | head -5 || echo "(no planning workflows)"`

---

## Instructions

### Step 1 — Score each criterion

Using the evidence collected above, assign a fulfillment level to each criterion:

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

### Step 2 — Determine current adoption level

Use the Level–Criteria Mapping table below. Check levels in order (1, then 2, then 3, then 4). The current level is the highest where **all** applicable thresholds are met.

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

Level names: 0 = Unassisted, 1 = Vibe Coding, 2 = Agentic Engineering, 3 = Software Factory, 4 = Sustainable Autonomy

---

### Step 3 — Identify the target level and blocking criteria

- If current level is 4: Report "This project is already at Level 4 — Sustainable Autonomy. No further adoption improvements are possible." Stop here.
- Otherwise, target level = current level + 1.
- List every criterion where the score is below the target level's threshold. These are the **blocking criteria**.

---

### Step 4 — Report the current state

Print a summary like this before making any changes:

```
## Current Adoption Level

**Level**: [N] — [Level Name]
**Target**: Level [N+1] — [Level Name]

## Blocking Criteria for Level [N+1]

| Criterion | Name | Current Score | Required |
|-----------|------|---------------|----------|
| A_ | [Name] | [score] | ≥ [threshold] |
...

## Improvements to implement

For each blocking criterion, I will now run the corresponding improve-a* logic:
- A_ → improve-a_ (current: [score] → target: [threshold])
...
```

---

### Step 5 — Implement improvements for each blocking criterion

For each blocking criterion identified in Step 4, apply the improvement logic below. Work through them in order (lowest criterion ID first).

---

#### A1 — Agent Context Availability (improve-a1 logic)

Run these bash commands to gather additional evidence:
- `ls CLAUDE.md AGENTS.md .claude/CLAUDE.md 2>/dev/null || echo "(none)"`
- `cat CLAUDE.md 2>/dev/null || cat AGENTS.md 2>/dev/null || echo "(empty)"`
- `head -30 README.md 2>/dev/null || echo "(no README.md)"`
- `ls -la | head -20`
- `ls src/ lib/ app/ packages/ 2>/dev/null | head -20 || echo "(no standard source directories)"`
- `cat package.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print('scripts:', d.get('scripts',{}))" 2>/dev/null || true`
- `grep -i "^build\|^test\|^run\|^start\|^dev\|^lint" Makefile 2>/dev/null | head -10 || echo "(no Makefile targets)"`
- `find docs/ -name "*.md" 2>/dev/null | head -10 || find . -maxdepth 3 -iname "ARCHITECTURE.md" 2>/dev/null | head -5 || echo "(no architecture docs)"`

**If A1 = 0 → raise to 1:** Create or substantially expand `README.md` to include: project name and clear one-paragraph description, who uses this system (users/actors), getting started (prerequisites, installation, first run), high-level project structure.

**If A1 = 1 → raise to 2:** Create `CLAUDE.md` at the project root. Read the codebase thoroughly first, then write a substantive file covering:

```markdown
# CLAUDE.md

## Project Overview
[what this system does and for whom — inferred from code]

## Key Commands
[actual commands for building, testing, running, linting — from package.json scripts, Makefile, etc.]

## Project Structure
[what each main directory contains — inferred from the file tree]

## Coding Conventions
[naming style, file organisation, patterns — inferred from existing code]

## Workflow
[how to make changes: branch naming, commit style, PR process if detectable]

## Important Notes
[non-obvious constraints, required env vars, external services, known gotchas]
```

Do not write placeholder text — every section must be based on actual project evidence.

**If A1 = 2 → raise to 3:** Two things are needed:

1. **Architecture docs for agent consumption**: If `docs/ARCHITECTURE.md` doesn't exist, create it. Include system context (what the system does, who uses it, external integrations), service/module level (main components, responsibilities, how they communicate), and at least 2 critical flows documented as text or Mermaid sequence diagrams. Ensure it is referenced from CLAUDE.md.

2. **MCP server configuration**: Add a GitHub MCP server (or the most relevant MCP for this project) to `.claude/settings.json`. Create the file if it doesn't exist:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```

Add `GITHUB_PERSONAL_ACCESS_TOKEN=` to `.env.example` with a comment. Update CLAUDE.md to mention what MCP servers are available and what they expose.

**If A1 = 3:** Already at maximum; skip.

---

#### A2 — Agent-Authored Contributions (improve-a2 logic)

Run these bash commands to gather additional evidence:
- `git log --since="90 days ago" --oneline 2>/dev/null | wc -l || echo "0 total"`
- `git log --since="90 days ago" --format="%B" 2>/dev/null | grep -ic "co-authored-by\|🤖\|claude\|copilot" 2>/dev/null || echo "0 agent commits"`
- `git log -10 --format="%s %b" 2>/dev/null | head -20 || echo "(no recent commits)"`
- `ls CLAUDE.md AGENTS.md 2>/dev/null || echo "(none)"`
- `grep -i "co-author\|commit\|git\|agent\|claude" CLAUDE.md AGENTS.md 2>/dev/null | head -10 || echo "(no commit guidance)"`

**If A2 = 0 → raise to 1:** Set up the infrastructure so agents can start contributing:

1. **Update CLAUDE.md** (create if absent) with a git workflow section:
   ```markdown
   ## Git Workflow

   When committing changes, always add a co-authorship trailer:
   ```
   git commit -m "feat: description

   Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
   ```
   ```

2. **Create a git commit message template** at `.git/commit_template.txt`:
   ```
   # <type>: <subject>
   #
   # Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
   ```
   Then configure it: `git config commit.template .git/commit_template.txt`

3. **Create a basic implementation skill** (`.claude/skills/implement-task/SKILL.md`) if none exists, to give agents a reusable workflow for making contributions:
   ```markdown
   ---
   name: implement-task
   description: Implement a task described by the user. Reads context, makes changes, runs tests, and reports.
   allowed-tools: Bash Read Write Edit
   ---

   # Implement Task

   ## Project Context
   !`cat CLAUDE.md 2>/dev/null | head -60 || echo "(no CLAUDE.md)"`
   !`git status`

   ## Instructions
   1. Read the task description carefully.
   2. Read CLAUDE.md for conventions and key commands.
   3. Locate and read relevant code before making changes.
   4. Implement the change with the minimum necessary scope.
   5. Run the test suite and fix any failures.
   6. Report: files changed, what was done, how to verify.
   ```

**If A2 = 1 → raise to 2:** Tooling is in place; strengthen habitual use:

1. **Strengthen CLAUDE.md** with explicit guidance that agent use is the default:
   ```markdown
   ## Development Workflow

   Agent use is the default for all implementation work. For each task:
   1. Assign the task to Claude Code via /do-next-task or by describing the task
   2. Review the resulting diff rather than writing code from scratch
   3. Humans focus on requirements, architecture decisions, and code review
   ```

2. **Create a GitHub Actions workflow** that checks for co-authorship markers. Create `.github/workflows/agent-adoption.yml`:
   ```yaml
   name: Agent Adoption Check
   on: [pull_request]
   jobs:
     check-co-authorship:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
           with:
             fetch-depth: 20
         - name: Check for agent co-authorship
           run: |
             count=$(git log origin/${{ github.base_ref }}..HEAD --format="%B" | grep -ic "co-authored-by" || echo 0)
             total=$(git log origin/${{ github.base_ref }}..HEAD --oneline | wc -l)
             echo "Agent commits: $count / $total"
             if [ "$count" -eq 0 ] && [ "$total" -gt 0 ]; then
               echo "::notice::No agent co-authorship detected in this PR. Consider using Claude Code for implementation."
             fi
   ```

**If A2 = 2 → raise to 3:** Focus on autonomous PR creation. Create `.github/workflows/agent-implement.yml`:
   ```yaml
   name: Agent Implementation
   on:
     issues:
       types: [labeled]
   jobs:
     implement:
       if: github.event.label.name == 'agent-implement'
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - name: Implement issue with agent
           # Uses Claude Code CLI or Anthropic API
           # See CLAUDE.md for implementation details
           run: echo "Configure your agent implementation step here"
   ```
   Add documentation to CLAUDE.md explaining the `agent-implement` label workflow.

**If A2 = 3:** Already at maximum; skip.

---

#### A3 — Feedback Loop Closure (improve-a3 logic)

Run these bash commands to gather additional evidence:
- `cat CLAUDE.md 2>/dev/null || cat AGENTS.md 2>/dev/null || echo "(no agent context file)"`
- `cat package.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); s=d.get('scripts',{}); print({k:v for k,v in s.items() if any(x in k for x in ['test','lint','build','typecheck','check'])})" 2>/dev/null || true`
- `grep -i "^test\b\|^lint\b\|^build\b\|^check\b" Makefile 2>/dev/null | head -10 || echo "(no Makefile quality targets)"`
- `cat .claude/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); mcp=d.get('mcpServers',{}); print('MCP servers:', list(mcp.keys()) if mcp else 'none')" 2>/dev/null || echo "(no MCP servers)"`

**If A3 = 0 → raise to 1:** Add a verification section to CLAUDE.md (create if absent) with at minimum the build command:

```markdown
## Before Submitting Changes

Always verify your changes compile/build before presenting them:
- Build: `[detected build command]`
- If the build fails, fix the errors before proceeding.
```

Detect the build command from the evidence above (e.g., `npm run build`, `go build ./...`, `cargo build`).

**If A3 = 1 → raise to 2:** Expand the verification section in CLAUDE.md to require full test suite execution with iteration:

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

Fill in actual commands detected from package.json scripts or Makefile. Also update any existing skills to include these verification steps before their "Report" section.

**If A3 = 2 → raise to 3:** Add MCP server access for CI pipeline and production monitoring:

1. **CI pipeline access** — add a GitHub MCP server to `.claude/settings.json` if not present:
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

**If A3 = 3:** Already at maximum; skip.

---

#### A4 — Task Scope (improve-a4 logic)

Run these bash commands to gather additional evidence:
- `ls .claude/skills/ 2>/dev/null || echo "(no skills directory)"`
- `find .claude/skills/ -name "SKILL.md" 2>/dev/null | xargs grep -h "^description:" 2>/dev/null | head -20 || echo "(no skill descriptions)"`
- `ls -la`
- `ls src/ lib/ app/ services/ packages/ 2>/dev/null | head -20 || echo "(no standard source dirs)"`
- `cat package.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print('scripts:', list(d.get('scripts',{}).keys()))" 2>/dev/null || true`

**If A4 = 0 → raise to 1:** Create `.claude/skills/fix-bug/SKILL.md`:
```markdown
---
name: fix-bug
description: Fix a specific bug described by the user. Makes targeted changes to the minimum number of files needed.
allowed-tools: Bash Read Write Edit
---

# Fix Bug

## Context
!`git status`
!`git log --oneline -5`

## Instructions
1. Read the bug description from the user's prompt carefully.
2. Locate the relevant code using Read and Bash (grep/find).
3. Understand the root cause before making any changes.
4. Make the minimal targeted change to fix the bug.
5. Run the test suite: `[test command from CLAUDE.md]`
6. If tests fail, fix them or adjust your approach.
7. Report: what was changed, why, and how to verify the fix.
```

Update CLAUDE.md to encourage using agents for bug fixes and small tasks.

**If A4 = 1 → raise to 2:** Create `.claude/skills/implement-feature/SKILL.md`:
```markdown
---
name: implement-feature
description: Implement a complete feature spanning multiple files. Includes writing tests and running the full suite before completing.
allowed-tools: Bash Read Write Edit
---

# Implement Feature

## Project Context
!`cat CLAUDE.md 2>/dev/null | head -60 || echo "(no CLAUDE.md)"`
!`ls src/ lib/ app/ 2>/dev/null | head -20`

## Instructions
1. Read the feature description carefully.
2. Read CLAUDE.md for conventions and key commands.
3. Plan the implementation: identify which files to create/modify.
4. Read existing code in the affected areas before making changes.
5. Implement the feature across all necessary files.
6. Write tests for the new functionality (unit + integration if applicable).
7. Run: build → lint → tests. Fix any failures.
8. Report: files changed, tests added, how to verify.
```

Also update CLAUDE.md to state that feature-level tasks should be assigned to agents as a whole.

**If A4 = 2 → raise to 3:** Create `.claude/skills/implement-story/SKILL.md`:
```markdown
---
name: implement-story
description: Implement a complete user story end-to-end, including all services, tests, documentation, and database migrations.
allowed-tools: Bash Read Write Edit
---

# Implement Story

## Project Context
!`cat CLAUDE.md 2>/dev/null | head -80`
!`ls -la`

## Instructions
1. Read the story description and acceptance criteria carefully.
2. Read CLAUDE.md for conventions, architecture, and commands.
3. Read VISION.md or relevant requirements docs.
4. Read all files in the affected service(s) before implementing.
5. Plan the full scope: API changes, DB migrations, frontend changes, tests, docs.
6. Implement all changes across all services/packages.
7. Write comprehensive tests: unit, integration, and E2E if applicable.
8. Update relevant documentation.
9. Run: build → lint → typecheck → tests. Fix any failures.
10. Report: all files changed, tests added, acceptance criteria verified.
```

Also create a `TODO.md` (if absent) with story-level items to make the story-scope expectation concrete.

**If A4 = 3:** Already at maximum; skip.

---

#### A5 — Workflow Integration (improve-a5 logic)

Run these bash commands to gather additional evidence:
- `git log --since="90 days ago" --format="%B" 2>/dev/null | grep -i "gh pr\|pull request\|PR#\|created pr" | head -10 || echo "(no PR creation evidence)"`
- `grep -i "pr\|pull request\|review\|ci\|deploy\|workflow\|handoff" CLAUDE.md AGENTS.md 2>/dev/null | head -15 || echo "(no workflow guidance in context files)"`
- `find .claude/skills/ -name "SKILL.md" 2>/dev/null | xargs grep -h -i "gh pr\|pull request\|PR" 2>/dev/null | head -10 || echo "(no PR creation in skills)"`
- `ls .github/workflows/ 2>/dev/null | head -10 || echo "(no GitHub Actions workflows)"`
- `which gh 2>/dev/null || echo "gh not installed"`

**If A5 = 0 → raise to 1:** Update CLAUDE.md (create if absent) with a workflow section:

```markdown
## Workflow Handoffs

When completing implementation work:
1. Summarize what was changed and why in your response
2. List all files modified
3. The developer will review the diff and incorporate it into a PR manually
```

Also add to any existing implementation skills a final "Handoff" section that lists files changed and suggests a commit message.

**If A5 = 1 → raise to 2:** Add PR creation steps to CLAUDE.md and to all implementation skills:

1. **Update CLAUDE.md** with PR creation guidance:
```markdown
## Creating Pull Requests

When implementation is complete and tests pass, create a PR:

```bash
git checkout -b feat/<short-description>
git add <changed files>
git commit -m "feat: <description>

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<bullet points of what was implemented>

## Test plan
- [ ] Tests pass locally (all suites)
- [ ] Reviewed for regressions

🤖 Generated with Claude Code
EOF
)"
```

After creating the PR, note the PR URL in your response.
```

2. **Update all implementation skills** to include a "Create PR" step before "Report": `git checkout -b`, `git add`, `git commit` with co-authorship, `gh pr create` with a structured body.

3. **Check if `gh` CLI is available**: Run `which gh 2>/dev/null || echo "not installed"`. If not installed, note in CLAUDE.md that `gh` must be installed (`brew install gh` / `sudo apt install gh`) and authenticated (`gh auth login`).

**If A5 = 2 → raise to 3:** Add CI monitoring and review comment capabilities:

1. **Update CLAUDE.md** with post-PR verification guidance:
```markdown
## Post-PR Verification

After creating a PR:
1. Note the PR number from `gh pr create` output
2. Wait for CI to start: `gh run list --branch <branch> --limit 3`
3. Watch CI status: `gh run watch <run-id>`
4. If CI fails, read the failure: `gh run view <run-id> --log-failed`
5. Fix the issue, push, and re-verify
6. Only request review when CI passes
```

2. **Add a GitHub MCP server** to `.claude/settings.json` if not present (see A3 = 2 config above).

3. **Create a PR review comment workflow** at `.github/workflows/agent-review.yml`:
```yaml
name: Agent Review
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
      - name: Post review checklist comment
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          gh pr comment ${{ github.event.pull_request.number }} \
            --body "## Agent Review Checklist
          - [ ] Tests pass in CI
          - [ ] No new lint warnings
          - [ ] Co-authorship trailer present
          - [ ] PR description explains the change"
```

4. **Update implementation skills** to include CI watching as a step after PR creation.

**If A5 = 3:** Already at maximum; skip.

---

#### A6 — Autonomous Operation (improve-a6 logic)

Run these bash commands to gather additional evidence:
- `ls .github/workflows/ 2>/dev/null | head -20 || echo "(no GitHub Actions workflows)"`
- `find .github/workflows/ -name "*.yml" 2>/dev/null | xargs grep -h "on:" 2>/dev/null | head -20 || echo "(no trigger configs)"`
- `find .github/workflows/ -name "*.yml" 2>/dev/null | xargs grep -h -i "claude\|agent\|implement\|llm\|ai" 2>/dev/null | head -10 || echo "(no agent invocation in CI)"`
- `find .github/workflows/ -name "*.yml" 2>/dev/null | xargs grep -h "cron:" 2>/dev/null | head -10 || echo "(no cron schedules)"`

**If A6 = 0 → raise to 1:** Create `.github/workflows/agent-on-label.yml`:
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

**If A6 = 1 → raise to 2:** Expand to systematic event-triggered workflows:

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
          Label agent-implement to trigger auto-diagnosis." \
            --label "ci-failure"
```

**If A6 = 2 → raise to 3:** Create `.github/workflows/agent-pipeline.yml`:
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
          NEXT=$(head -1 TODO.md 2>/dev/null || echo "")
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

**If A6 = 3:** Already at maximum; skip.

---

#### A7 — Proactive Quality Management (improve-a7 logic)

Run these bash commands to gather additional evidence:
- `ls .github/dependabot.yml 2>/dev/null && echo "(dependabot configured)" || echo "(no dependabot)"`
- `cat .github/dependabot.yml 2>/dev/null | head -20 || echo "(no dependabot config)"`
- `ls renovate.json .renovaterc .renovaterc.json 2>/dev/null && echo "(renovate configured)" || echo "(no renovate)"`
- `find .github/workflows/ -name "*.yml" 2>/dev/null | xargs grep -l "codeql\|snyk\|trivy\|audit\|security\|vulnerability" 2>/dev/null || echo "(no security workflows)"`
- `ls package.json pyproject.toml pom.xml go.mod Cargo.toml requirements.txt 2>/dev/null | head -5 || echo "(no package manifest)"`

**If A7 = 0 → raise to 1:** Add quality check commands to CLAUDE.md:

```markdown
## Quality Checks

Run these checks before submitting a PR:

```bash
# Dependency audit (pick the relevant one):
npm audit                     # Node.js
pip-audit                     # Python (pip install pip-audit)
cargo audit                   # Rust (cargo install cargo-audit)
mvn dependency:analyze        # Java/Maven

# Static analysis:
npx eslint . --ext .js,.ts    # JavaScript/TypeScript
ruff check .                  # Python
golangci-lint run             # Go

# Dependency freshness:
npm outdated                  # Node.js
pip list --outdated           # Python
```

When asked to "do a quality check", run the relevant commands for this project and report findings.
```

**If A7 = 1 → raise to 2:** Create scheduled workflows that scan and report findings:

1. Create `.github/workflows/dependency-audit.yml`:
```yaml
name: Dependency Audit
on:
  schedule:
    - cron: '0 8 * * 1'  # Every Monday at 8am
  workflow_dispatch:

jobs:
  audit:
    runs-on: ubuntu-latest
    permissions:
      issues: write
    steps:
      - uses: actions/checkout@v4

      - name: Run dependency audit
        id: audit
        continue-on-error: true
        run: |
          if [ -f package.json ]; then
            npm ci --prefer-offline 2>/dev/null || npm install
            RESULT=$(npm audit --json 2>/dev/null || echo '{}')
            VULN_COUNT=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('metadata',{}).get('vulnerabilities',{}).get('total', 0))" 2>/dev/null || echo "unknown")
          elif [ -f requirements.txt ]; then
            pip install pip-audit -q
            VULN_COUNT=$(pip-audit -r requirements.txt --format json 2>/dev/null | python3 -c "import sys,json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "unknown")
          else
            VULN_COUNT="unknown (no supported package manager)"
          fi
          echo "vuln_count=$VULN_COUNT" >> $GITHUB_OUTPUT
          echo "Vulnerabilities found: $VULN_COUNT"

      - name: Create issue if vulnerabilities found
        if: steps.audit.outputs.vuln_count != '0'
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          gh issue create \
            --title "Weekly dependency audit: ${{ steps.audit.outputs.vuln_count }} vulnerability/vulnerabilities found" \
            --body "Automated dependency audit found issues. Run \`npm audit\` (or equivalent) locally for details. Add label \`agent-implement\` to trigger automated remediation." \
            --label "security,dependencies"
```

2. Create `.github/workflows/dependency-freshness.yml`:
```yaml
name: Dependency Freshness
on:
  schedule:
    - cron: '0 9 1 * *'  # First day of each month
  workflow_dispatch:

jobs:
  check-outdated:
    runs-on: ubuntu-latest
    permissions:
      issues: write
    steps:
      - uses: actions/checkout@v4
      - name: Check outdated packages
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          if [ -f package.json ]; then
            npm install -q
            OUTDATED=$(npm outdated --parseable 2>/dev/null | wc -l || echo 0)
            if [ "$OUTDATED" -gt 0 ]; then
              gh issue create \
                --title "Monthly dependency check: $OUTDATED outdated packages" \
                --body "$(npm outdated 2>/dev/null || echo 'Run npm outdated for details')" \
                --label "dependencies"
            fi
          fi
```

**If A7 = 2 → raise to 3:** Enable automated PR creation for dependency updates.

1. **Configure Dependabot**. Create `.github/dependabot.yml` (adjust package-ecosystem to match the project):

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    open-pull-requests-limit: 5
    labels:
      - "dependencies"
      - "automated"
    commit-message:
      prefix: "chore"

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    labels:
      - "dependencies"
      - "automated"
```

2. Create `.github/workflows/agent-tech-debt.yml`:
```yaml
name: Agent Tech Debt
on:
  schedule:
    - cron: '0 6 * * 1'  # Every Monday morning
  workflow_dispatch:

jobs:
  tech-debt:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
    steps:
      - uses: actions/checkout@v4

      - name: Find tech debt items
        id: debt
        run: |
          TODO_COUNT=$(grep -r "TODO\|FIXME\|HACK\|XXX" --include="*.ts" --include="*.js" --include="*.py" --include="*.go" . 2>/dev/null | grep -v node_modules | wc -l || echo 0)
          echo "todo_count=$TODO_COUNT" >> $GITHUB_OUTPUT
          echo "Tech debt items: $TODO_COUNT"

      - name: Implement one tech debt item
        if: steps.debt.outputs.todo_count != '0'
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          ITEMS=$(grep -rn "TODO\|FIXME" --include="*.ts" --include="*.js" --include="*.py" --include="*.go" . 2>/dev/null | grep -v node_modules | head -5)
          echo "Tech debt items found:"
          echo "$ITEMS"
          # Configure agent invocation:
          # claude --print "Fix one of these TODO/FIXME items: $ITEMS. Create a PR."
          echo "Configure ANTHROPIC_API_KEY secret and agent invocation"
```

3. Update CLAUDE.md:
```markdown
## Proactive Quality Management

Automated quality management is configured:

- **Dependabot** (`.github/dependabot.yml`): Opens PRs weekly for outdated npm/pip/docker/actions dependencies
- **Dependency Audit** (weekly): Creates issues when vulnerabilities are found
- **Tech Debt** (weekly): Agent opens PRs to fix TODO/FIXME items
```

**If A7 = 3:** Already at maximum; skip.

---

#### A8 — Planning Integration (improve-a8 logic)

Run these bash commands to gather additional evidence:
- `find .claude/skills/ -name "SKILL.md" 2>/dev/null | xargs grep -l -i "story\|backlog\|epic\|plan\|decompos" 2>/dev/null | head -5 || echo "(no planning skills)"`
- `grep -i "story\|backlog\|epic\|plan\|decompos" CLAUDE.md AGENTS.md 2>/dev/null | head -10 || echo "(no planning guidance)"`
- `ls TODO.md BACKLOG.md STORIES.md 2>/dev/null || echo "(no backlog files)"`
- `head -20 TODO.md 2>/dev/null || head -20 BACKLOG.md 2>/dev/null || echo "(no backlog content)"`

**If A8 = 0 → raise to 1:** Add planning assistance guidance to CLAUDE.md:

```markdown
## Planning Assistance

Agents can assist with planning tasks when asked. Examples:

- "Break this goal into user stories: [goal description]"
- "Decompose this epic into concrete tasks: [epic description]"
- "Write acceptance criteria for this story: [story description]"
- "Suggest a task breakdown for implementing: [feature description]"

Use these prompts to accelerate planning sessions. The agent will produce a structured list that can be added to TODO.md or your backlog.
```

**If A8 = 1 → raise to 2:** Create a `generate-story` skill and a `decompose-epic` skill:

Create `.claude/skills/generate-story/SKILL.md`:
```markdown
---
name: generate-story
description: Generate a well-formed user story with acceptance criteria and task breakdown from a high-level goal or feature description.
allowed-tools: Bash Read Write Edit
---

# Generate Story

## Project Context
!`cat CLAUDE.md 2>/dev/null | head -60 || echo "(no CLAUDE.md)"`
!`cat VISION.md 2>/dev/null | head -40 || echo "(no VISION.md)"`
!`head -20 TODO.md 2>/dev/null || echo "(no TODO.md)"`

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

Create `.claude/skills/decompose-epic/SKILL.md`:
```markdown
---
name: decompose-epic
description: Decompose a high-level epic or goal into a prioritised list of user stories, each with acceptance criteria.
allowed-tools: Bash Read Write Edit
---

# Decompose Epic

## Project Context
!`cat CLAUDE.md 2>/dev/null | head -60 || echo "(no CLAUDE.md)"`
!`cat VISION.md 2>/dev/null | head -40 || echo "(no VISION.md)"`
!`head -30 TODO.md 2>/dev/null || head -30 BACKLOG.md 2>/dev/null || echo "(no backlog)"`

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

**If A8 = 2 → raise to 3:** Add autonomous backlog grooming via a scheduled workflow:

Create `.github/workflows/agent-backlog-grooming.yml`:
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

Add to CLAUDE.md:
```markdown
## Planning Integration (Autonomous)

The agent backlog grooming runs every Monday (`.github/workflows/agent-backlog-grooming.yml`):
- Reviews TODO.md and refines entries (splits large items, removes duplicates, clarifies vague tasks)
- Opens a PR with the refined backlog for human review

Required secret: `ANTHROPIC_API_KEY`.
```

**If A8 = 3:** Already at maximum; skip.

---

### Step 6 — Final report

After completing all improvements, produce a summary:

```
## Improvement Summary

**Previous level**: Level [N] — [Name]
**New level**: Level [N+1] — [Name] (if all blocking criteria have been resolved)

### Changes made

| Criterion | Before | After | Change |
|-----------|--------|-------|--------|
| A_ [Name] | [old score] | [new score] | [file/action] |
...

### Remaining gaps (if any)

[List any criteria that could not be fully automated, e.g., A2 → 2 or 3 requires genuine changes in team behaviour that tooling alone cannot achieve. Explain what manual steps the team needs to take.]

### Next steps

[If still below Level 4, note what the next improvement cycle would target.]
```
