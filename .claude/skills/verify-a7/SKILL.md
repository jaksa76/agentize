---
name: verify-a7
description: Verify adoption criterion A7 (Proactive Quality Management) in the current project. Reports fulfillment level 0–3.
allowed-tools: Bash Read
---

# Verify A7 — Proactive Quality Management

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | No proactive quality management by agents; quality work is entirely human-initiated |
| 1 | Agents run quality checks (security scans, dependency audits) when explicitly asked by a developer |
| 2 | Agents automatically flag or report tech debt, security issues, and dependency updates, but do not open PRs to fix them |
| 3 | Agents proactively open PRs for tech debt reduction, dependency updates, security remediations, and standards enforcement without human initiation |

## Evidence

### Automated dependency update tooling
!`ls .github/dependabot.yml .github/dependabot.yaml renovate.json .renovaterc renovate.json5 2>/dev/null || echo "(no Dependabot or Renovate config)"`
!`cat .github/dependabot.yml 2>/dev/null | head -20 || cat renovate.json 2>/dev/null | head -20 || echo "(no dependency update config content)"`

### Scheduled quality / security workflows
!`find .github/workflows/ -name "*.yml" -o -name "*.yaml" 2>/dev/null | xargs grep -l -i "schedule\|codeql\|snyk\|trivy\|bandit\|dependabot\|audit\|security\|quality" 2>/dev/null | head -10 || echo "(no scheduled quality workflows)"`
!`grep -r -B2 -A10 "schedule:" .github/workflows/ 2>/dev/null | grep -A10 "schedule:" | head -40 || echo "(no scheduled workflow details)"`

### Agent-triggered quality PRs in git history
!`git log --since="90 days ago" --format="%s %b" 2>/dev/null | grep -i "dependabot\|renovate\|security\|cve\|tech.debt\|refactor\|dependency.update\|chore.*update\|bump " | head -20 || echo "(no automated quality PRs in recent git history)"`
!`git log --since="90 days ago" --author="dependabot\[bot\]\|renovate\[bot\]\|github-actions\[bot\]" --oneline 2>/dev/null | head -15 || echo "(no bot-authored commits)"`

### Skills for proactive quality tasks
!`find .claude/skills/ -name "SKILL.md" 2>/dev/null | xargs grep -l -i "security\|tech.debt\|dependency\|audit\|upgrade\|renovate\|vulnerability" 2>/dev/null | head -10 || echo "(no quality-focused skills)"`

### Quality reporting workflows (flag but don't fix)
!`find .github/workflows/ -name "*.yml" -o -name "*.yaml" 2>/dev/null | xargs grep -l -i "report\|flag\|notify\|comment.*issue\|create.*issue" 2>/dev/null | head -5 || echo "(no quality reporting workflows)"`

### CLAUDE.md / AGENTS.md — proactive quality instructions
!`grep -i "security\|tech.debt\|dependency\|audit\|quality\|vulnerability\|upgrade" CLAUDE.md AGENTS.md 2>/dev/null | head -15 || echo "(no quality guidance in agent context files)"`

## Instructions

Analyse the evidence above and determine the fulfillment level for A7.

Scoring guide:
- **Level 0**: No automated quality workflows, no Dependabot/Renovate, no bot-authored quality commits, no quality-focused skills. All quality work (security reviews, dependency updates, tech debt) is initiated manually by a developer.
- **Level 1**: Quality checks exist as agent-runnable tasks that a developer explicitly requests — e.g., a skill for security scanning or dependency auditing, but no automated triggering. Agents run quality checks on demand, not proactively.
- **Level 2**: Automated workflows flag or report quality issues without opening PRs to fix them — e.g., a scheduled CodeQL scan that posts results to an issue, a Snyk report workflow, a dependency audit that creates a report. The key distinction from Level 3: problems are flagged, not fixed.
- **Level 3**: Agents proactively open PRs without human initiation — Dependabot or Renovate auto-PR, a scheduled agent workflow that opens tech-debt or security fix PRs, or agent-authored fix commits appearing in git history from bot authors. Both dependency updates and security fixes may qualify separately.

Report in exactly this format:

**A7 — Proactive Quality Management**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [one or two sentences citing the specific evidence]
