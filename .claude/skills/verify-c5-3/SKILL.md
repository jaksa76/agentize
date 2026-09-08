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

### Integration and E2E test discovery

Integration and E2E tests are frequently separated from unit tests by directory, source set, or annotation rather than by filename. Search every convention that applies to the languages present in the repository — finding no `integration/` directory is not evidence that integration tests are absent.

| Language | Where integration and E2E tests live |
|---|---|
| Java / Kotlin | `src/integrationTest/java/` (and the Gradle `integrationTest` source set that declares it); classes annotated `@SpringBootTest`, `@IntegrationTest`, `@Testcontainers`, `@QuarkusIntegrationTest`; packages named `integration` or `apitest`; Failsafe-bound `*IT.java` / `*ITCase.java` files |
| JavaScript / TypeScript | `test/integration/`, `e2e/`, `cypress/`, `playwright/`; `playwright.config.*`, `cypress.config.*`, `wdio.conf.*`; Jest projects or configs scoped to an integration test match pattern |
| Python | `tests/integration/`, `tests/e2e/`; pytest markers such as `@pytest.mark.integration` or `@pytest.mark.e2e` and their declarations in `pytest.ini` / `pyproject.toml`; `conftest.py` fixtures that start a database or HTTP server |
| Go | build-tagged files (`//go:build integration`) and `TestMain` setups that start external services |
| Generic fallback | any directory or file whose name contains `integration`, `e2e`, `api-test`, or `apitest`, at any depth |

- Look among the configuration files and dependency manifests for any sign of E2E or browser testing tools (Cypress, Playwright, Selenium, WebdriverIO, Puppeteer, REST Assured, Karate, Supertest).
- Distinguish an integration test from an E2E test by what it exercises: an integration test crosses one boundary (a real database, a real HTTP endpoint, a message broker); an E2E test drives a critical user flow through the running application end to end.
- Confirm the tests found are actually wired into a runnable task or CI job — a directory of test files with no way to execute them is weaker evidence than a configured, invoked suite.

### Visual regression evidence

- Look for visual regression configuration and dependencies (Percy, Chromatic, Applitools, BackstopJS, `jest-image-snapshot`, Playwright `toHaveScreenshot`).
- Look for committed snapshot or baseline image directories (`__image_snapshots__/`, `__snapshots__/` containing images, `cypress/snapshots/`, `playwright/*-snapshots/`).

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
