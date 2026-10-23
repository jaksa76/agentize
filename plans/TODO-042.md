# TODO-042 — Rename skills to more intuitive names

## Goal

Replace the opaque criterion IDs (`C1.1`, `A3`, …) in skill names with descriptive names, make the track
(readiness vs. adoption) visible in every skill name, and use one verb ("assess") for measuring.

## Decisions

1. **Naming scheme:** `<verb>-<track>-<criterion>` where
   - `verb` ∈ `assess` | `improve`
   - `track` ∈ `readiness` | `adoption`
   - `criterion` = kebab-case slug of the criterion name (table below)
2. **`verify` → `assess`.** The skills return a graded level 0–3 (a measurement), not a pass/fail check, and the
   docs already say "assess". "Verify" is dropped from skill names, descriptions, docs and plugin keywords.
3. **Aggregate skills keep their names:** `assess-readiness`, `improve-readiness`, `assess-adoption`,
   `improve-adoption`. Hierarchy: `assess-readiness` = whole track, `assess-readiness-unit-tests` = one criterion.
4. **Criterion IDs (C1.1, A3, …) disappear from skill names, headings and descriptions.** Docs group criteria by
   dimension (the C1–C8 headings) so the structure stays visible.
5. **Skill locations are unchanged.** Readiness criterion skills stay in `plugins/agentize/skills/`; the adoption
   skills and the other `improve-c*` skills stay in `.claude/skills/`. Moving them is out of scope.

## Name mapping

### Readiness (11 criteria)

| Old assess skill | New assess skill | Old improve skill | New improve skill |
|---|---|---|---|
| `verify-c1-1` | `assess-readiness-codebase-accessibility` | `improve-c1-1` | `improve-readiness-codebase-accessibility` |
| `verify-c2-1` | `assess-readiness-devenv-setup` | `improve-c2-1` | `improve-readiness-devenv-setup` |
| `verify-c3-1` | `assess-readiness-documentation` | `improve-c3-1` | `improve-readiness-documentation` |
| `verify-c4-1` | `assess-readiness-requirements` | `improve-c4-1` | `improve-readiness-requirements` |
| `verify-c5-1` | `assess-readiness-runnability` | `improve-c5-1` | `improve-readiness-runnability` |
| `verify-c5-2` | `assess-readiness-unit-tests` | `improve-c5-2` | `improve-readiness-unit-tests` |
| `verify-c5-3` | `assess-readiness-integration-tests` | `improve-c5-3` | `improve-readiness-integration-tests` |
| `verify-c6-1` | `assess-readiness-coding-guidelines` | `improve-c6-1` | `improve-readiness-coding-guidelines` |
| `verify-c7-1` | `assess-readiness-test-isolation` | `improve-c7-1` | `improve-readiness-test-isolation` |
| `verify-c8-1` | `assess-readiness-ci-cd` | `improve-c8-1` | `improve-readiness-ci-cd` |
| `verify-c8-2` | `assess-readiness-observability` | `improve-c8-2` | `improve-readiness-observability` |

### Adoption (8 criteria)

| Old assess skill | New assess skill | Old improve skill | New improve skill |
|---|---|---|---|
| `verify-a1` | `assess-adoption-agent-context` | `improve-a1` | `improve-adoption-agent-context` |
| `verify-a2` | `assess-adoption-agent-contributions` | `improve-a2` | `improve-adoption-agent-contributions` |
| `verify-a3` | `assess-adoption-feedback-loops` | `improve-a3` | `improve-adoption-feedback-loops` |
| `verify-a4` | `assess-adoption-task-scope` | `improve-a4` | `improve-adoption-task-scope` |
| `verify-a5` | `assess-adoption-workflow-integration` | `improve-a5` | `improve-adoption-workflow-integration` |
| `verify-a6` | `assess-adoption-autonomous-operation` | `improve-a6` | `improve-adoption-autonomous-operation` |
| `verify-a7` | `assess-adoption-proactive-quality` | `improve-a7` | `improve-adoption-proactive-quality` |
| `verify-a8` | `assess-adoption-planning-integration` | `improve-a8` | `improve-adoption-planning-integration` |

Total: 38 skills renamed (19 assess + 19 improve). `assess-readiness`, `assess-adoption`, `improve-readiness`,
`improve-adoption` and `do-next-task` keep their names.

## Steps

1. **Rename directories with `git mv`** (preserves history), one per row of the mapping tables, in both
   `.claude/skills/` and `plugins/agentize/skills/`. `improve-c1-1` contains `scripts/` (the merge scripts); the
   whole directory moves, so check nothing refers to its old path.
2. **Update each renamed `SKILL.md`:**
   - frontmatter `name:` to the new name
   - frontmatter `description:` — "Verify …" becomes "Assess …"; drop the criterion ID, e.g.
     `Assess readiness criterion Unit Test Coverage in the current project. Reports fulfillment level 0–3.`
   - the `# Verify C5.2 — Unit Test Coverage` heading becomes `# Assess Readiness: Unit Test Coverage`
     (same pattern for improve and adoption)
   - body text that names other skills, e.g. `/agentize:verify-c1-1`
3. **Update the aggregate skills:**
   - `assess-readiness`: the 11 `follow the /agentize:verify-cX-Y skill` lines, plus "C1.1–C8.2" in the
     description and the report template
   - `assess-adoption`, `improve-readiness`, `improve-adoption`: references to `verify-*`, `improve-c*`,
     `improve-a*`, and criterion IDs in descriptions, steps and report templates
4. **Update the docs:** `README.md` (skill table at lines ~33–43 and the usage examples), `READINESS.md`,
   `ADOPTION.md` and `VISION.md`. Replace skill names and criterion IDs with names, and keep the dimension
   grouping. Fix the typo "assesment" in `README.md` (line ~48).
5. **Plugin metadata:** `plugins/agentize/.claude-plugin/plugin.json` — change the keyword `verify` to
   `assess`. Check `.claude-plugin/marketplace.json` for skill references. Decide whether to bump the version
   (the rename breaks existing slash commands, so probably 1.1.0 or 2.0.0).
6. **Repo-wide sweep for leftovers:**
   ```
   grep -rEn "\b(verify|improve)-(c[1-8]-[1-9]|a[1-8])\b" .
   grep -rEn "\b(C[1-8]\.[1-9]|A[1-8])\b" --exclude-dir=.git .
   grep -rin "verify" --exclude-dir=.git .
   ```
   The second grep also matches "A1" in unrelated text, so review each hit. Every hit for the first and third
   should be gone or deliberate.
7. **Smoke test:** reload the plugin and the project skills, then check that:
   - the new names show up under `/` autocomplete (`assess-readiness-` lists 11, `assess-adoption-` lists 8,
     and the same for `improve-`)
   - `/agentize:assess-readiness` runs end to end on a sample project and calls every criterion skill by its
     new name
   - `/agentize:improve-readiness` and `/improve-adoption` still delegate correctly
8. **Commit** in logical chunks (renames and SKILL.md edits, then docs, then plugin metadata), then update
   `TODO.md` to mark TODO-042 done.

## Risks and notes

- **Breaking change** for anyone with the old slash commands installed or in their own docs and scripts. No
  aliases are planned; mention the rename in the commit message and the README.
- **Git rename detection:** do the `git mv` in a commit separate from large content edits, so the renames stay
  traceable.
- **Report output:** the assessment reports currently print criterion IDs. After the rename they should print
  criterion names only, so check the report templates in the aggregate skills.
- **Name length:** the longest name is `improve-adoption-workflow-integration` (37 characters). Acceptable.
- **Open question:** whether to keep a stable short ID anywhere (for example in report tables) for people who
  already know C1.1-style references. Default: no.
