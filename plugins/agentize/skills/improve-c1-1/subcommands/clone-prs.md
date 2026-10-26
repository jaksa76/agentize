<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# `clone-prs`

Recreate the sources' open pull requests in the mono-repo, once it is pushed.

## Done when

- Every open pull request of the sources has an equivalent in the mono-repo: its source branch, its target,
  its title, its description, its linked work items and its reviewers, and a link to the original.
- Running it again creates nothing twice: a pull request that already has an equivalent is recognised (by
  its link to the original, for example) and left alone or updated.
- The user has a summary: what was created, what was skipped and why.

## The user decides

- Creating them: show the list of pull requests to create (original, branches, title, reviewers) and wait for
  confirmation.
- Whether to close the originals, and with what comment. Also outward-facing; show it first.

## Lessons and pitfalls

- If a pull request's branch moved after the last run, `update` first, so the mono-repo's branch has the
  pull request's latest commits.
- A source branch whose name changed in the migration (case, a `<repo>/<branch>` split, a folder clash) is
  found through the mono-repo's record and the migration's decisions, not by name.
- A pull request's branch here holds every repository's folder; its diff against the target must show only
  the original's changes. If it shows more, the branch was combined differently from its target; find out
  why before creating it.
- Use the hosting service's own interface (its CLI or API: Azure DevOps, GitHub, GitLab, Bitbucket, ...).
  Comments and review history don't carry over; the link to the original keeps them reachable.
