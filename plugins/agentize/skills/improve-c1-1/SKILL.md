---
name: improve-c1-1
description: Improve readiness criterion C1.1 (Codebase Accessibility) in the current project by creating or enhancing the agent context file (CLAUDE.md). Raises the fulfillment level by one step.
allowed-tools: Bash Read Write Edit
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Improve C1.1 — Codebase Accessibility

## Current State

Examine the project to understand its current state:

- Check for agent context files (`CLAUDE.md`, `AGENTS.md`, or equivalent) and read their full content.
- Read `README.md` to assess its depth.
- Look at the project root structure and source directories to understand the layout and technology stack.
- Identify key build, run, and test commands from the build manifest or Makefile.

## Instructions

**Step 1 — Determine current level:**
- Level 0: No README and no CLAUDE.md/AGENTS.md
- Level 1: README exists but no CLAUDE.md/AGENTS.md (or it's minimal)
- Level 2: CLAUDE.md or AGENTS.md exists with substantive conventions, commands, and navigation guidance

**Step 2 — Implement the improvement:**

**If current level is 0 → raise to 1:**
Create a `README.md` at the project root with at minimum:
- Project name and one-paragraph description of what it does and why
- Getting started section (prerequisites, how to clone and run)
- Basic project structure overview

**If current level is 1 → raise to 2:**
Create a `CLAUDE.md` at the project root. Base it on the evidence above (README content, detected language/framework, directory structure, build scripts). Include:

```markdown
# CLAUDE.md

## Project Overview
[brief description of what this project does]

## Key Commands
[list the most important commands: build, test, run, lint — use the actual commands detected above]

## Project Structure
[describe the main directories and what lives in them]

## Coding Conventions
[list conventions: naming style, file organisation, patterns used — infer from the existing code structure]

## Important Notes
[any non-obvious constraints, environment variables required, external services, known gotchas]
```

Read enough of the actual codebase to write accurate, project-specific content. Do not write generic placeholder text.

**If already at level 2:**
Report that C1.1 is already at its maximum level (2) and no improvement is needed.

**Step 3 — Report:**
State what file was created or modified, what level it was at before, and what level it is now.

## Merging Separate Repositories into a Mono-repo

When the codebase is split across several repositories and the user wants them combined, use `${CLAUDE_SKILL_DIR}/scripts/merge-repos.sh`. It is a one-time migration: it creates a new repository and never modifies the sources.

**Step 1 — Prepare:**
- Confirm with the user the list of source repositories (URL or local path) and the folder name each should get in the combined repo.
- Make sure `git filter-repo` is available (`git filter-repo --version`); if not, ask the user to install it (`pip install git-filter-repo`).

**Step 2 — Run the script:**

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/merge-repos.sh" --output <new-dir> \
  --repo "<name>=<url-or-path>" --repo "<name>=<url-or-path>" ...
```

The script rewrites each repo's history so its files live under `<name>/`, then creates one branch per branch name found in any source. Each combined branch merges that branch from every repo; repos without it contribute the branch it would have been created from (gitflow: `feature/*`, `bugfix/*`, `release/*` → `develop`; `hotfix/*`, `support/*` → `master`/`main`; otherwise the default branch). It ends with a verification report and exits non-zero if any check fails. Show the user the report and the branch composition, and investigate any failure before continuing.

**Step 3 — Merge the tags:**
The script does not create tags. Each source tag is stored as `refs/imported-tags/<name>/<tag>`, pointing at the rewritten commit. Run the following in the output repository.

1. List them: `git for-each-ref --sort=creatordate --format='%(refname:lstrip=2)  %(creatordate:iso)' refs/imported-tags/`
2. Group tags that represent the same release across repos (release train): the same name, or the same version written differently (`v1.2.0`, `1.2.0`, `release-1.2.0`), created close together in time. Propose the grouping and the combined tag names to the user and wait for confirmation.
3. For each group, create a commit containing every repo at its tagged state, and tag it:
   - For each repo in the group, take the tagged commit `C=$(git rev-parse 'refs/imported-tags/<name>/<tag>^{commit}')` and its folder `git rev-parse "$C:<name>"`.
   - For a repo with no tag in the group, use its latest commit before the release date: `git rev-list -1 --before=<date> <default-branch> -- <name>/` (skip the repo if there is none).
   - Build the tree with `git mktree` (one `040000 tree <folder-hash><TAB><name>` line per repo), create the commit with `git commit-tree <tree> -p <C1> -p <C2> ... -m "Release <version>"`, and tag it with `git tag -a <tag> -m "<release, listing the source tags>" <commit>`.
4. Fallback for tags that do not belong to any group: keep them under the repo name, `git update-ref refs/tags/<name>/<tag> refs/imported-tags/<name>/<tag>`.
5. Check that every imported tag is covered by a combined or fallback tag, then delete the namespace: `git for-each-ref --format='delete %(refname)' refs/imported-tags/ | git update-ref --stdin`.

**Step 4 — Report:**
Report the output location, the branch composition, the tags created (combined and fallback), and anything that needs the user's attention. Do not push the combined repository anywhere; that is the user's decision.
