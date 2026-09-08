---
name: improve-c1-1
description: Improve readiness criterion C1.1 (Codebase Accessibility) in the current project by consolidating split repositories into a single combined repository. Raises the fulfillment level by one step.
allowed-tools: Bash Read Write Edit
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Improve C1.1 — Codebase Accessibility

## Levels

| Level | Description |
|-------|-------------|
| 0 | Code split across unlinked repositories |
| 1 | Repositories linked through submodules or equivalent mechanisms |
| 2 | Monolith or mono-repo — all required project code in a single repository |

This skill raises the fulfillment level to **Level 2** by combining every repository that belongs to the project into a single mono-repo. The source repositories are **read only** — they are cloned and never pushed to, rewritten, or deleted. The combined repository is a new artefact.

**If the project is already at Level 2**, report that C1.1 is already at its maximum level and stop.

> **Scope note.** This skill changes *where the project's code lives*. It does not write `README.md` or `CLAUDE.md` agent-context content — that is criterion A1 (Agent Context Availability); use `/improve-a1` for it. The only context file this skill writes is the root README of the newly created combined repository, describing what was merged into it.

---

## Pre-flight

Before running, verify:

1. **Git is available** (`git --version`) and the current user has read access to every source repository.
2. **Write access** to the destination path where the combined repository will be created.
3. **The destination path is outside every source repository**, so nothing can be written back into a source.

---

## Execution strategy

This skill is long-running and touches many files. To keep context manageable and progress recoverable:

- **Every step ends with a commit checkpoint** in the combined repository, using the exact commit subjects given below. The skill is resumable: on start, read `git -C <output-dir> log --oneline` and skip every step whose checkpoint commit is already present. Resume from the first missing checkpoint.
- **Subagents** handle the two most context-heavy steps (CI migration and cross-repo reference updates). Spawn a fresh subagent per step, give it only the context it needs, and commit its output yourself before proceeding.

The main agent retains ownership of the flow, the checkpoints, and the final report. Subagents write files; they do not commit.

---

## Instructions

### Step 1 — Determine the current level

Follow the `/verify-c1-1` skill to confirm the current level. If it is already Level 2, stop and report.

### Step 2 — Discover every repository in the project

Compile the complete list of repositories that belong to this project. Look, in order of reliability:

1. **Explicit project metadata** — a `projects.json`, `repos.yaml`, workspace manifest, or equivalent file listing the project's repositories (for example a `repos` field).
2. **Technical links from this repository** — `.gitmodules`, git subtree remotes, workspace configuration, vendored path dependencies.
3. **Outbound references** — CI workflows and build scripts that `actions/checkout` a different `repository:`, `git clone` a sibling repo, or copy files out of one; dependency manifests pointing at sibling git URLs.
4. **Inbound references** — sibling repositories under the same organisation that check out, clone, copy, import, or path-depend on *this* repository. A utility repository consumed by sibling project repositories is part of the split codebase and must be included.
5. **The hosting organisation** — list the org's repositories (for example `gh repo list <org>`) and match them against the names found above.

Exclude generic third-party reusable tools and actions that do not carry project-owned code.

Record, for each repository, its URL or local clone path and the **subdirectory name** it will occupy in the combined repo — the last path segment of the URL, without `.git`:

| Source | Subdirectory in combined repo |
|---|---|
| `https://github.com/org/service-api` | `service-api/` |
| `https://github.com/org/shared-utils` | `shared-utils/` |

If the list is ambiguous, or if a repository may or may not belong to the project, **ask the user to confirm the list before merging anything.**

### Step 3 — Create the combined repository

Create and initialise the output repository, then import each source repository into its own subdirectory with history preserved.

```bash
mkdir -p <output-dir> && git -C <output-dir> init -b main
git -C <output-dir> commit --allow-empty -m "chore: initialise combined repository"
```

> **Checkpoint** — commit: `chore: initialise combined repository`

**Preferred method — `git subtree`.** For each source repository, in list order:

```bash
git -C <output-dir> remote add <name> <url-or-local-path>
git -C <output-dir> fetch <name>
git -C <output-dir> subtree add --prefix=<name> <name> <default-branch>
```

`git subtree add` places the source repository's files under `<name>/` and keeps its entire commit graph as ancestors of the resulting merge commit, without rewriting any historical commit. It reads the source over a normal fetch and never writes to it. Detect `<default-branch>` per repository (`git -C <output-dir> remote show <name>`) rather than assuming `main` or `master`.

Keep the remotes in place until Step 7's verification passes, then remove them (`git -C <output-dir> remote remove <name>`).

> **Checkpoint** — one commit per repository. `git subtree add` creates its own merge commit; keep its default subject or set it to `feat: import <name> via subtree`.

**Scripted method — `merge-repos.sh`.** For more than two or three repositories, use the bundled script instead of running the commands by hand. It performs the same `git subtree add` import per repository, and adds per-repo statistics and a verification report. The script is at `.claude/skills/improve-c1-1/scripts/merge-repos.sh` (in a plugin install, `skills/improve-c1-1/scripts/merge-repos.sh` under the plugin root).

```bash
bash .claude/skills/improve-c1-1/scripts/merge-repos.sh \
  --output <output-dir> \
  --repo "service-api=https://github.com/org/service-api" \
  --repo "shared-utils=https://github.com/org/shared-utils"
```

For each repository the script clones the source into a temporary directory, detects its default branch, records its branch/commit/file counts, and runs `git subtree add --prefix=<name>`. It works only on those local clones — the source repositories are never modified. It then prints a verification report with two checks:

| Check | What it verifies |
|---|---|
| Files in output working tree | The output file count equals the sum of the source file counts — nothing lost, nothing collided |
| Total unique commits | The output commit count equals source commits + 1 empty root commit + one subtree merge commit per repository — no history truncated or duplicated |

**Both checks must pass before proceeding.** If either fails, investigate (clone error, fetch conflict, a source repo with an unexpected default branch) and re-run from a clean output directory.

**Know the trade-off of the subtree approach.** Both methods import only the default branch, and in *historical* (pre-merge) commits the files still sit at the source repository's root rather than under `<name>/`. `git log --follow <name>/<file>` therefore reports history from the merge point forward; reaching further back means walking the merged-in ancestry directly (`git log -- <file>` against the source-side parent). This is the accepted cost of not rewriting commit hashes. If the project genuinely needs every branch imported and every historical path rewritten, that is a `git filter-repo` migration and is out of scope for this skill — say so in the report rather than improvising it.

Whichever method is used, the result has the same properties: every source file lives under its own `<name>/` subdirectory on `main`, the full source commit graph is reachable, and colliding filenames (two `README.md` files, for example) are disambiguated by the subdirectory prefix.

> **Checkpoint.** All source history is now in the combined repository. No later step rewrites history — everything from here only adds commits. Record the HEAD SHA: `git -C <output-dir> rev-parse HEAD`.

### Step 4 — Add root-level scaffolding

The combined repository has no root-level files of its own yet — only the `<name>/` subdirectories. Create at the root:

- **`README.md`** — what the combined repository is, a table mapping each subdirectory to the source repository it came from, and links to each subdirectory's own README.
- **`.gitignore`** — the union of all source `.gitignore` files, deduplicated. Keep the per-subdirectory files as well.
- **`.editorconfig`** — if any source has one, lift the most common settings to the root. Per-subdirectory files still override.
- **`LICENSE`** — copy it up only if every source shares the same licence. If they differ, keep the per-subdirectory copies and record each licence in the root README. Never rewrite or merge licence text.

> **Checkpoint** — commit: `chore: add root scaffolding`

### Step 5 — Migrate CI pipelines *(subagent)*

**Context to pass to the subagent:** the output repository path; the subdirectory names and their source repository URLs; the CI platforms in use, read from the merged-in `<name>/.github/workflows/`, `<name>/Jenkinsfile`, `<name>/.gitlab-ci.yml`, `<name>/azure-pipelines.yml`, and equivalents.

**Task for the subagent:** inspect every merged-in CI configuration and produce updated versions.

1. **Path-scope each pipeline.** Add `working-directory: <name>/` to job steps (or the platform's equivalent) and narrow `on.push.paths` / `on.pull_request.paths` filters to `<name>/**`, so a change in one subdirectory does not run every pipeline.
2. **Fix checkout and artefact paths.** Update any step that checks out to a specific path, uploads artefacts by path, or references a file by a path that was previously repo-root-relative and is now under `<name>/`.
3. **Remove cross-repo checkouts.** A step that checked out a sibling repository now reads that code from a sibling subdirectory; delete the checkout and repoint the path. Remove the tokens and deploy keys that existed only to fetch sibling repos, and note them in the report so the team can revoke them.
4. **Add a root orchestration pipeline** (for example `.github/workflows/ci.yml`) that detects which subdirectories changed (path filters or `git diff --name-only`) and dispatches the per-subdirectory pipelines via a matrix strategy or reusable workflow calls. For a complex inter-subdirectory dependency graph, prefer a build tool that models it — Nx, Turborepo, Bazel, Gradle multi-project — over a hand-written matrix.

The subagent writes files but does not commit. Review its changes, then commit.

> **Checkpoint** — commit: `ci: migrate pipelines to monorepo structure`

### Step 6 — Migrate cross-repository dependencies *(subagent)*

**Context to pass to the subagent:** the output repository path; the subdirectory names with their original source repository URLs and package names, so it can search for references to them.

**Task for the subagent:** in every subdirectory, find references to the *other* source repositories and repoint them at monorepo-local paths.

1. **Package dependencies.** In `package.json`, `pom.xml`, `build.gradle`, `requirements.txt`, `pyproject.toml`, `go.mod`, `Gemfile`, `Cargo.toml`, and equivalents, replace git-URL and published-artifact dependencies on sibling repos with local links: npm/yarn/pnpm workspaces, Maven modules, Gradle `includeBuild`/project dependencies, Go `replace` directives, path dependencies.
2. **Import paths.** Where code imported a sibling through a module path tied to its old repository URL, repoint the import at the new in-repo location.
3. **Shared tooling.** Build scripts and Makefiles that ran `git clone <sibling>` can read the sibling subdirectory directly — delete the clone step and fix the path.
4. **Documentation links.** Repoint links that pointed at the old separate repository URLs to the corresponding subdirectory.
5. **Workspace configuration.** Create or update the root workspace file the toolchain needs (`package.json` workspaces, `pnpm-workspace.yaml`, `settings.gradle`, root `pom.xml`, `go.work`, Cargo workspace members).

The subagent writes files but does not commit. Review its changes, then commit.

> **Checkpoint** — commit: `refactor: update cross-repo references to monorepo paths`

### Step 7 — Validate the combined repository

Confirm the combined repository is functionally equivalent to the sources before declaring completion. Record the result of each check for the report.

1. **File completeness.** For each subdirectory, compare the tracked file list against the source repository's default branch:
   ```bash
   git -C <source-clone> ls-files | sort > /tmp/src-<name>.txt
   git -C <output-dir> ls-files "<name>/" | sed "s|^<name>/||" | sort > /tmp/out-<name>.txt
   diff /tmp/src-<name>.txt /tmp/out-<name>.txt
   ```
   The diff must be empty apart from files the migration steps deliberately moved or deleted.
2. **History preservation.** Confirm every source commit is reachable in the combined repository:
   ```bash
   git -C <output-dir> rev-list --count --all
   ```
   It must equal the sum of the source commit counts, plus the empty root commit, plus one merge commit per repository, plus any commits added by later steps. Then spot-check one file with a long history — `git -C <output-dir> log -- <name>/<some-file>` must show its original commits and authors. Remember the subtree trade-off from Step 3: `--follow` only tracks the file from the merge point forward, so its absence there is expected and is not a sign of lost history.
3. **Build.** Run each subdirectory's build command from the combined repository and confirm it succeeds. If a build fails because of a path or dependency the migration missed, fix it, commit, and re-run.
4. **Tests.** Run each subdirectory's test suite and confirm it passes. Distinguish failures caused by the migration from failures that already existed in the source repository — check the same test against the source clone before attributing it to the merge.
5. **CI dry-run.** If possible, push a test branch and confirm the root pipeline dispatches the right per-subdirectory jobs.

> **Checkpoint** — commit any fixes as: `fix: resolve monorepo migration issues`

---

## Report

State:

- **Before level** and **after level**
- **Repositories discovered**, how each was discovered (metadata, technical link, outbound reference, inbound reference), and which were merged
- **Import method used** (`git subtree` by hand or `merge-repos.sh`) and why
- **Output repository path**
- **Validation results** — file completeness, history preservation, build, and tests, per subdirectory, with the numbers
- **Credentials to revoke** — tokens or deploy keys that existed only for cross-repo access
- **Any blockers** that prevented completion, and whether the source repositories were left untouched (they should always be)
