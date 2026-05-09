---
name: improve-a5
description: Improve adoption criterion A5 (Workflow Integration) by embedding agents into pull request creation, CI observation, and review processes. Raises the fulfillment level by one step.
allowed-tools: Bash Read Write Edit
---

# Improve A5 — Workflow Integration

## Current State

### PR creation patterns in git/GitHub history
!`git log --since="90 days ago" --format="%B" 2>/dev/null | grep -i "gh pr\|pull request\|PR#\|created pr" | head -10 || echo "(no PR creation evidence)"`

### Agent context files — PR/workflow guidance
!`grep -i "pr\|pull request\|review\|ci\|deploy\|workflow\|handoff" CLAUDE.md AGENTS.md 2>/dev/null | head -15 || echo "(no workflow guidance in context files)"`

### Skills with PR creation steps
!`find .claude/skills/ -name "SKILL.md" 2>/dev/null | xargs grep -h -i "gh pr\|pull request\|PR" 2>/dev/null | head -10 || echo "(no PR creation in skills)"`

### CI configuration
!`ls .github/workflows/ 2>/dev/null | head -10 || echo "(no GitHub Actions workflows)"`
!`ls .circleci/config.yml .travis.yml Jenkinsfile 2>/dev/null || echo "(no other CI config)"`

### Review automation
!`ls .github/CODEOWNERS .github/pull_request_template.md 2>/dev/null || echo "(no review automation config)"`
!`find .github/workflows/ -name "*.yml" 2>/dev/null | xargs grep -l "review\|comment\|approve" 2>/dev/null || echo "(no review automation workflows)"`

### MCP servers (for CI/deployment access)
!`cat .claude/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); mcp=d.get('mcpServers',{}); print('MCP servers:', list(mcp.keys()) if mcp else 'none')" 2>/dev/null || echo "(no MCP servers)"`

## Instructions

**Step 1 — Determine current level:**
- Level 0: Agents used in isolation; all handoffs (PRs, reviews, CI, deployments) are managed by humans
- Level 1: Agents assist with tasks but humans handle all handoffs; agent output is manually incorporated
- Level 2: Agents create pull requests with generated descriptions; agents observe CI results as part of their workflow
- Level 3: Agents are fully embedded: create PRs, post review comments, monitor CI, trigger and observe deployments

**Assessment guide:**
- If no skills or CLAUDE.md mention `gh pr create` or PR workflows → Level 0 or 1
- If skills/CLAUDE.md instruct agents to create PRs but no CI monitoring → Level 2
- If CI observation is in skills and agents post review comments or monitor deployments → Level 3

**Step 2 — Implement the improvement:**

**If current level is 0 → raise to 1:**
Update CLAUDE.md (create if absent) with a workflow section that describes the expected handoff process:

```markdown
## Workflow Handoffs

When completing implementation work:
1. Summarize what was changed and why in your response
2. List all files modified
3. The developer will review the diff and incorporate it into a PR manually
```

Also add to any existing implementation skills a final "Handoff" section that lists files changed and suggests a commit message.

**If current level is 1 → raise to 2:**
Add PR creation steps to CLAUDE.md and to all implementation skills:

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

2. **Update all implementation skills** (`implement-feature`, `implement-story`, `fix-bug` if they exist) to include a "Create PR" step before "Report":
   - `git checkout -b` with a descriptive branch name
   - `git add` and `git commit` with co-authorship
   - `gh pr create` with a structured body

3. **Check if `gh` CLI is available**: Run `which gh 2>/dev/null || echo "not installed"`. If not installed, note in CLAUDE.md that `gh` must be installed (`brew install gh` / `sudo apt install gh`) and authenticated (`gh auth login`).

**If current level is 2 → raise to 3:**
Add CI monitoring and review comment capabilities:

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

2. **Add a GitHub MCP server** to `.claude/settings.json` if not present:
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

**If already at level 3:**
Report that A5 is already at its maximum level (3) and no improvement is needed.

**Step 3 — Report:**
State what files were created or modified, the before and after level.
