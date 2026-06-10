---
name: verify-c7-1
description: Verify readiness criterion C7.1 (Test Isolation) in the current project. Reports fulfillment level 0–2.
allowed-tools: Bash Read
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Verify C7.1 — Test Isolation

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | No isolation from external systems or data |
| 1 | In-code mocks/stubs and basic fixtures |
| 2 | Reproducible DB state via seed scripts + sandbox environments from vendors |

Note: This criterion may be omitted for projects without a database or external dependencies. If the project has no external dependencies, note this and report N/A rather than Level 0.

## Evidence to Gather

First determine whether the project has external dependencies (database, third-party APIs). If it has none, the criterion is N/A — note this and stop.

- Look for mock or stub directories and files in the test tree.
- Look for fixture directories and fixture data files.
- Look for seed scripts for populating a test database.
- Look for test-specific container configuration (docker-compose for tests, Testcontainers, LocalStack, etc.).
- Check dependency manifests for test isolation or mocking libraries.

## Instructions

Gather the evidence described above and determine the fulfillment level for C7.1.

If the project has no database and no external service dependencies (e.g., it is a pure library or a purely in-memory tool), state "N/A — no external dependencies" rather than assigning a level.

Scoring guide:
- **Level 0**: The project has external dependencies (DB, third-party APIs) but no isolation mechanism — tests hit real production data or live external services, or no test isolation is set up at all.
- **Level 1**: In-code mocks, stubs, or basic fixtures exist — mock objects, stub files, fixture JSON, or mocking libraries (sinon, nock, unittest.mock) are used in tests to isolate from external systems. No reproducible DB state is required.
- **Level 2**: Reproducible database state via seed scripts (prisma seed, SQL seed files, factory-boy, etc.) AND/OR vendor sandbox environments (Testcontainers, LocalStack, docker-compose for test DBs, or vendor-provided sandbox endpoints) are in use. Both the data and the external system boundary are controlled.

Report in exactly this format:

**C7.1 — Test Isolation**
- **Level**: [0 / 1 / 2 / N/A]
- **Rationale**: [one or two sentences citing the specific evidence]
