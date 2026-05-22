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

## Evidence

### Integration test directories and files
!`find . -maxdepth 5 -type d \( -name "integration" -o -name "integration-tests" -o -name "integration_tests" \) 2>/dev/null | grep -v node_modules | grep -v ".git" | head -10 || echo "(no integration test directories)"`
!`find . -maxdepth 6 \( -iname "*integration*" \) \( -name "*.test.*" -o -name "*.spec.*" -o -name "*_test.*" -o -name "test_*" \) 2>/dev/null | grep -v node_modules | grep -v ".git" | head -15 || echo "(no integration test files)"`

### E2E test framework config
!`ls cypress.json cypress.config.js cypress.config.ts playwright.config.ts playwright.config.js playwright.config.mts wdio.conf.js 2>/dev/null || echo "(no Cypress, Playwright, or WebdriverIO config)"`

### E2E test directories
!`ls -d cypress/ e2e/ tests/e2e/ __tests__/e2e/ test/e2e/ features/ 2>/dev/null || echo "(no E2E test directories)"`
!`find . -maxdepth 5 -type d -name "e2e" 2>/dev/null | grep -v node_modules | head -10 || true`

### E2E test files (sample)
!`find . -maxdepth 6 \( -iname "*e2e*" -o -iname "*end-to-end*" \) \( -name "*.test.*" -o -name "*.spec.*" -o -name "*.feature" \) 2>/dev/null | grep -v node_modules | head -15 || echo "(no E2E test files found)"`

### Visual regression tooling
!`ls -d .percy/ snapshots/ __image_snapshots__/ screenshot-diffs/ 2>/dev/null || echo "(no visual regression artifact directories)"`
!`cat package.json 2>/dev/null | python3 -c "
import sys, json
d = json.load(sys.stdin)
deps = {**d.get('dependencies', {}), **d.get('devDependencies', {})}
vr = [k for k in deps if any(x in k for x in ['percy', 'chromatic', 'storybook', 'loki', 'reg-suit', 'image-snapshot'])]
print('Visual regression deps:', vr if vr else 'none')
" 2>/dev/null || true`

### E2E / testing deps in package.json
!`cat package.json 2>/dev/null | python3 -c "
import sys, json
d = json.load(sys.stdin)
deps = {**d.get('dependencies', {}), **d.get('devDependencies', {})}
e2e = [k for k in deps if any(x in k for x in ['cypress', 'playwright', 'puppeteer', 'selenium', 'webdriver', 'nightwatch', 'testcafe'])]
print('E2E deps:', e2e if e2e else 'none')
" 2>/dev/null || true`

## Instructions

Analyse the evidence above and determine the fulfillment level for C5.3.

Scoring guide:
- **Level 0**: No integration or E2E test files or directories exist; no E2E framework is configured.
- **Level 1**: Integration tests exist covering key service or module boundaries — e.g., tests that call a real database, hit a real HTTP endpoint, or cross a service boundary. An `integration/` directory with test files qualifies, even without E2E browser tests.
- **Level 2**: E2E tests exist that exercise critical user flows through the running application — browser-based (Cypress, Playwright) or API-level E2E tests. A configured E2E framework with test files qualifies.
- **Level 3**: E2E tests exist AND visual regression testing is set up (Percy, Chromatic, image snapshot comparison). If the project has no UI, Level 2 is the maximum achievable — note this in the rationale.

Report in exactly this format:

**C5.3 — Integration and E2E Coverage**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [one or two sentences citing the specific evidence]
