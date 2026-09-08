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

Note: This criterion may be omitted for projects without a database or external dependencies — but only after the external-dependency discovery below has been carried out and found none. If the project genuinely has no external dependencies, note this and report N/A rather than Level 0.

## Evidence to Gather

### Step A — Discover the external dependencies (do this first)

Do not decide whether this criterion applies until the discovery below has actually been performed. Enumerate every database and third-party service the project talks to, drawing on all four sources:

- **Source code** — database clients and ORMs (JDBC, JPA/Hibernate, SQLAlchemy, Prisma, GORM, Mongoose), HTTP and gRPC clients pointed at external hosts, SDK imports for cloud and vendor services (AWS, GCP, Azure, Stripe, Twilio, SendGrid, Auth0), message broker producers and consumers (Kafka, RabbitMQ, SQS), cache clients (Redis, Memcached), and mail or file-storage clients.
- **Dependency manifests** — `package.json`, `pom.xml`, `build.gradle(.kts)`, `requirements.txt`, `pyproject.toml`, `go.mod`, `Gemfile`, `Cargo.toml`. Database drivers, vendor SDKs, and broker clients each imply an external dependency.
- **Configuration** — connection strings and service URLs in `application.properties`/`.yml`, `.env` and `.env.example`, `settings.py`, `config/*.json|yaml`, Helm values and Kubernetes manifests, `docker-compose.yml` service definitions, Terraform resources, and CI secrets whose names point at an external system (`DATABASE_URL`, `STRIPE_API_KEY`, `AWS_ACCESS_KEY_ID`).
- **Documentation** — README setup and prerequisites sections, architecture docs, and runbooks that name a database or third-party service the project requires.

Build an explicit list of the dependencies found. Each entry must be reported, whatever the outcome.

### Step B — Determine how tests handle each dependency

For every dependency on the list, establish whether the test suite isolates it or contacts the real system:

- Look for mock or stub directories and files in the test tree, and for mocking used inline in tests.
- Look for fixture directories and fixture data files.
- Look for seed scripts for populating a test database.
- Look for test-specific container configuration (docker-compose for tests, Testcontainers, LocalStack, WireMock, MockServer, embedded databases such as H2 or `sqlite::memory:`).
- Check dependency manifests for test isolation or mocking libraries (Mockito, sinon, nock, msw, `unittest.mock`, `responses`, `httpretty`, `gomock`).
- Look for the opposite signal too: tests reading a real `DATABASE_URL` or vendor API key from the environment, hitting a live host, or skipping themselves when a credential is missing. That is a test contacting the real system, not isolating it.

## Instructions

Gather the evidence described above and determine the fulfillment level for C7.1.

**Report the dependency inventory first**, as a table listing each database or third-party service found, the evidence for it, and how the tests treat it:

| Dependency | Evidence | Test treatment |
|---|---|---|
| PostgreSQL | `spring.datasource.url` in `application.yml`; `postgresql` driver in `pom.xml` | Testcontainers in `src/test/.../DbIT.java` — isolated |
| Stripe API | `stripe-java` in `pom.xml`; `STRIPE_API_KEY` in CI secrets | live key read in `PaymentIT.java` — contacts the real system |

Only after Step A has been completed and found **no** database and no external service dependency may the criterion be reported as N/A. State that the discovery was performed and what was searched — for example "N/A — no external dependencies: no database driver, vendor SDK, broker client, or service URL found in manifests, configuration, or source". Never report N/A merely because no mocks or fixtures were found; missing isolation around a real dependency is Level 0, not N/A.

Scoring guide:
- **Level 0**: The project has external dependencies (DB, third-party APIs) but no isolation mechanism — tests hit real production data or live external services, or no test isolation is set up at all.
- **Level 1**: In-code mocks, stubs, or basic fixtures exist — mock objects, stub files, fixture JSON, or mocking libraries (sinon, nock, unittest.mock) are used in tests to isolate from external systems. No reproducible DB state is required.
- **Level 2**: Reproducible database state via seed scripts (prisma seed, SQL seed files, factory-boy, etc.) AND/OR vendor sandbox environments (Testcontainers, LocalStack, docker-compose for test DBs, or vendor-provided sandbox endpoints) are in use. Both the data and the external system boundary are controlled.

Report in exactly this format:

**C7.1 — Test Isolation**
- **External dependencies found**: [the inventory table, or "none — discovery performed across source, manifests, configuration, and documentation"]
- **Level**: [0 / 1 / 2 / N/A]
- **Rationale**: [one or two sentences citing the specific evidence]
