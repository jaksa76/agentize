<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# `plan`

Decide the source set and everything the migration needs decided, before migrating. A source missed here
means migrating again later.

## Done when

- The source set is complete and justified: every repository in it has a reason, and every repository of the
  hosting project left out of it is listed with its reason.
- Every internal artifact a source consumes (package, image, generated client, shared template) is built by a
  source, or is explicitly accepted as coming from outside.
- What changes meaning once a repository becomes a subfolder is listed per repository, with what `migrate`
  will do about it.
- The user's decisions (below) are made, and all decisions are recorded with their reasons where `migrate`
  will find them (the work folder, which `migrate` carries into the mono-repo). A later rehearsal or final run
  reuses them.
- The user has seen a short summary: the source set, what was left out and why, the decisions, and the risks
  found.

## The user decides

- The source set, after seeing your proposal and what you left out.
- The migration's shape: rehearsal then final run during a freeze, or rehearsal then `update` during the
  freeze (shorter freeze, but merge commits, and the rehearsal's decisions stay as they were).
- How far the pipelines go: per-component pipelines with path triggers, or merged pipelines that build only
  what a change affects; and whether deployments become per change.
- Whether internal packages are still published for consumers outside the mono-repo.
- The mono-repo's name, where it will be hosted, and its default branch if the sources disagree.
- The cutover date and how long the freeze may take; who locks the old repositories.

Propose an answer for each, with its trade-off; don't ask open questions.

## Yours to decide

Everything about the history (see [history-merge.md](../history-merge.md)), the folder names, and how to
record what the subcommands need in common.

## Lessons

- **Repos were missed.** In the example project, two repositories that consumed the sources' internal
  packages weren't in the set. Every internal artifact a source consumes should be built by a source. Anything
  outside the set that consumes what the sources build is a candidate too. Compare against the whole hosting
  project (the organisation, group or project on the hosting service), so leaving a repository out is a
  visible decision rather than an oversight.
- **Stray clones.** A workspace folder is not a source set. The example workspace held clones that didn't
  belong: an `infrastructure` repository of another team, a template repository, an unused fork. Repositories
  sharing a first commit are forks or copies; decide which one is the source.
- **Things that change meaning as subfolders.** Look for what silently changes once a repository is no longer
  at the root:
  - config that tools look up from parent folders (editor, formatter, linter, package manager and build
    settings), which now finds another repository's or the root's file;
  - scripts that assume they are at the repository root; tests for `.git` broke three scripts in the example;
  - versions derived from tags, now renamed or combined into release tags;
  - hooks installed for the whole repository;
  - pipeline definitions under odd names (`azure-piplines*.yml` in the example) or in subfolders, which a
    name-based search misses; look at what the hosting service has registered too;
  - paths that reach outside the repository (`../other-repo`), which now point into the mono-repo.
- **Local work that won't be migrated.** Uncommitted changes, unpushed commits and stashes in the clones
  you can see are a sample of what every developer has. They are what `migrate-local-changes` is for; note
  them, don't block on them.
