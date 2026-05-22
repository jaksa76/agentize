---
name: verify-c5-2
description: Verify readiness criterion C5.2 (Unit Test Coverage) in the current project. Reports fulfillment level 0–3.
allowed-tools: Bash Read
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Verify C5.2 — Unit Test Coverage

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | No unit tests |
| 1 | Some tests present (<50% coverage) |
| 2 | ≥50% coverage |
| 3 | ≥80% coverage |

## Evidence to Gather

- Look for test directories and test files to assess whether tests exist and estimate their volume relative to the codebase.
- Look for coverage configuration or threshold settings in the test framework configuration files.
- Check for existing coverage report artifacts (coverage directories, lcov files, etc.).
- Look for a CI step that measures or enforces coverage.

## Instructions

Gather the evidence described above and determine the fulfillment level for C5.2.

Scoring guide:
- **Level 0**: No unit test files exist anywhere in the repository.
- **Level 1**: Unit test files exist but coverage is below 50%, or coverage is not measured/configured. Existence of test files without a coverage report or threshold config is a strong indicator of Level 1.
- **Level 2**: Coverage is configured at ≥50% or a coverage report shows ≥50% line/statement coverage. A threshold config enforcing ≥50% in jest, pytest-cov, or similar qualifies.
- **Level 3**: Coverage is configured at ≥80% or a coverage report shows ≥80% line/statement coverage. A threshold config enforcing ≥80% qualifies.

If no coverage reports or thresholds exist, estimate based on the number of test files relative to the overall codebase size. Err toward a lower level when uncertain.

Report in exactly this format:

**C5.2 — Unit Test Coverage**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [one or two sentences citing the specific evidence]
