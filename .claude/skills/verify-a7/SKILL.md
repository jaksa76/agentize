---
name: verify-a7
description: Verify adoption criterion A7 (Proactive Quality Management) in the current project. Reports fulfillment level 0–3.
allowed-tools: Bash Read
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Verify A7 — Proactive Quality Management

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | No proactive quality management by agents; quality work is entirely human-initiated |
| 1 | Agents run quality checks (security scans, dependency audits) when explicitly asked by a developer |
| 2 | Agents automatically flag or report tech debt, security issues, and dependency updates, but do not open PRs to fix them |
| 3 | Agents proactively open PRs for tech debt reduction, dependency updates, security remediations, and standards enforcement without human initiation |

## Evidence to Gather

- Check for Dependabot or Renovate configuration files in the `.github/` directory.
- Look at CI workflow files for scheduled quality, security scanning, or dependency-audit workflows.
- Check recent git history for bot-authored commits (dependabot, renovate, github-actions[bot]) that indicate automated quality fixes.
- Look in `.claude/skills/` for skills focused on security scanning, dependency auditing, or tech-debt management.
- Check `CLAUDE.md` or `AGENTS.md` for any proactive quality management guidance.

## Instructions

Gather the evidence described above and determine the fulfillment level for A7.

Scoring guide:
- **Level 0**: No automated quality workflows, no Dependabot/Renovate, no bot-authored quality commits, no quality-focused skills. All quality work (security reviews, dependency updates, tech debt) is initiated manually by a developer.
- **Level 1**: Quality checks exist as agent-runnable tasks that a developer explicitly requests — e.g., a skill for security scanning or dependency auditing, but no automated triggering. Agents run quality checks on demand, not proactively.
- **Level 2**: Automated workflows flag or report quality issues without opening PRs to fix them — e.g., a scheduled CodeQL scan that posts results to an issue, a Snyk report workflow, a dependency audit that creates a report. The key distinction from Level 3: problems are flagged, not fixed.
- **Level 3**: Agents proactively open PRs without human initiation — Dependabot or Renovate auto-PR, a scheduled agent workflow that opens tech-debt or security fix PRs, or agent-authored fix commits appearing in git history from bot authors. Both dependency updates and security fixes may qualify separately.

Report in exactly this format:

**A7 — Proactive Quality Management**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [one or two sentences citing the specific evidence]
