---
name: improve-c1-1
description: Improve readiness criterion C1.1 (Codebase Accessibility) to its maximum level (2) by merging the project's separate repositories into one mono-repo that keeps every repository's history, branches and tags. Analyses the repositories, migrates, cleans up, verifies the result against the sources and writes a migration report.
allowed-tools: Bash Read Write Edit
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Improve C1.1 — Codebase Accessibility

C1.1 is 0 when the code is split across unlinked repositories, 1 when they are linked through submodules or
similar, and 2 for a monolith or mono-repo. This skill takes the project to level 2 in one step: it merges the
repositories into a new mono-repo, each in its own folder, with full history, every branch and every tag.

If the project is already one repository holding all its code (see `/agentize:verify-c1-1`), report that C1.1
is at its maximum level (2) and stop.

The migration creates a **new** repository. It never changes the source repositories or their checkouts, and
it pushes nothing. Adapting the build and the CI pipelines to the mono-repo is a later, separate step.

**Run every phase without asking the user.** Each decision follows a fixed rule (below) and is recorded in the
report; the user reviews the report and corrects anything afterwards. Stop only when a phase fails.

## Before you start

Decide these yourself:

- **Sources.** When the clones sit side by side in one folder (a workspace), use `--workspace <folder>`: every
  git repository directly inside it is merged and its folder name becomes the repository's folder in the
  mono-repo. Otherwise take the repository list from the project (a `repos.txt`, the workspace file, the
  README or the CI configuration) and pass each one as `--repo <name>=<path-or-url>`. Ask the user only if
  you cannot tell which repositories belong to the project.
- **Output.** A new folder next to the workspace, `<project>-monorepo`, which must not exist yet. The work
  folder (snapshots, plan, logs, report) is `<output>.migration`.
- **Tools.** git 2.29 or newer (2.45+ recommended), Python 3.8+, and git-filter-repo. If
  `python -c "import git_filter_repo"` fails, install it with `python -m pip install --user git-filter-repo`.
  The scripts run it as a Python module, so it doesn't need to be on PATH.

The scripts are in `scripts/` next to this file. Run each phase with `python <skill dir>/scripts/<phase>.py`.
On a large project, run the migration and the verification in the background and wait for them to finish.

## Phase 1 — Analysis

```bash
python scripts/analyze.py --work <work> --workspace <workspace>     # or --repo <name>=<path-or-url> ...
```

The analysis copies each source into `<work>/snapshot/<name>.git`: its local branches and tags as they are,
and its remote's branches and tags, fetched fresh (`--no-fetch` uses the clone's remote-tracking branches
instead). These snapshots are the reference that verification compares against. It then decides everything
the later phases do and writes `<work>/analysis.json` (the plan) and `<work>/analysis.md` (a summary).

Read `analysis.md`. It lists each repository's default branch, branching strategy, branch and tag counts, the
decisions taken, and the **Needs attention** items: uncommitted work and stashes that won't be migrated,
submodules, Git LFS, paths too long for Windows, file names Windows can't check out, CI and hook files that
assume they are at the repository root, and repositories sharing history. These go into the report; they
don't stop the migration. A shallow snapshot does stop it: fetch the full history and run the analysis again.

## Phase 2 — Migration

```bash
python scripts/migrate.py --work <work> --output <output>
```

Each repository's history is rewritten with git filter-repo so its files live under `<name>/`, in parallel.
Author, committer, dates and messages are kept; commit hashes change, and filter-repo updates hashes quoted in
commit messages. Every branch name then becomes one combined branch: a commit whose tree holds every
repository's folder and whose parents are the branch each repository contributes. The default branch is
checked out.

## Phase 3 — Cleanup

```bash
python scripts/cleanup.py --work <work>
```

Creates the release tags, keeps single-repository tags as `<repo>/<tag>`, deletes the merged and inactive
branches, removes the helper refs (`refs/sources/`, `refs/imported-tags/`) and runs `git gc`.

## Phase 4 — Verification

```bash
python scripts/verify.py --work <work>
```

Compares the mono-repo with the untouched snapshots, and exits 1 if any check fails:

| Check | What it proves |
|---|---|
| Branches | every planned branch exists, the pruned ones are gone, tips unchanged since migration |
| Structure | for every branch and repository, `<repo>/` is exactly the source branch's tree, and the parents are the rewritten source commits |
| Content | for the **recent branches** of every repository, every file's bytes, mode and name equal the source, read from both object stores |
| History | for the same branches, the same commits: authors, committers, dates, parents and subjects |
| Commits | every source commit is reachable in the mono-repo |
| Tags | every source tag is covered and its folder matches the tagged source tree |
| Working tree | the default branch is checked out and `git status` is clean on this machine |

**Recent branches**, per repository: the production branch (master/main), develop, the default branch, every
branch whose last commit is at most 90 days older than the repository's newest branch (relative to the
repository's own activity, so a dormant repository is still checked), and at least its five newest branches.

The content check compares each pair of folders only once: a folder unchanged between branches is reused, so
checking dozens of branches costs little more than checking one.

If a check fails, find the cause; don't work around it. If the cause is in the plan or the scripts, fix it
and run again from the analysis or the migration, into a new output folder.

## Phase 5 — Report

```bash
python scripts/report.py --work <work>
```

Writes `<work>/migration-report.md`: a summary (output, sources, history, branches, tags, verification), the
changes made without asking, what needs attention, the next steps, and each phase's details. Read it and add to
**Needs attention** anything you noticed that the scripts didn't record.

Then tell the user: where the mono-repo is, where the report is, the verification result, the changes made
without asking (counts), and the items that need attention. Don't push the mono-repo anywhere; that is the
user's decision.

## Rules the plan follows

- **Local or remote branch.** A branch only on the remote is migrated as is. When the local and the remote
  branch differ, the newer one is used: an out-of-date local branch is replaced by the remote one, and a local
  branch with unpushed commits is used instead of the remote one. If they diverged, the remote branch keeps the
  name and the local one becomes `local/<branch>`. A local-only branch is migrated if it has commits that are
  not on the remote; otherwise (never pushed, or its remote branch was deleted) it is left out.
- **Names.** Branch names that differ only in letter case (`Feature/X`, `feature/x`) become one, using the
  spelling most repositories use (on a tie, the one with fewer capitals). This is decided folder by folder.
  Windows, macOS and Azure Repos can't hold both spellings. The production branches become one: a repository
  on `main` joins the others' `master`, or the other way round. A branch that is also a folder of other branch
  names (`feature` next to `feature/x`) is renamed `feature-branch`.
- **Combined branches.** A repository that doesn't have a branch contributes the branch it would have been
  created from (git-flow): its production branch for `master`, `main`, `hotfix/*` and `support/*`; its `develop`
  (or, without develop, its default branch) for everything else. The default branch of the mono-repo is the
  most common default branch.
- **Pruning.** A branch is deleted in cleanup when every repository that has it merged it into develop or
  production and none of them used it recently (see "Recent branches"). Production, develop, the default
  branches, `release/*`, `hotfix/*`, `support/*` and branches with unpushed commits are never deleted. Their
  commits stay in the history; the report lists each deleted branch's tip.
- **Tags.** Tags are grouped by name, ignoring letter case and a version prefix (`v1.2.0`, `1.2.0`,
  `release-1.2.0` are the same release). Dates are not used: lightweight tags carry the tagged commit's date,
  not the release date. A group found in two or more repositories becomes one annotated release tag, using the
  most common spelling, on a commit holding every repository at that release: the tagged commit where it has
  the tag, otherwise its production branch as of the release date (a repository that didn't exist yet is left
  out). A tag found in one repository only is kept as `<repo>/<tag>`.

## Re-running

The analysis can run again at any time; it reuses the snapshots and fetches only what changed. The migration
always needs a new, empty output folder. Each phase reads the previous phases' files in the work folder, so after
a fix you can rerun from the phase that needs it.
