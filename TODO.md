- [ ] When evaluating criteria, read previous evaluation results
- [ ] C1.1 still evaluates to L1 even for disconnected repos
- [ ] add language specific test detection to verify-c5-2
- [ ] 
Update the skills in github.com/jaksa76/agentize so downstream GitHub Copilot distributions can synchronize them safely.

Make these focused changes:

1. Fix C6.1 consistency in `.claude/skills/assess-readiness/SKILL.md`
   - Use the criterion name “Coding Guidelines”, not “Static Analysis”.
   - Set its maximum level to 2, matching `verify-c6-1`.
   - Check all C6.1 references for the same name and maximum.

2. Fix the C1.1 improver/verifier mismatch
   - `verify-c1-1` defines Codebase Accessibility in terms of whether required project code is consolidated or technically linked.
   - `improve-c1-1` currently creates README/CLAUDE.md content, which improves agent context but does not improve the measured C1.1 criterion.
   - Replace `improve-c1-1` with a repository-consolidation workflow that:
     - discovers every repository belonging to the project;
     - creates a combined monorepo without modifying source repositories;
     - preserves source history, preferably through `git subtree`;
     - places each source repository in a named subdirectory;
     - migrates CI paths and cross-repository dependencies;
     - validates file completeness, history, builds, and tests;
     - uses resumable commit checkpoints.
   - Move the existing context-file behavior to `improve-a1`, where it matches Agent Context Availability.
   - Ensure `improve-readiness` invokes the corrected C1.1 implementation.

3. Strengthen `verify-c1-1`
   - Inspect inbound dependencies as well as dependencies declared by the repository being assessed.
   - When project grouping information is available, inspect sibling repositories for checkout, clone, copy, import, path dependency, workspace, and shared-tooling references to the assessed repository.
   - Treat a utility repository consumed by sibling project repositories as part of a split codebase.
   - Require checks of project metadata, technical links, outbound consumption, and inbound consumption before assigning Level 2.
   - Ignore generic third-party reusable tools that do not pull project-owned code.

4. Strengthen `verify-c5-2`
   Add explicit test-discovery guidance:
   - Java/Kotlin: `src/test/java/`, `src/test/kotlin/`
   - JavaScript/TypeScript: `__tests__/`, `*.test.*`, `*.spec.*`
   - Python: `tests/`, `test_*.py`, `*_test.py`
   - Go: `*_test.go`
   - Generic: `test`, `tests`, `spec`, and `specs`
   Also mention common coverage evidence such as JaCoCo configuration and reports, Jest configuration, pytest/coverage configuration, LCOV files, and coverage directories.

5. Strengthen `verify-c5-3`
   Add explicit integration/E2E discovery guidance:
   - Java/Kotlin: `src/integrationTest/java/`, `@SpringBootTest`, `@IntegrationTest`, and `integration`/`apitest` packages
   - JavaScript/TypeScript: `test/integration/`, `e2e/`, `cypress/`, `playwright/`
   - Python: `tests/integration/`, `tests/e2e/`
   - Generic names containing `integration`, `e2e`, `api-test`, or `apitest`

6. Strengthen `verify-c7-1`
   - First discover external dependencies from source code, manifests, configuration, and documentation.
   - Report each database or third-party service and whether tests isolate it or contact the real system.
   - Only mark the criterion N/A after confirming that no relevant external dependencies exist.

7. Harden `improve-c2-1`
   - Retain its incremental Level 0→1→2→3 behavior.
   - Before creating or validating a devcontainer, verify that Docker is installed and its daemon is reachable.
   - Run `devcontainer up`, then execute the project’s real build and test commands inside it.
   - Iterate on configuration-related failures.
   - If `devcontainer exec` cannot attach after a successful build, validate using the generated image with the repository mounted.
   - Distinguish configuration failures from external blockers such as unavailable secrets, networks, or services.
   - Report the validation method and build/test outcomes.

8. Preserve useful existing upstream behavior
   - Keep the recursive architecture-document inspection in `verify-c3-1`.
   - Keep linting and formatting configuration as valid evidence in `verify-c6-1`.
   - Do not remove the adoption skills, readiness improvers, or orchestration skills.

9. Add automated consistency validation
   - Verify every criterion name and maximum score agrees between:
     - `assess-readiness`
     - its corresponding `verify-*` skill
     - its corresponding `improve-*` skill
     - README skill tables
   - Fail validation when an improver targets behavior unrelated to its verifier.
   - Check skill cross-references resolve to existing directories.

10. Validate the result
   - Review all changed Markdown/frontmatter.
   - Run any repository tests or validation scripts.
   - Report changed files, checks run, and unresolved compatibility concerns.
   - Do not change licensing text.
