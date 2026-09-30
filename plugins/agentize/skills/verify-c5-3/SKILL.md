---
name: verify-c5-3
description: Verify readiness criterion C5.3 (Integration and E2E Coverage) in the current project, including whether the tests are maintained, actually run, and cover the critical flows. Reports fulfillment level 0–3.
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

**Tests only count if they are alive.** The point of this criterion is that an agent can rely on these tests to catch regressions. Test files that are never run, that fail against the current system, or that nobody has maintained while the code moved on give the agent no signal, so they do not raise the level. Existence of test files or a configured framework is never enough on its own.

## Evidence to Gather

### 1. Discovery

- Look for integration test directories or files (directories or files with "integration" in the name, or tests that reference real databases/APIs).
- Look among the configuration files and dependency manifests for any sign of E2E or browser testing tools.
- Look for E2E test directories and files.
- Look for visual regression testing configuration, snapshot directories, or visual testing dependencies.
- If tests live in a separate repository from the code they test, treat that repository as part of the project.

### 2. Maintenance signals

Do this for every suite found (integration, E2E, mobile UI, visual regression separately).

- **Last real change.** Find the last commit that touched the suite's directory (`git log -1 --format=%cs -- <test-dir>`) and how many commits touched it in the last 6 months. Read what those commits changed: formatting, warning fixes, dependency bumps, renames and other mechanical edits are not maintenance. A commit that adds or changes test logic, fixtures or selectors is.
- **Drift.** Count commits to the code under test since the last real test change (`git rev-list --count <last-test-commit>..HEAD -- <src-dir>`). A suite untouched for 6 months or more while the code kept changing is presumed stale until a run shows otherwise.
- **Executed by CI.** Read the pipeline definitions. A pipeline that only builds, restores or publishes the test binaries does not execute the tests. Look for an actual test step (`dotnet test`, `pytest`, `playwright test`, `cypress run`, `mvn verify`, `gradle connectedCheck`, ...). If pipeline history is accessible, find the most recent run that executed the suite and whether it passed.
- **Disabled tests.** Count tests marked skipped or ignored (`[Ignore]`, `@Disabled`, `test.skip`, `xit`, `pytest.mark.skip`, category filters that exclude them) as a share of all tests.
- **Dangling targets.** Spot-check at least 5 tests: do the routes, endpoints, pages, selectors or screens they reference still exist in the current source?

### 3. Experimental run (primary evidence)

Try to run every suite. Do not rely on reading test files when a run is possible.

- Run in a container, not on the host machine: use the project's devcontainer or compose setup if there is one, otherwise a suitable SDK/runtime image.
- If the tests need a running application, bring the application up first the way C5.1 does (all services together for a distributed system, with local databases, emulators or mocks for the dependencies) and point the tests at it through their own configuration (environment variables, base URLs, test accounts). Seed the test data the suite expects if seed scripts exist.
- Do not edit test code to make tests pass. Configuration, environment variables, URLs and seed data may be set up, and every such step must be recorded.
- Record, per suite: the command used, the environment, and the numbers of tests discovered, executed, passed, failed, skipped and errored.
- Classify each failure:
  - **Stale**: the app is running correctly but the test fails on an assertion, a 404 or missing route, a missing UI element or selector, or a schema mismatch. This shows the suite has rotted.
  - **Environment**: the test cannot reach a dependency it needs (identity provider, live third-party API, cloud-only service, credentials) even though the app is up. This does not show rot, but the suite is unverified.
- Time-box the attempt to a reasonable effort. If a suite cannot be executed, record exactly what blocked it. That result is "not verified experimentally" and triggers the caps below. It is not a pass.
- Classify the run: **healthy** (at least 80% of executed tests pass), **degraded** (50–80%), **broken** (below 50%), or **not verified** (could not be executed).

### 4. Coverage of boundaries and critical flows

- Inventory what should be covered: the public API surface (OpenAPI, controllers, routes), the services and data stores, and the critical user flows (from architecture, functionality or requirements docs, or the main pages, screens and roles).
- Map tests onto that inventory:
  - Integration: which services, endpoints or modules and which boundaries (database, service-to-service call, external API) are exercised.
  - E2E: which user journeys, per role and per client (web, mobile), are exercised.
- If tooling is available, measure instead of estimating (code coverage of the service under test while the suite runs, route coverage from access logs).
- State the covered share of critical flows and name the roles or clients with no E2E test.

## Instructions

Gather the evidence described above and determine the fulfillment level for C5.3.

A suite is **active** when it is not stale, and either it ran healthy in the experiment or CI ran it and it passed within the last 6 months. A suite is **stale** when the experiment shows stale failures or it has had no real change for 6 months or more while the code it targets kept changing.

Scoring guide:
- **Level 0**: No integration or E2E tests exist, or the tests that exist are dead: they do not run, or fail on a majority of executed tests for stale reasons, or are unverified and show no CI execution and no real change in 6 months.
- **Level 1**: An active integration suite exists and covers the project's key boundaries: its data store, service-to-service calls and public API, roughly a quarter or more of the API surface or services, not a handful of smoke tests. A suite that cannot be executed experimentally may still reach Level 1, marked unverified, if CI executes it or it had a real change within the last 6 months.
- **Level 2**: Level 1 is met, and an active E2E suite exercises the critical user flows through the running application (browser-based, API-level or mobile UI): at least half of the identified critical flows, and every primary client type (for example web and mobile) has at least one E2E test. Its run is healthy, or CI executes it and it passed within the last 6 months. A configured E2E framework with test files, or E2E tests that nobody runs, do not qualify.
- **Level 3**: Level 2 is met AND visual regression testing is set up and active: baseline snapshots exist, the comparison is executed in CI or in the experiment, and it passes (Percy, Chromatic, image snapshot comparison). If the project has no UI, Level 2 is the maximum achievable — note this in the rationale.

Caps that apply whatever the file counts say:
- Suite not verified experimentally and not executed by CI: at most Level 1.
- Suite whose run is broken: counts as Level 0 for that suite.
- E2E covering less than half of the critical flows, or a primary client type with no E2E test: cap at Level 1 and say E2E is partial. Below a quarter, call it incidental.

If the project is composed of multiple services/repositories, evaluate each test suite and the service it protects in a separate context using subagents if available, then aggregate and weight the results by how critical each service is.

The 6-month and percentage thresholds are guidance. If the evidence points clearly the other way (for example a stable suite that passes cleanly against the current app is not stale just because it is old), use judgment and say why.

Report in exactly this format:

**C5.3 — Integration and E2E Coverage**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [two or three sentences citing the specific evidence: the experimental result (executed/passed/failed, or what blocked the run), when the suite was last really changed and whether CI runs it, and the share of boundaries or critical flows covered]
