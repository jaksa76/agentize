---
name: verify-c3-1
description: Verify readiness criterion C3.1 (Architecture Depth) in the current project. Reports fulfillment level 0–3.
allowed-tools: Bash Read
---

# Verify C3.1 — Architecture Depth

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | No in-repo architecture docs |
| 1 | System context documented (users, external systems) |
| 2 | Container/service level documented |
| 3 | Component level documented + critical flows documented |

All documentation must live in-repo or be accessible via MCP to count.

## Evidence

### Architecture-related files at root and in docs/
!`find . -maxdepth 4 \( -iname "ARCHITECTURE.md" -o -iname "architecture.md" -o -iname "DESIGN.md" -o -iname "design.md" -o -iname "TECHNICAL.md" -o -iname "ADR.md" \) 2>/dev/null | grep -v node_modules | head -20 || echo "(none found)"`

### docs/ directory contents
!`find docs/ -name "*.md" -o -name "*.puml" -o -name "*.c4" 2>/dev/null | head -30 || echo "(no docs/ directory or no files there)"`

### C4 / diagram files
!`find . -maxdepth 5 \( -name "*.puml" -o -name "*.c4" -o -name "*.drawio" -o -name "*.mmd" \) 2>/dev/null | grep -v node_modules | head -20 || echo "(no diagram files found)"`

### Architecture keywords in README
!`grep -n -i "architecture\|c4\|container diagram\|component\|service\|context diagram\|external system\|flow\|sequence" README.md 2>/dev/null | head -20 || echo "(no architecture keywords in README)"`

### Preview of primary architecture doc (if present)
!`head -80 docs/ARCHITECTURE.md 2>/dev/null || head -80 ARCHITECTURE.md 2>/dev/null || head -80 docs/architecture.md 2>/dev/null || echo "(no primary architecture doc found)"`

## Instructions

Analyse the evidence above and determine the fulfillment level for C3.1.

Scoring guide:
- **Level 0**: No architecture documentation exists in the repo — no dedicated architecture file, no architecture section in the README, no diagrams.
- **Level 1**: System-context level documentation exists: who the users are, what external systems interact with this project, and the high-level purpose. A README paragraph or a simple context diagram qualifies.
- **Level 2**: Container or service-level documentation exists — shows the major services, processes, or containers that make up the system and how they interact (e.g., a C4 container diagram, a services overview, API boundary docs).
- **Level 3**: Component-level documentation exists (internal structure of individual services/containers) AND critical flows or sequence diagrams are documented (e.g., key request paths, authentication flow, data pipeline).

Report in exactly this format:

**C3.1 — Architecture Depth**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [one or two sentences citing the specific evidence]
