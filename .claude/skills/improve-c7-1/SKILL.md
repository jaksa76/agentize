---
name: improve-c7-1
description: Improve readiness criterion C7.1 (Test Isolation) in the current project by adding mocks, fixtures, or seed scripts. Raises the fulfillment level by one step.
allowed-tools: Bash Read Write Edit
---

# Improve C7.1 — Test Isolation

## Current State

### External dependency detection
!`cat package.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); deps={**d.get('dependencies',{}),**d.get('devDependencies',{})}; db=[k for k in deps if any(x in k for x in ['pg','mysql','mongo','redis','prisma','typeorm','sequelize','knex','sqlite'])]; ext=[k for k in deps if any(x in k for x in ['axios','fetch','got','node-fetch','request','stripe','twilio','sendgrid'])]; print('DB deps:', db); print('External API deps:', ext)" 2>/dev/null || true`
!`grep -r "process.env.DATABASE_URL\|mongoose.connect\|createPool\|PrismaClient\|redis.createClient" --include="*.ts" --include="*.js" --include="*.py" -l . 2>/dev/null | grep -v node_modules | head -10 || echo "(no DB connection patterns found)"`

### Existing mocks / fixtures
!`find . -maxdepth 5 -type d \( -name "mocks" -o -name "__mocks__" -o -name "fixtures" -o -name "stubs" \) 2>/dev/null | grep -v node_modules | head -10 || echo "(no mock/fixture directories)"`
!`find . -maxdepth 5 \( -name "*.mock.*" -o -name "mock_*.py" \) 2>/dev/null | grep -v node_modules | head -10 || echo "(no mock files)"`

### Seed scripts
!`find . -maxdepth 5 \( -iname "seed*" \) \( -name "*.js" -o -name "*.ts" -o -name "*.py" -o -name "*.sql" \) 2>/dev/null | grep -v node_modules | head -10 || echo "(no seed scripts)"`
!`ls prisma/seed.ts prisma/seed.js 2>/dev/null || echo "(no Prisma seed)"`

### Test docker-compose
!`ls docker-compose.test.yml docker-compose.testing.yml 2>/dev/null || echo "(no test docker-compose)"`

### Schema / models (for generating seeds)
!`find . -maxdepth 4 \( -name "schema.prisma" -o -name "*.schema.ts" -o -name "models.py" -o -name "schema.sql" \) 2>/dev/null | grep -v node_modules | head -10 || echo "(no schema files found)"`
!`head -60 prisma/schema.prisma 2>/dev/null || echo "(no Prisma schema)"`

## Instructions

**Step 1 — Check applicability:**
If the project has no database and no external API dependencies (it's a pure library, CLI tool, or in-memory system), report "C7.1 is N/A for this project — no external dependencies detected" and stop.

**Step 2 — Determine current level:**
- Level 0: No isolation from external systems
- Level 1: In-code mocks/stubs and basic fixtures exist
- Level 2: Reproducible DB state via seed scripts + sandbox environments

**Step 3 — Implement the improvement:**

**If current level is 0 → raise to 1:**
Add mock infrastructure appropriate to the detected stack:

- **Node.js/TypeScript with external APIs**: Create `src/__mocks__/` or `tests/mocks/` directory. Create mock files for each external dependency detected:
  - HTTP clients: create a Jest manual mock or use `msw` (Mock Service Worker) for API mocking
  - Add `msw` to devDependencies and create `tests/mocks/handlers.ts` with request handlers for detected external API calls
  - Create `tests/fixtures/` with sample response JSON files for detected APIs

- **Node.js/TypeScript with DB**: Create mock implementations for repository/data access classes if they exist. Add `jest.mock()` calls in test setup.

- **Python**: Create `tests/fixtures/` directory with fixture files. If using pytest, create `tests/conftest.py` with fixtures using `unittest.mock.patch` for external dependencies.

Write at least one concrete mock/fixture for each detected external dependency.

**If current level is 1 → raise to 2:**
Add reproducible database state:

- **Prisma**: Create `prisma/seed.ts` that inserts representative test data for each model in the schema. Add `"seed": "ts-node prisma/seed.ts"` to package.json scripts and `"prisma": { "seed": "..." }` to package.json.

- **TypeORM/Sequelize**: Create `src/database/seeds/` directory with seed files that create test data.

- **Python/SQLAlchemy**: Create `tests/fixtures/seed.py` with functions to populate a test database.

- **Any project with a DB**: Create `docker-compose.test.yml` that spins up an isolated test database (Postgres, MySQL, Redis) on a different port from development, using in-memory or tmpfs storage where possible.

Base seed data on the actual models/schema detected in the project.

**If already at level 2:**
Report that C7.1 is already at its maximum level (2) and no improvement is needed.

**Step 4 — Report:**
State what files were created or modified, the before and after level.
