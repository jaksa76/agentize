---
name: verify-c8-1
description: Verify readiness criterion C8.1 (CI/CD Automation) in the current project. Reports fulfillment level 0–3.
allowed-tools: Bash Read
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Verify C8.1 — CI/CD Automation

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | No access to pipeline |
| 1 | Agents can read pipeline status |
| 2 | Agents can trigger pipeline runs |
| 3 | Full pipeline control including deployment |

## Evidence to Gather

- Look for CI configuration files (GitHub Actions workflows, GitLab CI, Jenkinsfile, etc.) and read their content to understand what the pipeline does.
- Check the MCP server configuration for any CI/CD or version control servers (GitHub, GitLab, Jenkins) that would allow agents to read pipeline status.
- Look for `workflow_dispatch` or equivalent manual triggers that would allow an agent to trigger CI runs via an API.
- Look for deployment steps in CI workflows and check for deployment infrastructure configuration (Kubernetes, Terraform, PaaS config files, etc.).
- Try accessing pipeline status via URLs, APIs, or MCP server endpoints if available.

## Instructions

Gather the evidence described above and determine the fulfillment level for C8.1.

Scoring guide:
- **Level 0**: No CI/CD pipeline exists, or no mechanism exists for an agent to interact with it.
- **Level 1**: A CI/CD pipeline exists and an agent can read its status — e.g., via the GitHub API (MCP server with GitHub access), GitLab API, or similar. The key question is whether an agent can check whether a pipeline run passed or failed without human intervention. Existence of a GitHub Actions MCP server or equivalent qualifies.
- **Level 2**: An agent can trigger pipeline runs — e.g., via `workflow_dispatch`, GitHub API calls, GitLab pipeline triggers, or a CI/CD MCP server that exposes trigger operations. Workflows with `workflow_dispatch` triggers that an agent can invoke via the API qualify.
- **Level 3**: Full pipeline control including deployment — an agent can not only trigger CI but also trigger deployments and observe their results. Deployment steps in workflows that an agent can initiate and monitor qualify. An agent-accessible deployment command (kubectl, helm, Terraform apply, etc.) combined with CI triggering qualifies.

Report in exactly this format:

**C8.1 — CI/CD Automation**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [one or two sentences citing the specific evidence]