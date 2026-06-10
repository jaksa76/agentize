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

- Look at the project root structure to understand the overall layout and whether there is a single entry point.
- Read `README.md` and assess whether this repository is part of a larger multi-repo setup.
- Check for dependencies and references to other repositories in documentation, build files, or configuration files.
- Check for any indicators of a multi-repo setup (gitmodules, symlinks, references to other repos).
- Inspect CI/CD workflows and build scripts for cross-repo checkout/copy patterns (for example `actions/checkout` with `repository: org/other-repo`, `git clone org/other-repo`, or `cp` from externally checked-out repos).
- Inspect dependency/config manifests for explicit sibling-repo links (for example git URLs, path dependencies, workspace mappings, or automation keys/tokens used to fetch another repo).

### Project-Context Requirement (Inbound Check)

Evaluate C1.1 from a story-delivery perspective, not only local repo structure.

- If this repository is mainly consumed by sibling repos as shared utilities/tooling, treat it as part of a split multi-repo codebase for end-to-end delivery.
- Consider only **project-code coupling** as inbound evidence. Ignore generic third-party reusable actions/tools unless they pull this repository's code.

### Minimum Evidence Checklist

Before final scoring, confirm all checks below:

1. Repo-internal layout (`README.md`, root folders, app/module structure).
2. Technical linking mechanisms (`.gitmodules`, git subtree/workspace linking, checked-in path links).
3. Cross-repo consumption evidence from workflows/build/docs (checkout/clone/copy/import of sibling repos).

Do not assign **Level 2** unless checks 2, 3, and 4 show no cross-repo split of code ownership relevant to build/runtime/tooling and end-to-end story delivery.

## Instructions

Gather the evidence described above and determine the fulfillment level for C1.1.

Scoring guide:
- **Level 0**: Code is split across unlinked repositories. This includes multi-repo setups that only reference each other in README/docs, cases where CI/build pulls code from sibling repos without submodule/subtree/workspace-style technical linking.
- **Level 1**: Repos are technically linked through submodules or equivalent mechanisms (for example git submodules, git subtree, or workspace-level linking checked into the repo).
- **Level 2**: Monolith or Mono-repo with no evidence that required project code is sourced from other repositories.

### Disambiguation Rules

- A repository containing multiple internal packages/folders (for example `utils/`, `shared/`, `docs/`) is **not automatically Level 2**.
- If another repo must be checked out/cloned/copied for implementing a user story end to end, treat as split codebase and score **Level 0** unless a formal technical linking mechanism justifies **Level 1**.
- If sibling repos depend on this repo for code needed in their build/deploy/runtime/test flows, this repo is not independently sufficient for end-to-end story delivery; prefer **Level 0** unless formal technical linking justifies **Level 1**.
- In rationale, cite concrete file-level evidence (for example workflow file and step name) when cross-repo coupling is detected.

Report in exactly this format:

**C1.1 — Codebase Accessibility**
- **Level**: [0 / 1 / 2]
- **Rationale**: [one or two sentences citing the specific evidence]