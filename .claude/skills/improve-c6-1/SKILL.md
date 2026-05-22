---
name: improve-c6-1
description: Improve readiness criterion C6.1 (Coding Guidelines) in the current project by adding syntax standards or design principles documentation. Raises the fulfillment level by one step.
allowed-tools: Bash Read Write Edit
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Improve C6.1 — Coding Guidelines

## Current State

Examine the project to understand its current state:

- Read CLAUDE.md, CONTRIBUTING.md, STYLE.md, and any docs/architecture/* files for existing coding guidance.
- Look for linting and formatting configuration files (standalone files or embedded in a project config) that encode syntax-level rules.
- Identify the language, framework, and architectural patterns already in use in the codebase — these will inform what design principles to document.

## Instructions

**Step 1 — Determine current level:**
- Level 0: No coding guidance of any kind
- Level 1: Syntax-level standards documented or encoded (formatting, naming, linting config)
- Level 2: Design principles and patterns additionally documented

**Step 2 — Implement the improvement:**

**If current level is 0 → raise to 1:**
Add syntax-level coding standards. Prefer encoding rules in a linting config (they are machine-enforceable) and summarising them in CLAUDE.md or CONTRIBUTING.md so agents can read them directly.

- **Node.js/TypeScript**: Add ESLint + Prettier configs (`.eslintrc` or `eslint.config.mjs`, `.prettierrc`). Add a "Code Style" section to CLAUDE.md covering naming conventions (e.g., camelCase for variables, PascalCase for types), file naming, and import ordering.
- **Python**: Add `ruff.toml` or `[tool.ruff]` in `pyproject.toml` with standard rules. Add a "Code Style" section to CLAUDE.md covering naming (snake_case, UPPER_CASE constants), docstring format, and import ordering.
- **Go**: Add `.golangci.yml`. Note that Go enforces formatting via `gofmt`; add a "Code Style" section to CLAUDE.md covering package naming, error wrapping conventions, and comment style.
- **Other languages**: Add the idiomatic linter for the detected language and document the key syntax conventions in CLAUDE.md.

If CLAUDE.md does not exist, create a minimal one with a "Code Style" section only. Do not fabricate conventions — derive them from the existing codebase.

**If current level is 1 → raise to 2:**
Add design principles and architectural pattern documentation. The goal is to tell an agent *how the system should be structured*, not just how code should look.

1. Read the existing codebase to identify the actual architectural patterns in use:
   - Layer structure (e.g., controllers → services → repositories)
   - Module/package boundaries and dependency direction rules
   - Preferred error-handling approach
   - Preferred abstraction patterns (e.g., interface-first, composition over inheritance)
   - Key idioms specific to the framework in use

2. Add a "Architecture and Design Principles" section to CLAUDE.md (or a dedicated `docs/ARCHITECTURE.md` linked from CLAUDE.md) that documents:
   - The layer or module structure with explicit dependency direction rules
   - One or two key design principles the codebase follows (e.g., "services must not import from controllers", "prefer pure functions for business logic")
   - The idiomatic patterns for the main framework in use (e.g., React component patterns, Django view patterns, Go interface patterns)

   Do not invent principles that are not reflected in the existing code. Document what is actually there.

**If already at level 2:**
Report that C6.1 is already at its maximum level (2) and no improvement is needed.

**Step 3 — Report:**
State what files were created or modified, and the before and after level.
