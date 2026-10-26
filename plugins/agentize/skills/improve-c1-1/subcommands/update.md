<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# `update`

Bring in what the sources got since the last run, keeping the mono-repo's own changes.

It is needed even with the old repositories locked: until the new pipelines are green, a production fix may
have to go through an old repository. It is also one way through the freeze: update the rehearsal's mono-repo
instead of migrating again (the user chooses in `plan`).

## Done when

- Every source branch's new history is in the mono-repo, under the source's folder, with authors, dates and
  messages kept, and the mono-repo's record says how far each source branch is now brought in.
- The mono-repo's own changes are intact, and nothing from the sources undoes them.
- New branches and tags are in, following the migration's rules and its recorded decisions.
- Branches deleted in a source are reported, not applied.
- The mono-repo still builds and its tests pass, apart from known failures.
- The user has a summary: what came in per source, conflicts and how they were resolved, what was reported
  and not applied.

## The user decides

Conflicts where a source change and a migration change both make sense and can't both be kept; whether a
branch deleted in a source should go here too. Propose a resolution.

## Lessons and pitfalls

- **Merging keeps the mono-repo's changes.** Because rewriting is deterministic, a source's new history,
  rewritten the same way as in the migration, descends from commits already in the mono-repo, so it merges
  like any branch. A conflict means a source commit touched something the migration changed; that is the
  place to look, not to resolve blindly.
- **New branches and tags follow the migration's rules,** and its recorded decisions where they apply. Only
  what has no decision yet needs fresh review.
- **"Folder equals source" no longer holds.** Verify instead that each source's history is contained in the
  mono-repo, and that each folder differs from its source only where the migration changed it: the
  difference between the two is exactly the mono-repo's own changes to that folder.
- **Check the record first.** It says how far each source was brought in. If the mono-repo was changed
  somewhere it doesn't say (a hand-made merge, a cherry-pick from an old repository), find out before adding
  history on top.
