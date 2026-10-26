<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# `migrate`

A mono-repo with full history that builds, tests, runs and deploys as one, plus the `migrate-local-changes`
skill for developers. Run as a **rehearsal** while the team still works in the old repositories, or as the
**final run** during the freeze, reusing the rehearsal.

If `plan` hasn't run, or its decisions don't cover what you find, do that part of `plan` first. The output is a
new folder (`<project>-monorepo` next to the workspace by default) that must not exist yet; the work folder
is `<output>.migration`.

## Done when

- **The history is verified against the sources,** before any change of the mono-repo's own: every source
  commit, branch and tag is accounted for, and each folder equals its source where it should (see the checks
  in [history-merge.md](../history-merge.md)).
- **The mono-repo records its sources** and how far each was brought in, and its own changes are
  distinguishable from the sources' history (see SKILL.md, "What the subcommands need in common").
- **It builds as one and its tests pass,** apart from failures the sources already had, each of which is
  listed with its evidence from the baseline.
- **The images, the local environment and the pipelines work from it,** as far as they can be checked
  without pushing. What can only be checked after the push is listed.
- **`migrate-local-changes` is in it and tested** on a throwaway clone with each kind of local work.
- **The report** (`<work>/migration-report.md`, extending the history merge's report) says what was decided
  and why, what changed and why, what is known to fail and since when, and the switchover checklist: what
  is still to do, by whom, in which order, with every outward-facing step marked.

## The user decides

What `plan` left open, and anything that turns out to need a decision of the kind `plan` lists: a library
that can't be built with its consumers without a breaking change, a pipeline that can't be merged, a test
that only passes against a shared environment. Ask with a proposal, and keep going with the rest meanwhile.

## Yours to decide

The history (see [history-merge.md](../history-merge.md)), the order of the work, and how to fix the build.
Commit the mono-repo's own changes locally as you go; push nothing.

## Lessons

- **Take a baseline before changing anything.** Right after the merge, each folder equals its source.
  Building and testing there separates the failures that already existed from the migration's. In the
  example project, 41 test failures were attributed by hand; one of them was a test pinning a bug that the
  library had already fixed.
- **Build internal libraries with their consumers,** not through published packages. Otherwise a library
  change still isn't built and tested with its consumers, which is most of the point of a mono-repo. Whether
  the packages are still published for outside consumers is the user's call.
  - Expect fixes where consumers were behind the library's head: in the example, an old beta still in use,
    a removed option still being set.
  - Expect conflicts that only appear once everything builds together, like a package downgrade.
- **Builds that reach other folders** need the root as their context (the container builds in the example).
- **Machine resources.** Building and testing everything at once is a new load. The example run ran out of
  memory three times; limit parallelism.
- **Pipelines.**
  - Inventory them first, including who consumes their artifacts by name; in the example, another
    repository's pipelines did.
  - Path triggers must include the dependency closure: a component's pipeline runs when anything it builds
    from changes.
  - "What changed" must be measured from the last *successful* build, not the previous commit.
  - Deploying only what differs needs a record of what each environment runs.
  - Pipelines can't run before they are registered, so check them locally as far as possible: their syntax,
    the paths they reference, the commands they run.
- **Rehearsal and final run.**
  - The final run reuses the rehearsal's decisions and changes. Keeping the changes as commits makes them
    replayable onto the new history, and a conflict then marks exactly what changed during the freeze.
  - The alternative is to `update` the rehearsal's mono-repo during the freeze. That makes the freeze
    shorter, but adds merge commits and keeps the rehearsal's decisions fixed. The user chooses (in `plan`).
  - Reuse the rehearsal's snapshots, and review only what is new since then: branches, tags, repositories.
- **Lock and redirect** belong in the checklist: lock the old repositories (still readable), add a README
  pointing to the mono-repo, disable their pipelines. These are outward-facing; propose them, don't do them.

## `migrate-local-changes`

A skill in the mono-repo, for developers after the switchover. It brings over what never reached the old
repositories: uncommitted files (including untracked ones), commits that were never pushed, and stashes.
Developers use it without agentize, so it ships with the mono-repo from the first push, in the place the
project's agents look for skills (for example `.claude/skills/migrate-local-changes/SKILL.md`).

Write it for this project, starting from [the template](../templates/migrate-local-changes.md). Like
this skill, it states the goal and the context, not a method. Test it on a throwaway clone of a source with
each kind of local work (an uncommitted change, an untracked file, an unpushed commit on an existing branch,
a local-only branch, a stash), and check that the old clone is unchanged afterwards.
