---
name: verify-c5-3
description: Verify readiness criterion C5.3 (Integration and E2E Coverage) in the current project. Reports fulfillment level 0–3.
allowed-tools: Bash Read
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Verify C5.3 — Integration and E2E Coverage

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | No automated integration or E2E tests |
| 1 | Integration tests cover key boundaries |
| 2 | E2E tests cover critical flows |
| 3 | E2E + UI visual regression (if UI present) |

Note: Level 3 (UI visual regression) may be omitted for projects without a UI — such projects max out at Level 2 if they have E2E coverage.

## Evidence to Gather

- Look for integration test directories or files (directories or files with "integration" in the name, or tests that reference real databases/APIs).
- Look among the configuration files and dependency manifests for any sign of E2E or browser testing tools.
- Look for E2E test directories and files.
- Look for visual regression testing configuration, snapshot directories, or visual testing dependencies.

## Instructions

Gather the evidence described above and determine the fulfillment level for C5.3.

Scoring guide:
- **Level 0**: No integration or E2E test files or directories exist; no E2E framework is configured.
- **Level 1**: Integration tests exist covering key service or module boundaries — e.g., tests that call a real database, hit a real HTTP endpoint, or cross a service boundary. An `integration/` directory with test files qualifies, even without E2E browser tests.
- **Level 2**: E2E tests exist that exercise critical user flows through the running application — browser-based (Cypress, Playwright) or API-level E2E tests. A configured E2E framework with test files qualifies.
- **Level 3**: E2E tests exist AND visual regression testing is set up (Percy, Chromatic, image snapshot comparison). If the project has no UI, Level 2 is the maximum achievable — note this in the rationale.

Report in exactly this format:

**C5.3 — Integration and E2E Coverage**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [one or two sentences citing the specific evidence]
