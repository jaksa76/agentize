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

### Test discovery

Search for unit tests using the conventions of the detected language. Absence of tests in one convention is not evidence of absence — check every convention that applies to the languages present in the repository.

| Language | Where unit tests live |
|---|---|
| Java / Kotlin | `src/test/java/`, `src/test/kotlin/` (also per-module: `*/src/test/java/`) |
| JavaScript / TypeScript | `__tests__/` directories, `*.test.*` and `*.spec.*` files |
| Python | `tests/` directories, `test_*.py` and `*_test.py` files |
| Go | `*_test.go` files, alongside the code they test |
| Generic fallback | directories named `test`, `tests`, `spec`, or `specs` at any depth |

Assess the volume of the tests found relative to the size of the codebase (file counts, test-function counts, lines of test code versus lines of production code).

### Coverage evidence

Look for coverage configuration and coverage reports. Common forms:

- **Java / Kotlin** — JaCoCo configuration in `pom.xml` or `build.gradle(.kts)` (the `jacoco` plugin, `jacocoTestCoverageVerification` rules and limits), and reports at `target/site/jacoco/`, `build/reports/jacoco/`, `jacoco.xml`, or `jacocoTestReport.xml`. Other JVM tools: Cobertura, Kover.
- **JavaScript / TypeScript** — Jest configuration (`jest.config.*` or the `jest` key in `package.json`) including `collectCoverage` and `coverageThreshold`; Vitest `coverage` config; nyc/istanbul `.nycrc`.
- **Python** — `pytest.ini`, `setup.cfg`, `tox.ini`, or `pyproject.toml` sections for `[tool.pytest.ini_options]`, `[tool.coverage.*]`, or a `.coveragerc`; `--cov` flags in the test command; `fail_under` thresholds.
- **Go** — `-coverprofile` flags in build scripts or CI, and the resulting `coverage.out`.
- **Language-agnostic artifacts** — LCOV files (`lcov.info`, `coverage.lcov`), `coverage/`, `htmlcov/`, or `coverage-final.json` directories and files; `cobertura.xml`; coverage upload steps in CI (Codecov, Coveralls, SonarQube) and any thresholds configured there.

An enforced threshold (a build that fails below N%) is stronger evidence than a generated report, which is in turn stronger than configuration that merely enables coverage collection.

### Running the tests

- If the project has a devcontainer or similar, attempt to run unit tests with coverage within that environment to validate the evidence.
- If the app doesn't have a devcontainer, attempt to execute the unit tests within a suitable container, but not on the host machine.

## Instructions

Gather the evidence described above and determine the fulfillment level for C5.2.

Scoring guide:
- **Level 0**: No unit test files exist anywhere in the repository.
- **Level 1**: Unit test files exist but coverage is below 50%, or coverage is not measured/configured. Existence of test files without a coverage report or threshold config is a strong indicator of Level 1.
- **Level 2**: Measured coverage is at ≥50% or a coverage report shows ≥50% line/statement coverage. A threshold config enforcing ≥50% in jest, pytest-cov, or similar qualifies.
- **Level 3**: Measured coverage is at ≥80% or a coverage report shows ≥80% line/statement coverage. A threshold config enforcing ≥80% qualifies.

If you cannot run the unit tests or no coverage reports or thresholds exist, estimate based on the number of test files relative to the overall codebase size. Err toward a lower level when uncertain.

Report in exactly this format:

**C5.2 — Unit Test Coverage**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [one or two sentences citing the specific evidence]