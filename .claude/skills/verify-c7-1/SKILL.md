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

## Evidence

### Mock / stub directories
!`find . -maxdepth 5 -type d \( -name "mocks" -o -name "__mocks__" -o -name "stubs" -o -name "fakes" \) 2>/dev/null | grep -v node_modules | grep -v ".git" | head -10 || echo "(no mock/stub directories)"`

### Mock / fixture files
!`find . -maxdepth 6 \( -name "*.mock.*" -o -name "mock_*.py" -o -name "*Mock*.java" -o -name "*Stub*.java" \) 2>/dev/null | grep -v node_modules | grep -v ".git" | head -15 || echo "(no explicit mock files found)"`
!`find . -maxdepth 5 -type d -name "fixtures" 2>/dev/null | grep -v node_modules | head -10 || echo "(no fixtures directories)"`
!`find . -maxdepth 5 -name "*.fixture.*" -o -name "fixtures.json" -o -name "*.fixtures.*" 2>/dev/null | grep -v node_modules | head -10 || echo "(no fixture files)"`

### DB seed scripts
!`find . -maxdepth 5 \( -iname "seed*" -o -iname "*seed*" \) \( -name "*.js" -o -name "*.ts" -o -name "*.py" -o -name "*.sql" -o -name "*.sh" -o -name "*.rb" \) 2>/dev/null | grep -v node_modules | grep -v ".git" | head -15 || echo "(no seed scripts found)"`
!`ls -d db/ database/ prisma/ migrations/ 2>/dev/null || echo "(no db/database/prisma/migrations directory)"`
!`ls prisma/seed.ts prisma/seed.js 2>/dev/null || echo "(no Prisma seed file)"`

### Test-specific docker-compose
!`ls docker-compose.test.yml docker-compose.testing.yml docker-compose.ci.yml docker-compose.override.yml 2>/dev/null || echo "(no test-specific docker-compose)"`

### Sandbox / vendor environment indicators
!`grep -r -i "testcontainer\|localstack\|wiremock\|mockserver\|test-db\|test_db\|DATABASE_URL.*test\|TEST_DATABASE" .github/workflows/ docker-compose*.yml 2>/dev/null | head -10 || echo "(no sandbox/testcontainers patterns)"`
!`cat package.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); deps={**d.get('dependencies',{}),**d.get('devDependencies',{})}; iso=[k for k in deps if any(x in k for x in ['testcontainer','localstack','wiremock','nock','msw','sinon'])]; print('Isolation deps:', iso if iso else 'none')" 2>/dev/null || true`

## Instructions

Analyse the evidence above and determine the fulfillment level for C7.1.

If the project has no database and no external service dependencies (e.g., it is a pure library or a purely in-memory tool), state "N/A — no external dependencies" rather than assigning a level.

Scoring guide:
- **Level 0**: The project has external dependencies (DB, third-party APIs) but no isolation mechanism — tests hit real production data or live external services, or no test isolation is set up at all.
- **Level 1**: In-code mocks, stubs, or basic fixtures exist — mock objects, stub files, fixture JSON, or mocking libraries (sinon, nock, unittest.mock) are used in tests to isolate from external systems. No reproducible DB state is required.
- **Level 2**: Reproducible database state via seed scripts (prisma seed, SQL seed files, factory-boy, etc.) AND/OR vendor sandbox environments (Testcontainers, LocalStack, docker-compose for test DBs, or vendor-provided sandbox endpoints) are in use. Both the data and the external system boundary are controlled.

Report in exactly this format:

**C7.1 — Test Isolation**
- **Level**: [0 / 1 / 2 / N/A]
- **Rationale**: [one or two sentences citing the specific evidence]
