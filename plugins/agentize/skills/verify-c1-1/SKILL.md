---
name: verify-c1-1
description: Verify readiness criterion C1.1 (Codebase Accessibility) in the current project. Reports fulfillment level 0–2.
allowed-tools: Bash Read
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Verify C1.1 — Codebase Accessibility

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | Code split across unlinked repos |
| 1 | Repos linked through submodules or other mechanisms |
| 2 | Monolith or Mono-repo |

## Evidence to Gather

Assess C1.1 from a story-delivery perspective: can an agent implement a user story end to end with only this repository checked out? Gather evidence in all four areas below.

### 1. Repository layout and project metadata

- Look at the project root structure to understand the overall layout and whether there is a single entry point.
- Read `README.md` and assess whether this repository is described as part of a larger multi-repo setup.
- Look for explicit project metadata that groups repositories together: a `projects.json`, `repos.yaml`, workspace manifest, or equivalent file listing the project's repositories. This is the most reliable source for the project's repository set — when present, use it to enumerate the sibling repositories for the inbound check below.

### 2. Technical linking mechanisms

- Check for `.gitmodules` (git submodules), git subtree remotes or subtree merge commits, checked-in symlinks, and workspace-level linking committed to the repository.
- Check dependency and config manifests for sibling-repo links: git URLs, path dependencies, workspace mappings, or automation keys/tokens whose only purpose is fetching another repository.

### 3. Outbound consumption — what this repository pulls in

- Inspect CI/CD workflows and build scripts for cross-repo checkout/copy patterns, for example `actions/checkout` with `repository: org/other-repo`, `git clone org/other-repo`, or `cp` from an externally checked-out repository.
- Inspect dependency manifests for dependencies on project-owned sibling repositories, whether by git URL, path dependency, or published internal artifact.

### 4. Inbound consumption — what pulls this repository in

Outbound checks alone miss the common case of a shared utility repository, which declares no cross-repo dependencies of its own yet is required by every sibling that does. Inspect inbound coupling as well.

- **When project grouping information is available** (from project metadata, the hosting organisation, or the user), inspect the sibling repositories for references back to *this* repository. Look for:
  - `actions/checkout` with `repository:` naming this repository, or any CI step that clones it
  - `git clone` / `git submodule` / `git subtree` of this repository in build or deploy scripts
  - copy steps that pull files out of a checkout of this repository
  - source imports of this repository's modules or packages
  - path dependencies or workspace entries pointing at this repository
  - shared tooling references: reusable workflows, build plugins, container base images, config, or scripts sourced from this repository
- **When no grouping information is available**, say so in the rationale and score on the evidence you do have. Do not assume the absence of inbound coupling from an unchecked inbound path.

**A utility repository consumed by sibling project repositories is part of a split codebase.** It is not independently sufficient for end-to-end story delivery: a story touching it also touches its consumers.

Consider only **project-code coupling** as inbound evidence. Ignore generic third-party reusable actions and tools — `actions/checkout`, `actions/setup-node`, published upstream libraries — unless they pull this repository's own code.

### Minimum Evidence Checklist

Before final scoring, confirm all four checks below:

1. **Project metadata** — repository layout, `README.md`, and any project/workspace manifest grouping this repository with others.
2. **Technical links** — `.gitmodules`, subtree, workspace linking, checked-in path links.
3. **Outbound consumption** — workflows, build scripts, and manifests that check out, clone, copy, or depend on sibling repositories.
4. **Inbound consumption** — sibling repositories that check out, clone, copy, import, path-depend on, or source shared tooling from this repository.

Do not assign **Level 2** unless all four checks have been performed and checks 2, 3, and 4 show no cross-repo split of code ownership relevant to build, runtime, tooling, or end-to-end story delivery. If a check could not be performed, say which one in the rationale and do not score Level 2 on its absence.

## Instructions

Gather the evidence described above and determine the fulfillment level for C1.1.

Scoring guide:
- **Level 0**: Code is split across unlinked repositories. This includes multi-repo setups that only reference each other in README/docs, cases where CI/build pulls code from sibling repos without submodule/subtree/workspace-style technical linking.
- **Level 1**: Repos are technically linked through submodules or equivalent mechanisms (for example git submodules, git subtree, or workspace-level linking checked into the repo).
- **Level 2**: Monolith or Mono-repo with no evidence that required project code is sourced from other repositories.

### Disambiguation Rules

- A repository containing multiple internal packages/folders (for example `utils/`, `shared/`, `docs/`) is **not automatically Level 2**.
- If another repo must be checked out/cloned/copied for implementing a user story end to end, treat as split codebase and score **Level 0** unless a formal technical linking mechanism justifies **Level 1**.
- If sibling repos depend on this repo for code needed in their build/deploy/runtime/test flows — including as a shared utility or tooling repository — this repo is not independently sufficient for end-to-end story delivery; prefer **Level 0** unless formal technical linking justifies **Level 1**.
- Generic third-party reusable tools and actions that do not pull project-owned code are not evidence of a split codebase and must not lower the score.
- In rationale, cite concrete file-level evidence (for example workflow file and step name) when cross-repo coupling is detected.

Report in exactly this format:

**C1.1 — Codebase Accessibility**
- **Level**: [0 / 1 / 2]
- **Rationale**: [one or two sentences citing the specific evidence]