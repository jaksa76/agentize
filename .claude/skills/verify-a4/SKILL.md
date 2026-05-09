---
name: verify-a4
description: Verify adoption criterion A4 (Task Scope) in the current project. Reports fulfillment level 0–3.
allowed-tools: Bash Read
---

# Verify A4 — Task Scope

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | Agents only answer questions or explain code; they do not make changes |
| 1 | Agents handle bounded edits: a single function, a bug fix, a single-file change |
| 2 | Agents implement complete features spanning multiple files, writing and running tests as part of the implementation |
| 3 | Agents implement entire user stories end-to-end, including cross-service changes, test suites, documentation, and migration scripts |

## Evidence

### Agent-authored commit sizes (files changed per commit)
!`git log --since="90 days ago" --format="%H" 2>/dev/null | head -50 | while read hash; do git show --stat "$hash" 2>/dev/null | grep -i "co-authored-by\|claude\|copilot" > /dev/null 2>&1 && git show --stat "$hash" 2>/dev/null | tail -1; done | head -20 || echo "(could not compute agent commit sizes)"`

### Files changed in recent agent commits (stat summary)
!`git log --since="90 days ago" --format="%B" 2>/dev/null | grep -B5 "co-authored-by" | grep -v "^--$" | head -30 || echo "(no agent co-authored commits with context)"`

### Skill definitions describing task scope
!`find .claude/skills/ -name "SKILL.md" 2>/dev/null | xargs grep -h -i "story\|feature\|implement\|task\|multi-file\|cross-service\|end-to-end\|migration\|documentation" 2>/dev/null | head -20 || echo "(no scope-related content in skills)"`

### CLAUDE.md / AGENTS.md describing expected task granularity
!`grep -i "story\|feature\|task\|scope\|implement\|multi-file\|cross-service\|unit\|function\|file" CLAUDE.md AGENTS.md 2>/dev/null | head -20 || echo "(no task scope guidance in agent context files)"`

### Recent large multi-file agent commits (heuristic)
!`git log --since="90 days ago" --format="%H %s" 2>/dev/null | head -100 | while read hash msg; do
  body=$(git show --format="%B" --no-patch "$hash" 2>/dev/null)
  if echo "$body" | grep -qi "co-authored-by\|claude\|copilot"; then
    files=$(git show --stat "$hash" 2>/dev/null | tail -1 | grep -o "[0-9]* file" | grep -o "[0-9]*")
    if [ -n "$files" ] && [ "$files" -ge 3 ] 2>/dev/null; then
      echo "Multi-file agent commit ($files files): $msg"
    fi
  fi
done 2>/dev/null | head -10 || echo "(no multi-file agent commits detected)"`

### Task tracking files (TODO, stories, backlog)
!`ls TODO.md BACKLOG.md stories/ tasks/ 2>/dev/null || echo "(no task tracking files)"`
!`head -10 TODO.md 2>/dev/null || echo "(no TODO.md)"`

## Instructions

Analyse the evidence above and determine the fulfillment level for A4.

This criterion measures the largest scope of work that agents routinely handle end-to-end in this project. Look for evidence in git history (file counts per agent commit), skill definitions, and CLAUDE.md/AGENTS.md guidance.

Scoring guide:
- **Level 0**: No evidence of agents making code changes — no co-authored commits in git history, skills only describe Q&A or explanation tasks.
- **Level 1**: Agent-authored commits exist but are consistently small — 1–2 files changed, targeted bug fixes, single-function additions. Skill definitions describe bounded tasks.
- **Level 2**: Agent-authored commits regularly span multiple files (3+), include test files alongside implementation files, and/or skills describe full feature implementation as the expected scope.
- **Level 3**: Agent-authored commits span services or packages, include migrations, documentation, and comprehensive test suites. Skills or CLAUDE.md describe user-story-level implementation as the target scope. TODO/backlog items are story-level, not sub-task-level.

Report in exactly this format:

**A4 — Task Scope**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [one or two sentences citing the specific evidence]
