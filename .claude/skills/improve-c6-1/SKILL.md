---
name: improve-c6-1
description: Improve readiness criterion C6.1 (Static Analysis) in the current project by adding linting, type checking, or security scanning. Raises the fulfillment level by one step.
allowed-tools: Bash Read Write Edit
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Improve C6.1 — Static Analysis

## Current State

Examine the project to understand its current state:

- Identify the language and build system from the dependency manifest.
- Look for linting and formatting configuration files (standalone files or embedded in a project config).
- Look for type checking configuration files and check whether strict mode is enabled.
- Look for security scanning (SAST) configuration files and CI steps.
- Check the build scripts/Makefile to understand what quality commands already exist.

## Instructions

**Step 1 — Determine current level:**
- Level 0: No quality tooling
- Level 1: Linting and/or formatting configured
- Level 2: + Type checking enforced
- Level 3: + Security scanning (SAST)

**Step 2 — Implement the improvement:**

**If current level is 0 → raise to 1:**
Add linting appropriate to the detected language:

- **Node.js/TypeScript**: Add ESLint + Prettier.
  1. Add to package.json devDependencies: `eslint`, `@eslint/js`, `prettier`, `eslint-config-prettier`
  2. Create `eslint.config.mjs` with sensible defaults for the detected framework
  3. Create `.prettierrc` with standard formatting rules
  4. Add scripts: `"lint": "eslint src/"` and `"format": "prettier --write src/"`

- **Python**: Add Ruff (covers linting + formatting in one tool).
  1. Create `ruff.toml` or add `[tool.ruff]` section to pyproject.toml
  2. Configure standard rules (E, F, I at minimum)
  3. Add to Makefile or pyproject.toml scripts: `lint: ruff check .`

- **Go**: Add golangci-lint.
  1. Create `.golangci.yml` with standard linters (errcheck, gosimple, govet, staticcheck)
  2. Add lint step comment to Makefile if present

- **Java**: Add Checkstyle config if using Maven/Gradle.

**If current level is 1 → raise to 2:**
Add type checking appropriate to the detected language:

- **TypeScript (package.json exists, tsconfig.json missing)**: Create `tsconfig.json` with:
  ```json
  { "compilerOptions": { "strict": true, "noImplicitAny": true, ... } }
  ```
  Add `"typecheck": "tsc --noEmit"` to package.json scripts.

- **TypeScript (tsconfig.json exists but not strict)**: Edit tsconfig.json to add `"strict": true` to compilerOptions. Fix any immediate type errors if they are simple. Add `"typecheck": "tsc --noEmit"` script if missing.

- **Python**: Create `mypy.ini` or add `[tool.mypy]` to pyproject.toml with `strict = true` or at minimum `disallow_untyped_defs = true`. Add lint step: `mypy src/`.

- **Go**: Go has built-in type checking — note that `go vet` enforces this. Add a `vet` step to Makefile if not present.

**If current level is 2 → raise to 3:**
Add security scanning via GitHub Actions CodeQL (works for most languages, requires no external account):

1. Create `.github/workflows/codeql.yml`:
```yaml
name: CodeQL
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 8 * * 1'
jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v3
        with:
          languages: [detected-language]
      - uses: github/codeql-action/autobuild@v3
      - uses: github/codeql-action/analyze@v3
```

Replace `[detected-language]` with the appropriate CodeQL language identifier (javascript, python, java, go, etc.).

**If already at level 3:**
Report that C6.1 is already at its maximum level (3) and no improvement is needed.

**Step 3 — Report:**
State what files were created or modified, the before and after level.
