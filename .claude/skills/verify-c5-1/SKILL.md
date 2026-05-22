---
name: verify-c5-1
description: Verify readiness criterion C5.1 (Runnability) in the current project. Reports fulfillment level 0–2.
allowed-tools: Bash Read
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Verify C5.1 — Runnability

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | Project does not build |
| 1 | Project builds without errors |
| 2 | App can be run locally or in an ephemeral environment |

## Evidence

### Build system / language indicators
!`ls package.json pom.xml build.gradle build.gradle.kts setup.py pyproject.toml Cargo.toml go.mod mix.exs build.sbt 2>/dev/null || echo "(no standard build manifests found)"`

### package.json scripts (Node/JS projects)
!`cat package.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); s=d.get('scripts',{}); print('scripts:', list(s.keys()))" 2>/dev/null || true`

### Makefile targets related to build/run
!`grep -i "^build\b\|^run\b\|^start\b\|^serve\b\|^dev\b\|^compile\b\|^test\b" Makefile 2>/dev/null | head -15 || echo "(no Makefile or no build/run targets)"`

### Run / serve configuration
!`ls Procfile docker-compose.yml docker-compose.yaml .env.example 2>/dev/null || echo "(no Procfile, docker-compose, or .env.example)"`
!`cat Procfile 2>/dev/null | head -10 || true`

### CI evidence of builds succeeding
!`find .github/workflows/ -name "*.yml" -o -name "*.yaml" 2>/dev/null | xargs grep -l "build\|compile\|test" 2>/dev/null | head -5 || echo "(no CI workflow files with build/compile/test)"`

### README build/run instructions
!`grep -A8 -i "build\|compile\|run\|start\|serve\|launch\|docker" README.md 2>/dev/null | head -30 || echo "(no build/run keywords in README)"`

## Instructions

Analyse the evidence above and determine the fulfillment level for C5.1.

Scoring guide:
- **Level 0**: The project does not build or the build system is missing/broken. Indicators: no build manifest, no build instructions, CI consistently failing on build steps (if CI exists).
- **Level 1**: The project builds successfully — compilation succeeds, dependencies resolve, no build-time errors. Indicators: a working build manifest, CI passing on build jobs, or clear README instructions that produce a build artifact.
- **Level 2**: The application can be run locally or in an ephemeral environment — a server starts, a CLI executes, a container runs. Indicators: a Procfile, docker-compose, a `start` script in package.json, a README `run` section, or equivalent that demonstrates the app can be invoked and produces output.

Report in exactly this format:

**C5.1 — Runnability**
- **Level**: [0 / 1 / 2]
- **Rationale**: [one or two sentences citing the specific evidence]
