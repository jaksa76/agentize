---
name: improve-c3-1
description: Improve readiness criterion C3.1 (Architecture Depth) in the current project by generating architecture documentation. Raises the fulfillment level by one step.
allowed-tools: Bash Read Write Edit
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Improve C3.1 — Architecture Depth

## Current State

### Existing architecture docs
!`find . -maxdepth 4 \( -iname "ARCHITECTURE.md" -o -iname "architecture.md" -o -iname "DESIGN.md" \) 2>/dev/null | grep -v node_modules | head -10 || echo "(none)"`
!`cat ARCHITECTURE.md 2>/dev/null || cat docs/ARCHITECTURE.md 2>/dev/null || cat docs/architecture.md 2>/dev/null || echo "(no architecture doc)"`

### docs/ directory
!`ls docs/ 2>/dev/null && ls docs/ || echo "(no docs/ directory)"`

### Project structure (for analysis)
!`ls -la`
!`ls src/ lib/ app/ packages/ services/ 2>/dev/null | head -30 || echo "(no standard source directories)"`
!`find . -maxdepth 3 -name "package.json" 2>/dev/null | grep -v node_modules | head -10 || echo "(no package.json files)"`

### README (may contain architecture info)
!`cat README.md 2>/dev/null | head -80 || echo "(no README)"`

### Service / API boundary detection
!`find . -maxdepth 4 \( -name "docker-compose.yml" -o -name "docker-compose.yaml" \) 2>/dev/null | head -5 || echo "(no docker-compose)"`
!`cat docker-compose.yml 2>/dev/null | grep "^  [a-z]" | head -20 || echo "(no services in docker-compose)"`
!`find . -maxdepth 3 -name "*.routes.*" -o -name "*router*" -o -name "*controller*" 2>/dev/null | grep -v node_modules | head -15 || echo "(no route/controller files)"`

## Instructions

**Step 1 — Determine current level:**
- Level 0: No architecture documentation
- Level 1: System context documented (purpose, users, external systems)
- Level 2: Container/service level documented
- Level 3: Component level + critical flows documented

**Step 2 — Read the project thoroughly before writing:**
Read the README, main source files, docker-compose, and route/controller files to understand the system well enough to write accurate documentation.

**Step 3 — Implement the improvement:**

**If current level is 0 → raise to 1:**
Create `docs/ARCHITECTURE.md` (create `docs/` if needed). Write a system-context section covering:
- What this system does and for whom (users/actors)
- External systems it interacts with (databases, APIs, services)
- High-level data/request flow (a simple text diagram or description)

Use a Mermaid context diagram if appropriate:
```
graph TD
    User --> System
    System --> ExternalService
```

**If current level is 1 → raise to 2:**
Add a container/service-level section to the existing architecture doc. Based on the project structure, docker-compose services, and package structure, document:
- Each major service/process/container and its responsibility
- How they communicate (HTTP, message queue, database, etc.)
- Port numbers and protocols where detectable

Include a Mermaid diagram:
```
graph LR
    API --> DB
    API --> Cache
    Worker --> DB
```

**If current level is 2 → raise to 3:**
Add component-level and critical-flow documentation to the existing architecture doc:
- For each major service, document its internal components (router, services, repositories, etc.)
- Document 2–3 critical flows (e.g., "User authentication flow", "Order processing flow") as sequence diagrams or numbered step descriptions

**If already at level 3:**
Report that C3.1 is already at its maximum level (3) and no improvement is needed.

**Step 4 — Report:**
State what file(s) were created or modified, the before and after level.
