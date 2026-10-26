<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# `port-back`

Carry mono-repo work back to a source repository: a rollback, a hotfix that has to go through an old
pipeline, or a repository that stays separate. The arguments name the work (commits, a branch, a pull
request) and, if it isn't clear from them, the source.

## Done when

- The chosen work is on a branch of each source repository it touches, based on the source commit that
  corresponds to where the work started in the mono-repo, with authors, dates and messages kept.
- The mono-repo's own changes are left out: nothing on that branch comes from the migration's changes.
- The work is translated back to how that repository builds. For example, references to sibling folders
  become package references at published versions.
- The branch builds and its tests pass in the source repository, or what fails is reported.
- When the work spans a library and its consumers, the report gives the release order: which package version
  must be published before which consumer can build.
- Nothing is pushed unless the user asks.

## The user decides

Which work to port; whether to push; the release order, if publishing is involved.

## Lessons

- Because rewriting is deterministic, every mono-repo commit inside a source's folder maps back to exactly one
  source commit; the record says how far each source was brought in. Work done after the switchover sits on
  top of that, and the folder's part of it is what goes back.
- Work that touches several folders becomes one branch per source repository. Keep the pieces recognisable as
  one change (the same message, a shared reference to the work item).
- A rollback is the same operation for everything done since the switchover. Before it, check what the old
  repositories got in the meantime (their lock may have had exceptions).
