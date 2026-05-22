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

## Evidence

### Test directories
!`find . -maxdepth 4 -type d \( -name "test" -o -name "tests" -o -name "__tests__" -o -name "spec" -o -name "specs" \) 2>/dev/null | grep -v node_modules | grep -v ".git" | head -20 || echo "(no test directories found)"`

### Test file count (sample)
!`find . -maxdepth 6 \( -name "*.test.ts" -o -name "*.test.js" -o -name "*.test.tsx" -o -name "*.spec.ts" -o -name "*.spec.js" -o -name "*_test.py" -o -name "test_*.py" -o -name "*Test.java" -o -name "*_test.go" \) 2>/dev/null | grep -v node_modules | grep -v ".git" | wc -l`
!`find . -maxdepth 6 \( -name "*.test.ts" -o -name "*.test.js" -o -name "*.test.tsx" -o -name "*.spec.ts" -o -name "*.spec.js" -o -name "*_test.py" -o -name "test_*.py" -o -name "*Test.java" -o -name "*_test.go" \) 2>/dev/null | grep -v node_modules | grep -v ".git" | head -20`

### Coverage configuration / thresholds
!`cat jest.config.js jest.config.ts jest.config.mjs 2>/dev/null | grep -A5 -i "coverage\|threshold" | head -30 || echo "(no Jest config)"`
!`cat package.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); j=d.get('jest',{}); print('jest.coverageThreshold:', j.get('coverageThreshold','(not set)'))" 2>/dev/null || true`
!`grep -A10 "\[tool.coverage\|coverageThreshold\|minimum_coverage\|fail_under" pyproject.toml setup.cfg .coveragerc 2>/dev/null | head -20 || echo "(no Python coverage threshold config)"`

### Existing coverage reports / artifacts
!`ls coverage/ htmlcov/ .coverage coverage.xml lcov.info 2>/dev/null && echo "Coverage artifacts present" || echo "(no coverage artifacts found)"`
!`head -5 coverage/coverage-summary.json 2>/dev/null || cat coverage/lcov-report/index.html 2>/dev/null | grep -o "[0-9]*\.[0-9]*%" | head -5 || echo "(no parseable coverage summary)"`

### CI coverage step
!`grep -r -i "coverage\|--cov\|istanbul\|nyc" .github/workflows/ 2>/dev/null | head -10 || echo "(no coverage steps in CI)"`

## Instructions

Analyse the evidence above and determine the fulfillment level for C5.2.

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
