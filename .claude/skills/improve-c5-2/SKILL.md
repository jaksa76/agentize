---
name: improve-c5-2
description: Improve readiness criterion C5.2 (Unit Test Coverage) in the current project by generating unit tests for untested code. Raises the fulfillment level by one step.
allowed-tools: Bash Read Write Edit
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Improve C5.2 — Unit Test Coverage

## Current State

Examine the project to understand its current state:

- Identify the test framework from the dependency manifest or framework configuration files.
- Look for existing test directories and test files to understand what is already tested.
- Look for coverage configuration or threshold settings.
- Look for existing coverage reports to understand current coverage level.
- Look at the source directories to identify untested code that needs tests.

## Instructions

**Step 1 — Determine current level:**
- Level 0: No unit test files exist
- Level 1: Test files exist but coverage < 50% (or no coverage measurement)
- Level 2: ≥ 50% coverage configured or evidenced
- Level 3: ≥ 80% coverage configured or evidenced

**Step 2 — Read source files before writing tests:**
Identify the 3–5 most important untested source files (business logic, utilities, services — not configuration or entry points). Read each file fully before writing tests for it.

**Step 3 — Implement the improvement:**

**If current level is 0 → raise to 1:**
1. If no test framework is configured, add one appropriate to the language:
   - Node/TS: add `jest` and `@types/jest` to devDependencies in package.json, add jest config, add `"test": "jest"` script
   - Python: ensure `pytest` is in requirements/pyproject.toml
2. Write unit tests for the 3–5 most important source files identified above. Place them in the appropriate test directory (`tests/`, `__tests__/`, or alongside source with `.test.ts` suffix).
3. Each test file should have at minimum 3–5 test cases covering the main happy path and one edge case per function/method.

**If current level is 1 → raise to 2:**
1. Add a coverage threshold of 50% to the test config:
   - Jest: add `coverageThreshold: { global: { lines: 50 } }` to jest.config
   - pytest: add `[tool.coverage.report] fail_under = 50` to pyproject.toml
2. Identify the untested or under-tested source files from the file list above (files with no corresponding test file).
3. Write additional unit tests for the top 5 untested files, focusing on functions with clear inputs and outputs.

**If current level is 2 → raise to 3:**
1. Raise the coverage threshold to 80%:
   - Jest: update `coverageThreshold` to 80
   - pytest: update `fail_under` to 80
2. Identify gaps: find source files with corresponding test files but with clearly low coverage (look for files with many functions but few test cases).
3. Expand existing tests with additional cases: boundary conditions, error paths, and edge cases for the most critical functions.

**If already at level 3:**
Report that C5.2 is already at its maximum level (3) and no improvement is needed.

**Step 4 — Report:**
State what test files were created or modified, what coverage threshold was set, the before and after level.
