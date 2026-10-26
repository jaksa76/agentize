# improve-c1-1: subcommands for a whole migration

From the CheckIT Learning migration (2026-10-23, 37 repos, rehearsed again on 2026-10-26 with 39). The history merge
worked without a single migration option. Most of the effort went into what the skill leaves for "a later, separate
step": making the mono-repo build, test, run and deploy. One finding belonged before the merge: two source repos were
missing, which means migrating again. And a real switchover needs more than one run: a rehearsal, a final run during
a code freeze, then stragglers, open pull requests and work that never left a developer's machine.

The plan: improve-c1-1 gets subcommands, one per step of a switchover. The one thing it generates for the project is
the `migrate-local-changes` skill in the mono-repo.

## How the skill should be written

The agent running it will likely be more capable than the one that wrote it. So each subcommand states:
- its goal, and what must be true afterwards (how to check it);
- what is the user's to decide;
- the lessons learned, as pitfalls to look out for.

It does not state step lists, commands or a fixed method. No new scripts: the agent writes what it needs for the
project in front of it, and throws it away afterwards. Examples come from one project and say so; they show what to
look for, not what to do.

## Subcommands

| Subcommand | Goal |
|---|---|
| *(none)* | Explain the process, and where a migration under way stands and what comes next |
| `plan` | Decide the source set and everything the migration needs decided, before migrating |
| `migrate` | A mono-repo with full history that builds, tests, runs and deploys as one, plus `migrate-local-changes`; as a rehearsal, or the final run reusing the rehearsal |
| `update` | Bring in what the sources got since the last run, keeping the mono-repo's own changes |
| `add-repo` | Bring one more repository into an existing mono-repo |
| `clone-prs` | Recreate the sources' open pull requests in the mono-repo |
| `port-back` | Carry mono-repo work back to a source repository: a rollback, a hotfix through an old pipeline, a repository that stays separate |

Locally, nothing is pushed. Anything outward-facing (pull requests, locks) is shown first and needs the user's
confirmation.

## What the subcommands need in common

These are needs; the agent picks the mechanism.

- **The mono-repo knows its sources.** `update`, `port-back`, `clone-prs` and `migrate-local-changes` run later, on
  other machines. Record in the mono-repo itself which source maps to which folder, and how far each was brought in.
- **The mono-repo's own changes stay distinguishable from the sources' history.** These are the changes for building,
  pipelines and the local environment. A final run replays them; `update` must keep them; `port-back` must leave them
  out.
- **Decisions are reusable.** The final run during the freeze should not redo the rehearsal's review. Only what
  changed since then (new branches, tags, repos) needs fresh review. Snapshots are reused instead of fetched again
  (1.1 GB here).
- **Open question:** whether rewriting the same history twice gives the same commits. `update` and `port-back` are much
  simpler if it does.

## Without a subcommand

Explain:
- what C1.1 is;
- the switchover sequence: plan → rehearsal → fixes → freeze (old repositories locked, still readable) → final run, or
  an update of the rehearsal → push → pull requests, pipelines → developers port their local work → rollback only if
  needed;
- what the user decides.

If a migration is under way, also say where it stands and what comes next.

## `plan`

Done when the source set is complete and justified, and the migration's decisions are made and recorded.

Lessons:
- **Repos were missed.** Two repos that consumed the sources' internal packages weren't in the set. Every internal
  artifact a source consumes should be built by a source. Anything outside the set that consumes what the sources build
  is a candidate too. Compare against the whole hosting project, so leaving a repository out is a visible decision.
- **Stray clones.** A workspace folder held clones that didn't belong (`infrastructure`, a template repo, an unused
  fork).
- **Things that change meaning as subfolders.** Look for what silently changes once a repository becomes a subfolder:
  - config that tools look up from parent folders;
  - scripts that assume they are at the repository root (tests for `.git` broke three scripts here);
  - versions derived from tags, now renamed;
  - hooks installed for the whole repository;
  - pipeline files under odd names (`azure-piplines*.yml`) or in subfolders, which the current check misses.

## `migrate`

Done when:
- the history is verified against the sources;
- the mono-repo builds as one and its tests pass, apart from failures the sources already had;
- the images, the local environment and the pipelines work from it;
- `migrate-local-changes` is in it and tested;
- the report says what was decided, what changed, and what the switchover still needs.

Lessons:
- **Take a baseline before changing anything.** Right after the merge, each folder equals its source. Building and
  testing there separates the failures that already existed from the migration's. Here, 41 test failures were
  attributed by hand. One test pinned a bug that the library had already fixed.
- **Build internal libraries with their consumers,** not through published packages. Otherwise a library change still
  isn't built and tested with its consumers, which is most of the point. Whether the packages are still published for
  outside consumers is the user's call.
  - Expect fixes where consumers were behind the library's head: an old beta, a removed option still being set.
  - Expect conflicts that only appear once everything builds together, like a package downgrade.
- **Builds that reach other folders** need the root as their context (container builds here).
- **Machine resources.** Building and testing everything is a new load. This run ran out of memory three times; limit
  parallelism.
- **Pipelines:**
  - Inventory first, including who consumes their artifacts by name; another repo's pipelines did here.
  - Decide with the user how far to go: per-component pipelines with path triggers, or merged pipelines that build only
    what a change affects.
  - Path triggers must include the dependency closure.
  - "What changed" must be measured from the last *successful* build.
  - Deploying only what differs needs a record of what each environment runs.
  - Pipelines can't run before registration, so check them locally as far as possible.
- **Rehearsal and final run.**
  - The final run reuses the rehearsal's decisions and changes. Keeping those changes as commits makes them replayable,
    and a conflict then marks exactly what changed during the freeze.
  - The alternative is to `update` the rehearsal's mono-repo during the freeze. That makes the freeze shorter, but adds
    merge commits and keeps the rehearsal's decisions fixed. The user chooses.

## `migrate-local-changes` (generated by `migrate`)

A skill in the mono-repo, for developers after the switchover. It brings over what never reached the old
repositories:
- uncommitted files, including untracked ones;
- commits that were never pushed;
- stashes.

Developers use it without agentize, so it ships with the mono-repo from the first push.

Like improve-c1-1, it describes the goal and the context, not a method:
- where old clones usually are;
- how a clone maps to its folder (the recorded sources);
- that authors and history should be kept;
- that the old clone is never changed, and the developer sees what will happen first;
- what to check afterwards: anything the migration changed that old work can bring back. Here that is internal package
  references, per-folder package-source configs, old-style Dockerfiles and per-repo pipeline files.

`migrate` tests it on a throwaway clone with each kind of local work.

## `update`

Done when every source branch's new history is in the mono-repo, the mono-repo's own changes are intact, and nothing
from the sources undoes them.

It is needed even with the old repositories locked: until the new pipelines are green, a production fix may have to go
through an old repository.

Lessons and pitfalls:
- Merging keeps the mono-repo's changes. A conflict means a source commit touched something the migration changed.
- New branches and tags follow the migration's rules. Deleted branches are reported, not applied.
- "Folder equals source" no longer holds. Verify instead that the source's history is contained, and that the folder
  differs from the source only where the migration changed it.

## `add-repo`

Done when the repository is in the mono-repo, with its history and branches, and adapted like the others.

The trade-off against migrating again: history before the add doesn't contain the folder, so an old release checks out
incomplete. Before the cutover, migrating again is cleaner. After it, `add-repo`.

## `clone-prs`

Done when every open pull request of the sources has an equivalent in the mono-repo (source branch, target, title,
description, work items, reviewers), linked to the original. It is idempotent, and created only after the user
confirms. Whether to close the originals is the user's call.

If a pull request's branch moved after the last run, `update` first.

## `port-back`

Done when the chosen mono-repo work is on a branch of the source repository, without the mono-repo's own changes and
translated back to how that repository builds (package references at published versions). Report the release order
when the work spans a library and its consumers. Nothing is pushed unless the user asks.

## Also worth considering

- **Lock and redirect:** lock the old repositories (still readable), add a README pointing to the mono-repo, and
  disable the old pipelines. This is outward-facing, so it belongs in the report's checklist, or in a subcommand that
  asks first.
- **The scoring point:** a merged repository where libraries still flow through published packages arguably meets
  C1.1 level 2 on paper, but not in practice. verify-c1-1 could note it.

## Open questions

- **The existing phase scripts** (`analyze.py` … `verify.py`). They encode rules that worked well, and their
  verification is a strong guarantee. They are also the kind of fixed method this plan avoids. Options:
  - keep them as optional tools, with SKILL.md describing the rules and the checks so an agent can work without them;
  - or drop them.
- Whether `migrate` may commit in the new mono-repo without asking. Proposed: yes, locally, on a work branch, because
  replaying needs commits; never push.
- Which hosting providers to mention as examples, beyond Azure DevOps.
