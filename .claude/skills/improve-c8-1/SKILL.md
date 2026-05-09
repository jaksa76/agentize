---
name: improve-c8-1
description: Improve readiness criterion C8.1 (CI/CD Automation) in the current project by creating or extending GitHub Actions workflows. Raises the fulfillment level by one step.
allowed-tools: Bash Read Write Edit
---

# Improve C8.1 — CI/CD Automation

## Current State

### CI config files
!`ls .github/workflows/ 2>/dev/null && ls .github/workflows/ || ls .gitlab-ci.yml Jenkinsfile .circleci/ 2>/dev/null || echo "(no CI config)"`
!`find .github/workflows/ -name "*.yml" -o -name "*.yaml" 2>/dev/null | head -3 | xargs head -40 2>/dev/null || cat .gitlab-ci.yml 2>/dev/null | head -40 || echo "(no workflow content)"`

### Deployment steps
!`find .github/workflows/ -name "*.yml" -o -name "*.yaml" 2>/dev/null | xargs grep -l "deploy\|release\|publish" 2>/dev/null | head -5 || echo "(no deployment workflows)"`

### workflow_dispatch triggers
!`grep -r "workflow_dispatch" .github/workflows/ 2>/dev/null | head -5 || echo "(no workflow_dispatch)"`

### MCP / agent pipeline access
!`cat .claude/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); mcp=d.get('mcpServers',{}); ci=[k for k in mcp if any(x in k.lower() for x in ['github','gitlab','ci'])]; print('CI MCP servers:', ci if ci else 'none')" 2>/dev/null || echo "(no CI MCP)"`

### Language / build detection
!`ls package.json 2>/dev/null && cat package.json | python3 -c "import sys,json; d=json.load(sys.stdin); print('scripts:', list(d.get('scripts',{}).keys()))" 2>/dev/null || true`
!`ls pyproject.toml requirements.txt 2>/dev/null && echo "Python" || true`
!`ls pom.xml 2>/dev/null && echo "Maven/Java" || true`
!`ls build.gradle build.gradle.kts 2>/dev/null && echo "Gradle/Java" || true`
!`ls go.mod 2>/dev/null && echo "Go" || true`
!`ls Cargo.toml 2>/dev/null && echo "Rust" || true`

### Deployment infrastructure
!`ls kubernetes/ k8s/ helm/ terraform/ fly.toml heroku.yml app.yaml render.yaml 2>/dev/null || echo "(no deployment config)"`
!`ls Dockerfile 2>/dev/null && echo "(Dockerfile present)" || echo "(no Dockerfile)"`

## Instructions

**Step 1 — Determine current level:**
- Level 0: No CI pipeline exists
- Level 1: CI pipeline exists AND agents can read pipeline status (via GitHub API / MCP)
- Level 2: Agents can trigger pipeline runs (workflow_dispatch or equivalent)
- Level 3: Full pipeline control including deployment

Note: Level 1 requires a GitHub/GitLab MCP server for agents to read pipeline status programmatically. Creating the CI workflow is necessary but not sufficient — the MCP connection must also exist or be documented.

**Step 2 — Implement the improvement:**

**If current level is 0 → raise to 1:**
Create a CI workflow appropriate to the detected language. Create `.github/workflows/ci.yml`:

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - [language-specific setup step]
      - name: Install dependencies
        run: [install command]
      - name: Lint
        run: [lint command if linting is configured]
      - name: Test
        run: [test command]
```

Fill in the language-specific steps from the evidence above. Include `workflow_dispatch` trigger from the start (it makes Level 2 easier later).

Also add a note to CLAUDE.md (if it exists) that agents can check CI status via the GitHub API.

**If current level is 1 → raise to 2:**
Ensure `workflow_dispatch` is present in the CI workflow (add it if missing). This allows agents to trigger runs via the GitHub API.

Also document in CLAUDE.md how an agent can trigger CI:
```markdown
## CI/CD
- Check CI status: use the GitHub MCP server's `get_workflow_runs` tool
- Trigger CI: use the GitHub MCP server's `create_workflow_dispatch` tool on the `ci.yml` workflow
```

If no GitHub MCP server is configured in `.claude/settings.json`, document what needs to be set up.

**If current level is 2 → raise to 3:**
Add a deployment workflow. Based on detected infrastructure:

- **Fly.io** (`fly.toml` exists): Create `.github/workflows/deploy.yml` using `superfly/flyctl-actions` to deploy on push to main.
- **Heroku** (`heroku.yml` exists): Add Heroku deploy action.
- **Docker + generic**: Create a workflow that builds and pushes a Docker image to GitHub Container Registry (ghcr.io), then triggers a deployment via webhook or kubectl.
- **No infrastructure detected**: Create a template `.github/workflows/deploy.yml` with placeholders and clear comments explaining what to fill in.

Include `workflow_dispatch` in the deploy workflow so agents can trigger deployments manually.

**If already at level 3:**
Report that C8.1 is already at its maximum level (3) and no improvement is needed.

**Step 3 — Report:**
State what files were created or modified, the before and after level.
