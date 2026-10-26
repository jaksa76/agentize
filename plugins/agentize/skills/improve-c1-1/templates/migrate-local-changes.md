---
name: migrate-local-changes
description: Bring local work from a clone of one of the old <project> repositories into this mono-repo - uncommitted and untracked files, commits that were never pushed, and stashes - keeping authors and history. Use after the switchover to the mono-repo, when a developer still has work in an old clone.
allowed-tools: Bash Read Write Edit
---

<!--
Template for improve-c1-1's `migrate` subcommand. Adapt it to the project: replace every <...>, keep what
applies, add what the project needs, and remove this comment. It states the goal and the context, not a
method: the agent running it works out how.
-->

# Migrate local changes

The `<project>` repositories were merged into this mono-repo on `<date>`. Each old repository is now a folder
here, with its full history: every commit kept its author, date and message, under a new hash. The old
repositories are locked and read-only.

This skill brings over the work that never reached the old repositories from a developer's old clone:

- uncommitted changes, including untracked files;
- commits that were never pushed, on existing branches or on local-only branches;
- stashes.

Work that was pushed before the switchover is already here, and so are the old repositories' branches.

## Context

- **Where old clones usually are:** <for example, side by side in one workspace folder such as
  `C:\src\<project>\` or `~/src/<project>/`>. Ask the developer if you can't find them.
- **Which clone maps to which folder:** <the source record, for example `<path of the record>`>. It lists
  each old repository's URL, its folder here, and how far each of its branches was brought in. A clone is
  identified by its remote URL, not its folder name.
- **How the old history maps to this one:** each old commit has exactly one counterpart here, with the same
  author, dates and message and the same files under the repository's folder. <How to find it, for example
  "rewriting with `git filter-repo --to-subdirectory-filter <folder>` reproduces it" or "the record's
  mapping">. So an old branch's base can be found here, and the local work applied on top of it.
- **Branch names** that changed in the migration: <for example, `main` became `master`; `<repo>/<branch>`
  for branches split off; `local/<branch>`>.

## Rules

- **Never change the old clone.** Read from it, or from a copy of it. The developer keeps it as it is until
  they are satisfied.
- **Show what will happen first:** for each clone, the branches, commits, stashes and files found, and where
  each will go in the mono-repo. Proceed when the developer agrees.
- **Keep authors and history:** commits stay commits, with their author, date and message; a local branch
  becomes a branch here, based on the counterpart of its old base. Stashes and uncommitted work can become
  work in progress the developer finishes here, unless they say otherwise.
- **Nothing is pushed** unless the developer asks.

## Check afterwards

Anything the migration changed that old work can bring back. In this project:

- <for example, references to internal packages that are now built from source in the mono-repo>;
- <per-folder package-source or tool configs that the mono-repo replaced with root-level ones>;
- <old-style container files, or build files that assume the old repository root>;
- <per-repository pipeline files that the mono-repo's pipelines replaced>.

Then build and test what the work touched, and tell the developer what was brought over, what was left out,
and what they still need to look at.
