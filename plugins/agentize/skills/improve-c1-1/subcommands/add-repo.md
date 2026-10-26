<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# `add-repo`

Bring one more repository into an existing mono-repo. The argument names the repository (a path or URL), and
optionally its folder.

## Done when

- The repository is in the mono-repo under its own folder, with its full history, its branches (joined with
  the mono-repo's branches of the same name, following the migration's rules) and its tags.
- Its history is verified against the source, as in the migration.
- It is adapted like the others: built with the rest, its internal dependencies taken from source, its
  pipelines, images and local environment brought in line with the mono-repo's.
- The mono-repo's record lists it, and `migrate-local-changes` knows about it.
- The user has a summary, including the trade-off below.

## The user decides

Whether to add the repository or to migrate again (below); which of its branches to bring in when they don't
match the mono-repo's.

## The trade-off

History before the add doesn't contain the folder, so an old release checks out incomplete. Before the
cutover, migrating again is cleaner: the rehearsal's decisions and changes make it cheap. After the cutover,
`add-repo`. Say which applies.

## Lessons

- `plan`'s checks apply to this repository too: what it consumes from the mono-repo, what consumes it, and
  what changes meaning once it is a subfolder.
- A repository added because it was missed is a sign that the source set may still be incomplete; look again
  at what consumes the mono-repo's artifacts.
