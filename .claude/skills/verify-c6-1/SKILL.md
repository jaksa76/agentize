---
name: verify-c6-1
description: Verify readiness criterion C6.1 (Static Analysis) in the current project. Reports fulfillment level 0–3.
allowed-tools: Bash Read
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Verify C6.1 — Static Analysis

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | No quality tooling |
| 1 | Linting and/or formatting configured |
| 2 | + Type checking enforced |
| 3 | + Security scanning (SAST) |

## Evidence to Gather

- Look for linting and formatting configuration files at the project root or embedded in a project configuration file (e.g., a `[tool.ruff]` section in `pyproject.toml`).
- Check CI workflow files for linting and formatting steps.
- Look for type checking configuration files (tsconfig with strict settings, mypy config, Pyright config, etc.) and check whether type checking runs in CI.
- Look for security scanning (SAST) configuration files and CI steps — check for tools like CodeQL, Snyk, Semgrep, Bandit, or similar.

## Instructions

Gather the evidence described above and determine the fulfillment level for C6.1.

Scoring guide:
- **Level 0**: No quality tooling of any kind — no linter config, no formatter config, no type checking, no security scanning.
- **Level 1**: Linting and/or formatting is configured — an ESLint, Prettier, Ruff, pylint, or equivalent config file exists, or a linting step runs in CI. At least one of: linter config file present, linting step in CI.
- **Level 2**: Type checking is additionally enforced — a tsconfig with strict mode or noImplicitAny, a mypy config, Pyright, or equivalent is configured. Type checking runs in CI is a strong indicator. Level 1 requirements must also be met.
- **Level 3**: Security scanning (SAST) is additionally configured — CodeQL, Snyk, Semgrep, SonarQube, Bandit, or equivalent runs in CI or is configured as a pre-merge step. Levels 1 and 2 must also be met.

Report in exactly this format:

**C6.1 — Static Analysis**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [one or two sentences citing the specific evidence]
