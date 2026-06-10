---
name: verify-c6-1
description: Verify readiness criterion C6.1 (Coding Guidelines) in the current project. Reports fulfillment level 0–2.
allowed-tools: Bash Read
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Verify C6.1 — Coding Guidelines

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | No guidance |
| 1 | Syntax-level standards (formatting, naming, linting rules) |
| 2 | Design principles and patterns (architecture rules, module boundaries, idioms) |

## Evidence to Gather

- Look for coding guideline documents in the repository: CONTRIBUTING.md, STYLE.md, docs/architecture/*, CLAUDE.md, or similar files that describe how code should be written.
- Look for linting and formatting configuration files that encode syntax-level rules (e.g., `.eslintrc`, `.prettierrc`, `ruff.toml`, `pyproject.toml [tool.ruff]`, `.golangci.yml`).
- Look for documents or sections that describe design principles, architectural patterns, module boundary rules, naming idioms beyond basic syntax, or other structural conventions agents should follow.

## Instructions

Gather the evidence described above and determine the fulfillment level for C6.1.

Scoring guide:
- **Level 0**: No coding guidance of any kind — no style guides, no linting config, no contributor guidelines that address code style or structure.
- **Level 1**: Syntax-level standards are documented or encoded — at least one of: a linting/formatting config file exists, a CONTRIBUTING.md or STYLE.md covers naming or formatting conventions, a CLAUDE.md section specifies syntax-level rules. The guidance tells an agent *how code should look* but not *how it should be structured*.
- **Level 2**: Design principles and patterns are additionally documented — at least one of: architecture decision records, a documented module/layer structure with stated rules (e.g., "controllers must not call repositories directly"), idiomatic pattern guidance (e.g., preferred error-handling approach, preferred abstraction patterns), or a CLAUDE.md section that covers structural and design expectations. Level 1 requirements must also be met.

Report in exactly this format:

**C6.1 — Coding Guidelines**
- **Level**: [0 / 1 / 2]
- **Rationale**: [one or two sentences citing the specific evidence]
