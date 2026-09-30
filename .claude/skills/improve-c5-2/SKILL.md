---
name: improve-c5-2
description: Improve readiness criterion C5.2 (Unit Test Coverage) in the current project by generating unit tests for untested code.
allowed-tools: Bash Read Write Edit
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Improve C5.2 — Unit Test Coverage

This skill generates unit tests for untested or under-tested code in the current project, improving overall test coverage and ensuring code quality.

## Step 0

If the project is a multi-repository setup, perform the above in each repository independently using subagents. This step is not necessary for repos that do not contain code (e.g. infrastructure, documentation, etc.).

## Execution environment

Run all test and coverage commands (installing dependencies, measuring coverage, running the generated tests) in a devcontainer when the project has one (`.devcontainer/devcontainer.json`), not on the host machine.
- First check whether you are already running inside a devcontainer (e.g. `REMOTE_CONTAINERS` or `CODESPACES` environment variable set, or `/.dockerenv` present). If so, run commands directly.
- Otherwise, start the devcontainer with `devcontainer up --workspace-folder <repo>` and run commands with `devcontainer exec --workspace-folder <repo> <command>`.
- If the project has no devcontainer, run the commands in a suitable container image for the project's language/runtime instead of on the host.
- In a multi-repository setup, determine this for each repository separately.

## Step 1 - Evaluate situation
- Check for existing test framework and configuration.
- identify any existing patterns used in the tests (naming conventions, test structure, helper functions, fixtures, mocking strategies, etc.)
- If the tests are present, measure coverage and identify gaps.
- Identify the high priority untested or under-tested source files (containing business logic, edge cases, or complex logic).

## Step 2 - Generate Tests
Set up a testing framework and coverage tool if missing.

If this is not a multi-repository setup, subdivide the high priority untested or under-tested source files into smaller, manageable disjoint sets for testing and use parallel subagents to generate tests for each set simultaneously. Keep the number of subagents limited to avoid collisions.

- perform minimal refactoring for testability if necessary (dependency injection, breaking large units into smaller ones, etc.)
- if the code requires major refactoring for testability, skip the file and move on to the next one.
- Write the generated tests following the identified patterns and conventions.
- Run the tests and verify that they pass successfully.
- Ensure that the tests cover all significant edge cases and previously untested or under-tested code.
- Fix any bugs identified during testing.
- If the bug is complicated and requires significant changes to the logic, disable or remove the test and report it.
- Prefer the GIVEN...WHEN...THEN pattern for structuring tests.
- Assert observable behavior, not implementation.
- Keep tests deterministic, with no network, clock or filesystem dependence.
- Mock only at boundaries.
- Write meaningful assertions, not just execution.

## Step 3 - Review and Integrate
- Verify if integration or e2e tests are affected by the new unit tests and fix any issues that arise.
- Add unit tests to CI pipeline if necessary.
- Measure coverage and ensure it meets a reasonable threshold.
- If there is a CLAUDE.md or AGENTS.md file, make sure it mandates writing of unit tests for all new and modified code.

## Step 4 - Report
- Document the newly added tests and their coverage.
- Report any major refactorings made during the process.
- Report about any bugs found during testing.
- Highlight any remaining gaps in test coverage and suggest actions to address them.


# Multirepo Setup

