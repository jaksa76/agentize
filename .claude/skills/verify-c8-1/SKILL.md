---
name: verify-c8-1
description: Verify readiness criterion C8.1 (CI/CD Automation) in the current project. Reports fulfillment level 0–3.
allowed-tools: Bash Read
---

# Verify C8.1 — CI/CD Automation

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | No access to pipeline |
| 1 | Agents can read pipeline status |
| 2 | Agents can trigger pipeline runs |
| 3 | Full pipeline control including deployment |

## Evidence

### CI configuration files
!`ls .github/workflows/ .gitlab-ci.yml Jenkinsfile .circleci/ .travis.yml azure-pipelines.yml bitbucket-pipelines.yml 2>/dev/null || echo "(no CI config files found)"`
!`ls .github/workflows/ 2>/dev/null && ls .github/workflows/ || true`

### Workflow file content (first file preview)
!`find .github/workflows/ -name "*.yml" -o -name "*.yaml" 2>/dev/null | head -1 | xargs head -60 2>/dev/null || cat .gitlab-ci.yml 2>/dev/null | head -60 || echo "(no workflow content to preview)"`

### Agent / MCP access to pipeline status
!`cat .claude/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); mcp=d.get('mcpServers',{}); gh=[k for k in mcp if 'github' in k.lower() or 'gitlab' in k.lower() or 'ci' in k.lower()]; print('CI-related MCP servers:', gh if gh else 'none')" 2>/dev/null || echo "(no .claude/settings.json or no CI MCP servers)"`
!`cat .mcp.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(list(d.get('mcpServers',{}).keys()))" 2>/dev/null || echo "(no .mcp.json)"`

### Deployment steps in workflows
!`grep -r -i "deploy\|release\|publish\|kubectl\|helm\|terraform\|ecs\|lambda\|cloud run\|heroku\|fly.io" .github/workflows/ .gitlab-ci.yml 2>/dev/null | head -20 || echo "(no deployment steps found in CI)"`

### Deployment configuration
!`ls kubernetes/ k8s/ helm/ terraform/ .terraform/ cdk/ pulumi/ 2>/dev/null || echo "(no infrastructure/IaC directories)"`
!`ls fly.toml .fly/ Dockerfile heroku.yml app.yaml render.yaml railway.toml 2>/dev/null || echo "(no PaaS deployment config)"`

### Agent-triggerable workflow (workflow_dispatch)
!`grep -r "workflow_dispatch\|api.*trigger\|manual.*trigger" .github/workflows/ 2>/dev/null | head -10 || echo "(no workflow_dispatch triggers found)"`

## Instructions

Analyse the evidence above and determine the fulfillment level for C8.1.

Scoring guide:
- **Level 0**: No CI/CD pipeline exists, or no mechanism exists for an agent to interact with it.
- **Level 1**: A CI/CD pipeline exists and an agent can read its status — e.g., via the GitHub API (MCP server with GitHub access), GitLab API, or similar. The key question is whether an agent can check whether a pipeline run passed or failed without human intervention. Existence of a GitHub Actions MCP server or equivalent qualifies.
- **Level 2**: An agent can trigger pipeline runs — e.g., via `workflow_dispatch`, GitHub API calls, GitLab pipeline triggers, or a CI/CD MCP server that exposes trigger operations. Workflows with `workflow_dispatch` triggers that an agent can invoke via the API qualify.
- **Level 3**: Full pipeline control including deployment — an agent can not only trigger CI but also trigger deployments and observe their results. Deployment steps in workflows that an agent can initiate and monitor qualify. An agent-accessible deployment command (kubectl, helm, Terraform apply, etc.) combined with CI triggering qualifies.

Report in exactly this format:

**C8.1 — CI/CD Automation**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [one or two sentences citing the specific evidence]
