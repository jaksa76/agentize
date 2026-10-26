<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# History merge

How `migrate` merges the sources' history into a new repository, each source in its own folder, with every
branch and tag. The rules below worked on a real project; the checks are what makes the result trustworthy.
The scripts in `scripts/` implement both in five phases. They are tools, not the method: use them as they are,
with options, or do the merge another way where the project needs it. The checks must pass either way.

The history merge creates a **new** repository. It never changes the source repositories or their checkouts,
and it pushes nothing.

**The history decisions are yours.** Two need judgement: the **branch issues** after the analysis, which
decide the migration options, and the **cleanup plan**, which you review and edit before applying it. Make
them yourself and record each one, with the reason for every default you changed; the user reviews them in
the report. Run the phases through without stopping, unless one fails.

## Tools

git 2.29 or newer (2.38+ to detect squash merges, 2.45+ recommended), Python 3.8+, and git-filter-repo. If
`python -c "import git_filter_repo"` fails, install it with `python -m pip install --user git-filter-repo`.
The scripts run it as a Python module, so it doesn't need to be on PATH.

Run each phase with `python <skill dir>/scripts/<phase>.py`; `--help` describes every option. On a large
project, run the migration and the verification in the background and wait for them to finish.

The work folder (snapshots, plan, logs, report) is `<output>.migration` by default, next to the output.

## Phase 1 — Analysis

```bash
python scripts/analyze.py --work <work> --workspace <workspace>     # or --repo <name>=<path-or-url> ...
```

`--workspace` takes every git repository directly inside a folder, named after its folder; `--repo` names
each source explicitly. Pass the source set `plan` decided, not whatever happens to be in the workspace.

The analysis copies each source into `<work>/snapshot/<name>.git`: its local branches and tags as they are,
and its remote's branches and tags, fetched fresh (`--no-fetch` uses the clone's remote-tracking branches
instead). These snapshots are the reference that verification compares against. It then decides everything
the later phases do and writes `<work>/analysis.json` (the plan) and `<work>/analysis.md` (a summary).

Read `analysis.md`. It lists each repository's default branch, branching strategy, branch and tag counts, the
decisions taken, and the **Needs attention** items: uncommitted work and stashes that won't be migrated,
submodules, Git LFS, paths too long for Windows, file names Windows can't check out, CI and hook files that
assume they are at the repository root, and repositories sharing history. These go into the report; they
don't stop the migration. A shallow snapshot does stop it: fetch the full history and run the analysis again.
The file checks are hints, not an inventory: `plan` and `migrate` look for themselves.

### Check the branch issues

The **Branch issues** table lists the combined branches that are more than the same branch of several
repositories, with what the migration does by default and the option that changes it. The script can't tell
intent from history alone, so look at each one yourself in the snapshots (`<work>/snapshot/<repo>.git`; a
branch is `refs/remote/<branch>`, or `refs/local/<branch>` when only the local clone has it). For example,
`git -C <snapshot> log --date=short --format='%ad %an %s' <base>..refs/remote/<branch>` shows a branch's own
commits.

| Issue | What to look at | When to change the default |
|---|---|---|
| different bases | The commits of the repositories in the minority: are they the same work as the others (same ticket, same topic), or a fix meant for production that was named like a feature? | Same work, and merging it into develop is fine (master reaches develop anyway): `--combine <branch>`. Otherwise keep the split. |
| unexpected base | Whether the branch is really what its name says, e.g. a hotfix named `feature/...`. | The default follows the real base; change what the other repositories contribute with `--fallback` only if the base itself was detected wrongly. |
| partly merged | That the merged repository's work is really in its target (`git log <target> --grep <ticket>`, or the files). | Keep the default unless the team still needs the old, unmerged state of that folder: `--merged-content tip`. |
| no common history | What the branch holds: gh-pages, documentation, an imported project. | If the other repositories belong in it after all: `--fallback '<branch>=develop'`. |
| possibly unrelated | The commit subjects and ticket numbers on each repository's branch. | Different work under a reused name: `--split <branch>:<repo>` for each repository whose work differs from the most recent one. |
| squash-merged | Nothing; for information. | - |

Also look into anything else in the analysis that looks wrong, such as a guessed default branch or an
unexpected strategy, and correct it before migrating (for example `--default-branch`).

## Phase 2 — Migration

```bash
python scripts/migrate.py --work <work> --output <output> [options]
```

Each repository's history is rewritten with git filter-repo so its files live under `<name>/`, in parallel.
Author, committer, dates and messages are kept; commit hashes change, and filter-repo updates hashes quoted in
commit messages. `<work>/commit-maps/<name>` maps every source commit to its rewritten commit. Every branch
name then becomes one combined branch: a commit whose tree holds every repository's folder and whose parents
are the branches each repository contributes. The default branch is checked out.

Without options the migration follows the defaults shown in the analysis. Pass options only for what your
check of the branch issues showed to be wrong; each one is recorded in the report:

| Option | Effect |
|---|---|
| `--combine BRANCH` | Keep a branch together although its repositories created it from different trunks. |
| `--mixed-bases combine` | The same for every branch (the default is `split`). |
| `--split BRANCH:REPO` | Move one repository's branch to `<repo>/<branch>` (a reused name). `--split BRANCH` splits by trunk. |
| `--merged-content tip` | A repository that already merged a branch others still work on contributes its old branch tip instead of its target branch. |
| `--fallback PATTERN=KIND` | What repositories without a matching branch contribute: `base`, `develop`, `production`, `default` or `none`. PATTERN is a glob such as `release/*`. |
| `--contribute BRANCH:REPO=SRC` | One repository, which doesn't have BRANCH, contributes its branch SRC (or `none`). |
| `--default-branch NAME` | The mono-repo's default branch. |

## Phase 3 — Cleanup

Cleanup turns the sources' tags into the mono-repo's tags and deletes branches nobody needs. It runs in two
steps, with your own review in between, because the right result depends on how the project released and
worked.

**1. Propose.**

```bash
python scripts/cleanup.py --work <work> --plan
```

Writes `<work>/cleanup-plan.json` (the plan) and `<work>/cleanup-plan.md` (the same, for reading), following
the rules below: release tags, tags kept as `<repo>/<tag>`, branches to delete. Its **To review** section
lists what the rules may have got wrong.

**2. Review.** Read `cleanup-plan.md` together with the analysis and the migration summary, check the flagged
items in the snapshots, and edit `cleanup-plan.json` where the proposal is wrong. Give each change a `note`
saying why; the notes go into the report.

| Flag | What to look at | Typical change |
|---|---|---|
| release tag: dates far apart | The tags' dates, messages and the commits they point at. Different releases that happen to share a number? | Remove the release tag and list its tags under `repo_tags` as `<repo>/<tag>`. |
| release tag: spelled differently | Whether the spellings follow the same versioning. | Rename the release tag (`name`) to the project's usual spelling. |
| repository tag: close to other repositories' tags | A release train numbered per repository (`2024.03` in one, `v5.2` in another): release notes, CHANGELOGs, CI release pipelines, tag messages. | Move the tags into one release tag (`members`), named the way the project names its releases. |
| branch: could be deleted | Whether the team still needs it: recent commits, an environment branch (`staging`, `qa`), an open pull request on the old remote. | Add it to `delete_branches` with a reason, or leave it. |

Also use what you know about the project. For example, delete the `<repo>/<branch>` copies of a split branch
whose work is merged elsewhere, keep a branch the README calls a deployment branch, or name release tags after
the product's release scheme. Versions derived from tags (build tooling that reads `git describe`) see the
new names; `plan` should have found them.

**3. Apply.**

```bash
python scripts/cleanup.py --work <work> --apply
```

Checks the plan first: every source tag used exactly once, valid and unique tag names, existing branches,
and that deleting the branches loses no commit of the sources (only the combining commits). If anything is
wrong it changes nothing and lists the problems; fix the plan and apply again. Otherwise it creates the tags,
deletes the branches and the helper refs (`refs/sources/`, `refs/imported-tags/`) in one transaction and runs
`git gc`. Record in the mono-repo how far each source was brought in before this step, while the helper refs
still name each source branch's rewritten tip.

## Phase 4 — Verification

```bash
python scripts/verify.py --work <work>
```

Compares the mono-repo with the untouched snapshots, and exits 1 if any check fails:

| Check | What it proves |
|---|---|
| Branches | every migrated branch exists unless cleanup deleted it, tips unchanged since migration |
| Structure | for every branch and repository, `<repo>/` is exactly the source branch's tree, and the parents are the rewritten source commits |
| Content | for the **recent branches** of every repository, every file's bytes, mode and name equal the source, read from both object stores; a branch that is no branch's folder (already merged by its repository, or deleted in cleanup) is checked through its rewritten commit in the history |
| History | for the same branches, the same commits: authors, committers, dates, parents and subjects |
| Commits | every source commit is reachable in the mono-repo |
| Tags | every source tag is covered and its folder matches the tagged source tree |
| Working tree | the default branch is checked out and `git status` is clean on this machine |

**Recent branches**, per repository: the production branch (master/main), develop, the default branch, every
branch whose last commit is at most 90 days older than the repository's newest branch (relative to the
repository's own activity, so a dormant repository is still checked), and at least its five newest branches.

These checks hold right after the merge, before the mono-repo has changes of its own. Run them then. Once the
migration's changes are in, "folder equals source" no longer holds; `update` describes what to check instead.

If a check fails, find the cause; don't work around it. If the cause is in the plan or the scripts, fix it
and run again from the analysis or the migration, into a new output folder.

## Phase 5 — Report

```bash
python scripts/report.py --work <work>
```

Writes `<work>/migration-report.md` about the history merge: a summary (output, sources, history, branches,
tags, verification), the changes made without asking, what needs attention, and each phase's details. Add to
**Needs attention** anything you noticed that the scripts didn't record, and, for each migration option you
passed, what you found in the branch issues that made you choose it. `migrate` extends this report with
everything after the history merge.

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
- **Bases.** For every branch the analysis finds the trunk it was created from (develop, the production
  branch or a release branch: the one the fewest of its commits are missing from; on a tie, the one git-flow
  expects from its name), and whether it was already merged into its target (production for `release/*`,
  `hotfix/*` and `support/*`, the base otherwise), also by squash or rebase. A branch that is already
  contained in a trunk only shows where it was merged, not where it was created (a release merged into master
  but never back into develop), so its base is the trunk git-flow expects from its name.
- **Combined branches.** These defaults can be changed with migrate's options:
  - When repositories created a branch from different trunks, the minority moves to `<repo>/<branch>`.
  - A repository that already merged a branch, while others still work on theirs, contributes the branch it
    merged into; its old tip stays in the history as an extra parent.
  - A repository that doesn't have a branch contributes the branch's base: its production branch for
    `master`, `main`, `release/*`, `hotfix/*` and `support/*` (merging them into production then changes
    nothing in that folder); its `develop` (or, without develop, its production branch) for branches created
    from develop; nothing for a branch that shares no history with any trunk.
  - The default branch of the mono-repo is the most common default branch.
- **Pruning (proposed).** Cleanup proposes deleting a branch when every repository that has it merged it into
  develop or production and none of them used it recently (see "Recent branches"). Production, develop, the
  default branches, `release/*`, `hotfix/*`, `support/*` and branches with unpushed commits are never proposed.
  The review may delete more, but never a branch whose commits are on no other branch or tag; the report lists
  each deleted branch's tip.
- **Tags (proposed).** Tags are grouped by name, ignoring letter case and a version prefix (`v1.2.0`, `1.2.0`,
  `release-1.2.0` are the same release). Dates don't decide the grouping, because lightweight tags carry the
  tagged commit's date, not the release date; they only flag groups for review. A group found in two or more
  repositories becomes one annotated release tag, using the most common spelling, on a commit holding every
  repository at that release: the tagged commit where it has the tag, otherwise its production branch as of the
  release date (a repository that didn't exist yet is left out). A tag found in one repository only is kept as
  `<repo>/<tag>`. The review can regroup and rename them.

## Re-running and reusing

The analysis can run again at any time; it reuses the snapshots in its work folder and fetches only what
changed. The migration always needs a new, empty output folder. Each phase reads the previous phases' files
in the work folder, so after a fix you can rerun from the phase that needs it. `cleanup.py --plan` overwrites
the plan, including your edits; after a successful `--apply` the cleanup can't run again on the same
mono-repo, so a different cleanup means migrating again.

For a final run after a rehearsal, keep the rehearsal's work folder as it is and give the final run its own,
starting from a copy of the rehearsal's snapshots. Pass the rehearsal's migration options again (recorded in
its `migration.json`), and start the cleanup from its reviewed `cleanup-plan.json`: `--apply` then refuses
until every new tag is placed and every branch that disappeared is taken out, which is exactly the part that
needs fresh review.
