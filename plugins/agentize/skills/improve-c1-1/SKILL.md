---
name: improve-c1-1
description: Improve readiness criterion C1.1 (Codebase Accessibility) to its maximum level (2) by moving the project's separate repositories into one mono-repo that keeps every repository's history, and that builds, tests, runs and deploys as one. Subcommands cover a whole switchover - plan, migrate (rehearsal and final run), update, add-repo, clone-prs, port-back. Without a subcommand it explains the process and where a migration under way stands.
argument-hint: "[plan | migrate | update | add-repo | clone-prs | port-back] [details]"
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
similar, and 2 for a monolith or mono-repo. This skill takes the project to level 2: it moves the repositories
into a new mono-repo, each in its own folder, with full history, and makes the mono-repo build, test, run and
deploy as one. A merged history alone is not the goal; most of the work is in what comes after it.

If the project is already one repository holding all its code (see `/agentize:verify-c1-1`), report that C1.1
is at its maximum level (2) and stop.

Arguments: `$ARGUMENTS`. The first word is the subcommand; the rest is for it (a repository, a branch, a
pull request, ...).

| Subcommand | Goal | Read |
|---|---|---|
| *(none)* | Explain the process, and where a migration under way stands and what comes next | below |
| `plan` | Decide the source set and everything the migration needs decided, before migrating | [plan](subcommands/plan.md) |
| `migrate` | A mono-repo with full history that builds, tests, runs and deploys as one, plus `migrate-local-changes`; as a rehearsal, or the final run reusing the rehearsal | [migrate](subcommands/migrate.md) |
| `update` | Bring in what the sources got since the last run, keeping the mono-repo's own changes | [update](subcommands/update.md) |
| `add-repo` | Bring one more repository into an existing mono-repo | [add-repo](subcommands/add-repo.md) |
| `clone-prs` | Recreate the sources' open pull requests in the mono-repo | [clone-prs](subcommands/clone-prs.md) |
| `port-back` | Carry mono-repo work back to a source repository: a rollback, a hotfix through an old pipeline, a repository that stays separate | [port-back](subcommands/port-back.md) |

Read the subcommand's file before starting it. Each one states its goal, what must be true afterwards and how
to check it, what is the user's to decide, and the lessons learned so far. None of them prescribes a method:
you have the project in front of you, so work out how. Examples come from one project (the CheckIT Learning
migration, about 40 repositories on Azure DevOps, .NET and Node, containers) and say so; they show what to look
for, not what to do. Where you need a script for the project, write it in the migration's work folder and
treat it as disposable.

## Ground rules

- **The sources are never changed.** Neither the source repositories nor their clones. Everything happens in
  new folders.
- **Nothing is pushed, locally everything is allowed.** Commit freely in the new mono-repo, on a work branch
  or on the migrated branches as the subcommand needs. Replaying the migration's changes needs them as commits.
- **Outward-facing actions are shown first and need the user's confirmation:** pushing, creating or closing
  pull requests, locking repositories, registering or disabling pipelines, anything on the hosting service
  (Azure DevOps, GitHub, GitLab, Bitbucket, ...). Show exactly what will happen, then wait.
- **Decide what is yours to decide, ask what is the user's.** Each subcommand says which is which. Record every
  decision with its reason, so the report can show it and a later run can reuse it.

## What the subcommands need in common

These are needs; you pick the mechanism, and keep it consistent across runs.

- **The mono-repo knows its sources.** `update`, `port-back`, `clone-prs` and `migrate-local-changes` run later,
  on other machines, without the work folder. Record in the mono-repo itself which source (its URL) maps to
  which folder, and how far each source branch was brought in (the source commit and its rewritten
  counterpart). For example, a small file at the root, kept up to date by every subcommand that brings
  history in.
- **The mono-repo's own changes stay distinguishable from the sources' history.** These are the changes for
  building, testing, pipelines, images and the local environment. A final run replays them, `update` must keep
  them, `port-back` must leave them out. For example, they are separate commits on top of the merged history,
  each marked so that it can be found again (a trailer, a branch they are developed on, or both).
- **Decisions are reusable.** The final run during the freeze should not redo the rehearsal's review. Only what
  changed since then (new branches, tags, repositories) needs fresh review. Snapshots are reused instead of
  fetched again (1.1 GB in the example project).
- **Rewriting is deterministic.** git filter-repo, given the same source commits and the same options, gives
  the same rewritten commits, also when the source has gained commits since; the rewritten commits already in
  the mono-repo are then ancestors of the new ones. So a source's new history can be rewritten again and
  merged as is, and a mono-repo commit inside a folder maps back to exactly one source commit. Check it holds
  on the project (same tool versions, same options) before relying on it. The commits that join the
  repositories' branches are the migration's own; don't expect a second run to recreate them identically.

## Without a subcommand

Explain, briefly and for this project:

- **What C1.1 is,** where the project stands on it, and why level 2 matters to agents: one checkout holds
  everything a change touches, and one build and test run proves it.
- **The switchover sequence:**
  1. `plan`: the source set and the decisions.
  2. `migrate` as a rehearsal, with the team still working in the old repositories.
  3. Fixes found by the rehearsal, in the sources or as migration changes.
  4. The freeze: the old repositories are locked (still readable), their pipelines stopped.
  5. `migrate` again as the final run, reusing the rehearsal; or an `update` of the rehearsal's mono-repo.
  6. Push the mono-repo, `clone-prs`, register the pipelines, redirect the old repositories to it.
  7. Developers bring their local work over with `migrate-local-changes`.
  8. `update` or `port-back` while an old repository still has to ship a fix; a rollback with `port-back`
     only if needed.
- **What the user decides:** the source set, the cutover date and freeze, rehearsal-then-final-run or
  rehearsal-then-update, how far the pipelines go, whether internal packages are still published, and every
  outward-facing step.

Then look for a migration under way: a work folder (`<output>.migration` next to the workspace by default),
a mono-repo with the source record, a rehearsal's report. If there is one, say where it stands (which steps
are done, when the sources were last brought in, what the last report left open) and which subcommand comes
next.

## History merge tools

[history-merge.md](history-merge.md) describes how the history is merged: the rules that worked (branches,
bases, tags, cleanup) and the checks that prove the result. The scripts in `scripts/` implement them in five
phases (analysis, migration, cleanup, verification, report), with every source snapshotted first. They are
optional tools: use them when they fit, change their options, or work without them where the project needs
something else. Whatever you use, the checks in that file must pass.
