---
name: improve-c5-3
description: Improve readiness criterion C5.3 (Integration and E2E Coverage) in the current project by adding integration or E2E test infrastructure. Raises the fulfillment level by one step.
allowed-tools: Bash Read Write Edit
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Improve C5.3 — Integration and E2E Coverage

## Current State

### E2E framework
!`ls cypress.config.js cypress.config.ts playwright.config.ts playwright.config.js 2>/dev/null || echo "(no E2E framework config)"`
!`ls -d cypress/ e2e/ tests/e2e/ 2>/dev/null || echo "(no E2E directories)"`

### Integration tests
!`find . -maxdepth 5 -type d -name "integration" 2>/dev/null | grep -v node_modules | head -5 || echo "(no integration test directory)"`
!`find . -maxdepth 6 \( -iname "*integration*" \) \( -name "*.test.*" -o -name "*.spec.*" -o -name "*_test.*" \) 2>/dev/null | grep -v node_modules | head -10 || echo "(no integration test files)"`

### Visual regression
!`cat package.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); deps={**d.get('dependencies',{}),**d.get('devDependencies',{})}; vr=[k for k in deps if any(x in k for x in ['percy','chromatic','image-snapshot'])]; print('Visual regression deps:', vr)" 2>/dev/null || true`

### App type / endpoints
!`cat package.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); deps={**d.get('dependencies',{}),**d.get('devDependencies',{})}; web=[k for k in deps if any(x in k for x in ['express','fastify','koa','hono','next','react','vue','angular','svelte'])]; print('Web deps:', web)" 2>/dev/null || true`
!`grep -r "app\.\(get\|post\|put\|delete\)\|router\.\(get\|post\)" --include="*.ts" --include="*.js" -h . 2>/dev/null | grep -v node_modules | head -15 || echo "(no route definitions)"`
!`ls -d tests/ test/ __tests__/ 2>/dev/null || echo "(no test directory)"`

## Instructions

**Step 1 — Determine current level:**
- Level 0: No integration or E2E tests
- Level 1: Integration tests cover key boundaries
- Level 2: E2E tests cover critical flows
- Level 3: E2E + UI visual regression (N/A without a UI)

**Step 2 — Implement the improvement:**

**If current level is 0 → raise to 1:**
Create integration tests covering key service boundaries. Based on the detected project type:

- **REST API (Express/Fastify/etc.)**: Create `tests/integration/` directory and write integration tests using `supertest` (Node) or `pytest` with test client (Python/FastAPI). Test the main endpoints with real HTTP calls. Add `supertest` to devDependencies if not present.

  Example test structure:
  ```
  tests/integration/
    api.test.ts       — tests for main API routes
  ```

- **Database-backed service**: Write tests that connect to a real (test) database and verify data operations. Use a test database connection string.

- **Library/module**: Write tests that exercise the public API with real dependencies (not mocked) to verify integration points work end-to-end.

Write at minimum 5–10 integration tests covering the most important boundaries.

**If current level is 1 → raise to 2:**
Add E2E test infrastructure. Based on the detected project type:

- **Web app with UI**: Install and configure Playwright (preferred over Cypress for new setups):
  1. Add `@playwright/test` to devDependencies
  2. Create `playwright.config.ts` with base URL pointing to localhost and the detected port
  3. Create `e2e/` directory with basic tests for the main user flows (login if present, main feature flow, navigation)
  4. Add `"test:e2e": "playwright test"` to package.json scripts

- **API-only**: Extend existing integration tests to cover full request/response cycles including authentication, error handling, and multi-step operations (e.g., create → read → update → delete).

Write at minimum 3–5 E2E scenarios for the most critical user flows.

**If current level is 2 → raise to 3:**
If the project has a UI, add visual regression testing:
1. Add `@percy/playwright` or `@storybook/test-runner` with Chromatic to devDependencies
2. Add visual snapshot assertions to existing E2E tests for key pages/states
3. Configure Percy/Chromatic token as an environment variable (add to `.env.example`)

If the project has no UI, report that Level 3 is not applicable (maximum is Level 2 for API-only projects).

**If already at level 3 (or at level 2 with no UI):**
Report the current state and that no improvement is needed.

**Step 3 — Report:**
State what files were created or modified, the before and after level.
