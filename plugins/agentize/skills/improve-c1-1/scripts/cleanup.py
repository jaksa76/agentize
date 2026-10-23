#!/usr/bin/env python3
# Copyright (c) 2026 Codomain D.O.O. All rights reserved.
# Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
# See LICENSE.md for details.
"""Phase 3 — Cleanup, in two steps: propose a plan, review and edit it, apply it.

Usage:
    python cleanup.py --work <dir> --plan             writes <work>/cleanup-plan.json and cleanup-plan.md
    python cleanup.py --work <dir> --apply [--no-gc]  carries out <work>/cleanup-plan.json

--plan proposes, from the analysis and the migration:
- release tags: a tag name found in two or more repositories (`v1.2.0`, `1.2.0` and `release-1.2.0` count as
  the same) becomes one annotated tag on a commit that holds every repository at that release: the tagged
  commit where the repository has the tag, otherwise its production branch as of the release date.
- tags of a single repository, kept as <repo>/<tag>
- branches to delete: merged into develop/master in every repository that has them, and inactive
and lists what deserves a second look: release tags whose dates are far apart, single-repository tags
created around the same time as other repositories' tags (a release under different names), and branches
that could be deleted without losing anything but are kept by the rules.

Edit cleanup-plan.json where the review shows the proposal is wrong, then run --apply. Its format:

    release_tags     [{"name": "v1.2.0", "members": {"<repo>": "<source tag>", ...},
                       "fill": "auto" | {"<repo>": {"branch": "master", "at": "<ISO date>"} | {"commit": "<sha>"}},
                       "note": "<why, if you changed it>"}]
                     fill: what the repositories without a member tag contribute; "auto" means their
                     production branch as of the latest member tag; a repository left out of an explicit
                     fill is left out of the release.
    repo_tags        [{"repo": "<repo>", "tag": "<source tag>", "name": "<new tag name>", "note": ""}]
    delete_branches  [{"name": "<branch>", "reason": "..."}]

Other fields are information for the review and are ignored. Every source tag must appear exactly once, as a
release member or a repository tag. --apply refuses to delete branches whose commits are not all on another
branch or tag, so nothing of the sources' history can be lost. Finally it removes the helper refs
(refs/sources/, refs/imported-tags/) and runs git gc.
"""
import argparse
import datetime
import os
import shutil
import time
from collections import Counter

import common as c

# Tags of one release spread over more days than this are probably different releases.
SAME_RELEASE_DAYS = 30
# Tags of different repositories created this close together may be one release under different names.
NEAR_DAYS = 3


def parse_args():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--work', required=True)
    step = ap.add_mutually_exclusive_group(required=True)
    step.add_argument('--plan', action='store_true', help='propose the cleanup for review')
    step.add_argument('--apply', action='store_true', help='carry out the reviewed cleanup-plan.json')
    ap.add_argument('--no-gc', action='store_true', help="don't run git gc at the end")
    return ap.parse_args()


def iso(ts):
    return datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def lost_commits(output, tips, kept):
    """How many commits reachable from `tips` are not reachable from `kept` (commits or tags)."""
    revs = list(tips) + [f'^{k}' for k in kept]
    return int(c.git(['rev-list', '--count', '--stdin'], cwd=output, input='\n'.join(revs) + '\n').strip())


def branch_dates(plan):
    """The last commit date of every combined branch name, over the repositories that have it."""
    dates = {}
    for r in plan['repos']:
        for b in r['branches']:
            dates[b['target']] = max(dates.get(b['target'], 0), b['date'])
    return dates


# ---------------------------------------------------------------------------
# Step 1: propose
# ---------------------------------------------------------------------------

def propose(work, plan, mig):
    output = mig['output']
    repos = {r['name']: r for r in plan['repos']}
    tags = plan['combined']['tags']

    everything = [(t['date'], r['name'], t['name']) for r in plan['repos'] for t in r['tags']
                  if c.VERSION_TAG.match(t['name'])]
    release_tags = []
    for t in tags['combined']:
        dates = sorted((m['date'], rn) for rn, m in t['members'].items())
        warnings = []
        if dates[-1][0] - dates[0][0] > SAME_RELEASE_DAYS * 86400:
            warnings.append(f"tagged from {c.day(dates[0][0])} ({dates[0][1]}) to {c.day(dates[-1][0])} "
                            f"({dates[-1][1]}): probably different releases sharing a version number")
        if t['variants']:
            warnings.append(f"spelled differently: {', '.join([t['name']] + t['variants'])}")
        release_tags.append({
            'name': t['final'],
            'members': {rn: m['name'] for rn, m in sorted(t['members'].items())},
            'fill': {rn: {'branch': f['branch'], 'at': iso(t['date'])} for rn, f in sorted(t['fill'].items())},
            'dates': {rn: c.day(m['date']) for rn, m in sorted(t['members'].items())},
            'warnings': warnings, 'note': ''})

    repo_tags = []
    for t in tags['per_repo']:
        src = repos[t['repo']]['tags'][t['tag_index']]
        near = [f'{rn} {name} ({c.day(d)})' for d, rn, name in everything
                if rn != t['repo'] and abs(d - src['date']) <= NEAR_DAYS * 86400]
        warnings = []
        if near and c.VERSION_TAG.match(t['name']):
            warnings.append(f"created within {NEAR_DAYS} days of {', '.join(near[:4])}"
                            f"{', ...' if len(near) > 4 else ''}: possibly the same release under another name")
        repo_tags.append({'repo': t['repo'], 'tag': t['name'], 'name': t['final'], 'date': c.day(src['date']),
                          'reason': t['reason'], 'warnings': warnings, 'note': ''})

    # Branches: the rule's deletions, and the branches that could go without losing anything.
    dates = branch_dates(plan)
    heads = {name: b['tip'] for name, b in mig['branches'].items()}
    tags_kept = c.git(['for-each-ref', '--format=%(objectname)', 'refs/imported-tags'], cwd=output).split()
    delete, candidates = [], []
    for name, b in sorted(mig['branches'].items(), key=lambda kv: kv[0].lower()):
        if b['prune']:
            delete.append({'name': name, 'reason': b['prune_reason']})
            continue
        if b['protected'] or name == mig['default_branch']:
            continue
        others = [tip for n, tip in heads.items() if n != name] + tags_kept
        if lost_commits(output, [b['tip']], others) <= 1:
            origin = b['split_from'] or name
            last = dates.get(origin, 0)
            merged = all(x.get('in_trunk') for r in plan['repos'] if r['name'] in b['owners']
                         for x in r['branches'] if x['target'] == origin)
            why = 'all its commits are also on other branches or tags'
            why += (f'; merged, but kept because it counts as recent (last commit {c.day(last)})' if merged
                    else f'; last commit {c.day(last)}')
            candidates.append({'name': name, 'owners': b['owners'], 'last_commit': c.day(last), 'why': why})
    squash = [i for i in plan['combined'].get('issues', []) if i['kind'] in ('squash-merged', 'partly merged')]

    proposal = {'created': c.now_iso(), 'release_tags': release_tags, 'repo_tags': repo_tags,
                'delete_branches': delete, 'delete_candidates': candidates,
                'kept_merged': [{'branch': i['branch'], 'detail': i['detail']} for i in squash]}
    c.save_json(os.path.join(work, 'cleanup-plan.json'), proposal)
    c.save_json(os.path.join(work, 'cleanup-plan.proposed.json'), proposal)
    c.write_text(os.path.join(work, 'cleanup-plan.md'), render_plan(proposal))
    flagged = sum(bool(t['warnings']) for t in release_tags + repo_tags)
    c.log(f'Proposed {len(release_tags)} release tags, {len(repo_tags)} repository tags, {len(delete)} branch '
          f'deletions; {flagged} tag(s) and {len(candidates)} branch(es) to review.')
    c.log(f"Review {os.path.join(work, 'cleanup-plan.md')}, edit cleanup-plan.json, then run --apply")


def render_plan(p):
    lines = ['# Cleanup plan', '', 'Proposed; review it, edit `cleanup-plan.json` where it is wrong, then run '
             '`cleanup.py --apply`.', '']
    flagged = [t for t in p['release_tags'] + p['repo_tags'] if t['warnings']]
    lines += ['## To review', '']
    lines += [f"- tag `{t['name']}`: {'; '.join(t['warnings'])}" for t in flagged]
    lines += [f"- branch `{b['name']}` ({', '.join(b['owners'])}): {b['why']}" for b in p['delete_candidates']]
    if not flagged and not p['delete_candidates']:
        lines += ['- Nothing.']
    lines += ['', f"## Release tags ({len(p['release_tags'])})", '',
              '| Tag | Tagged in | Taken from the production branch | Warnings |', '|---|---|---|---|']
    for t in p['release_tags']:
        tagged = ', '.join(f'{rn} `{tag}` ({t["dates"][rn]})' for rn, tag in t['members'].items())
        lines.append(f"| `{t['name']}` | {tagged} | {', '.join(t['fill']) or '-'} | {'; '.join(t['warnings']) or '-'} |")
    lines += ['', f"## Tags kept under the repository name ({len(p['repo_tags'])})", '',
              '| Tag | Source | Date | Warnings |', '|---|---|---|---|']
    lines += [f"| `{t['name']}` | {t['repo']} `{t['tag']}` | {t['date']} | {'; '.join(t['warnings']) or '-'} |"
              for t in p['repo_tags']]
    lines += ['', f"## Branches to delete ({len(p['delete_branches'])})", '']
    lines += [f"- `{b['name']}`: {b['reason']}" for b in p['delete_branches']] or ['- None.']
    if p['kept_merged']:
        lines += ['', '## Merged branches that are kept', '',
                  'Merged by squash or rebase, or still open in another repository: their commits exist only on '
                  'these branches, so they cannot be deleted without losing history.', '']
        lines += [f"- `{k['branch']}`: {k['detail']}" for k in p['kept_merged']]
    return '\n'.join(lines) + '\n'


# ---------------------------------------------------------------------------
# Step 2: apply
# ---------------------------------------------------------------------------

def validate(cp, plan, mig):
    """Checks the reviewed plan; returns the problems found."""
    repos = {r['name']: r for r in plan['repos']}
    problems = []
    # Malformed entries are reported, not crashed on; the checks below only look at well-formed ones.
    malformed = [(f"release tag #{i + 1}", 'needs a "name" and a non-empty "members" object')
                 for i, t in enumerate(cp['release_tags'])
                 if not isinstance(t, dict) or not t.get('name') or not isinstance(t.get('members'), dict)
                 or not t['members'] or not (t.get('fill', 'auto') == 'auto' or isinstance(t.get('fill'), dict))]
    malformed += [(f"repository tag #{i + 1}", 'needs "repo", "tag" and "name"') for i, t in enumerate(cp['repo_tags'])
                  if not isinstance(t, dict) or not all(t.get(k) for k in ('repo', 'tag', 'name'))]
    malformed += [(f"branch deletion #{i + 1}", 'needs a "name"') for i, b in enumerate(cp['delete_branches'])
                  if not isinstance(b, dict) or not b.get('name')]
    if malformed:
        return [f'{what}: {need}' for what, need in malformed]
    seen = Counter()
    for t in cp['release_tags']:
        for rn, tag in t['members'].items():
            seen[(rn, tag)] += 1
        fill = t.get('fill', 'auto')
        if fill != 'auto':
            for rn, spec in fill.items():
                if rn not in repos:
                    problems.append(f"release tag {t['name']}: unknown repository '{rn}' in fill")
                elif rn in t['members']:
                    problems.append(f"release tag {t['name']}: {rn} is both a member and in fill")
                elif not isinstance(spec, dict):
                    problems.append(f"release tag {t['name']}: fill for {rn} must be an object")
                elif 'commit' not in spec and spec.get('branch') not in repos[rn]['targets']:
                    problems.append(f"release tag {t['name']}: {rn} has no branch '{spec.get('branch')}'")
    for t in cp['repo_tags']:
        seen[(t['repo'], t['tag'])] += 1
    source = {(r['name'], t['name']) for r in plan['repos'] for t in r['tags']}
    problems += [f'unknown source tag {rn}:{tag}' for rn, tag in sorted(set(seen) - source)]
    problems += [f'source tag {rn}:{tag} is used {n} times' for (rn, tag), n in sorted(seen.items()) if n > 1]
    problems += [f'source tag {rn}:{tag} is not in the plan' for rn, tag in sorted(source - set(seen))]

    names = [t['name'] for t in cp['release_tags']] + [t['name'] for t in cp['repo_tags']]
    lowered = Counter(n.lower() for n in names)
    problems += [f'tag name {n} is used more than once (ignoring case)' for n in sorted(set(names))
                 if lowered[n.lower()] > 1]
    problems += [f"tag name {n} is also a folder of another tag name"
                 for n in sorted(c.resolve_dir_file(set(names), '-tag'))]
    for n in names:
        if c.git_ok(['check-ref-format', f'refs/tags/{n}'])[0] != 0:
            problems.append(f"'{n}' is not a valid tag name")

    deletes = [b['name'] for b in cp['delete_branches']]
    problems += [f"branch {n} does not exist" for n in deletes if n not in mig['branches']]
    problems += [f"branch {n} is listed twice" for n, k in Counter(deletes).items() if k > 1]
    if mig['default_branch'] in deletes:
        problems.append(f"the default branch {mig['default_branch']} cannot be deleted")
    return problems


def describe_changes(cp, proposed):
    """What the review changed in the proposal, in a few lines."""
    changes = []
    before = {t['name']: t['members'] for t in proposed['release_tags']}
    after = {t['name']: t['members'] for t in cp['release_tags']}
    # A tag that disappeared while another one with the same members appeared was renamed.
    gone, new = set(before) - set(after), set(after) - set(before)
    for old in sorted(gone):
        renamed = next((n for n in sorted(new) if after[n] == before[old]), None)
        if renamed:
            changes.append(f'release tag `{old}` renamed to `{renamed}`')
            gone.discard(old)
            new.discard(renamed)
    for name in sorted(gone):
        changes.append(f'release tag `{name}` not created')
    for name in sorted(new):
        changes.append(f"release tag `{name}` added ({', '.join(f'{r} {t}' for r, t in after[name].items())})")
    for name in sorted(set(after) & set(before)):
        if after[name] != before[name]:
            changes.append(f"release tag `{name}` regrouped ({', '.join(f'{r} {t}' for r, t in after[name].items())})")
    for t in cp['release_tags']:
        old = next((x for x in proposed['release_tags'] if x['name'] == t['name']), None)
        if old and t.get('fill', 'auto') not in ('auto', old['fill']):
            changes.append(f"release tag `{t['name']}`: repositories without the tag changed")
    before = {(t['repo'], t['tag']): t['name'] for t in proposed['repo_tags']}
    for t in cp['repo_tags']:
        if before.get((t['repo'], t['tag'])) != t['name']:
            changes.append(f"{t['repo']} `{t['tag']}` kept as `{t['name']}`")
    old_del = {b['name'] for b in proposed['delete_branches']}
    new_del = {b['name'] for b in cp['delete_branches']}
    changes += [f'branch `{n}` kept' for n in sorted(old_del - new_del)]
    changes += [f'branch `{n}` deleted' for n in sorted(new_del - old_del)]
    return changes


def apply(work, plan, mig, no_gc):
    output, names = mig['output'], mig['repos']
    started = time.time()
    path = os.path.join(work, 'cleanup-plan.json')
    if not os.path.exists(path):
        c.die('No cleanup-plan.json; run cleanup.py --plan first.')
    cp = c.load_json(path)
    for key in ('release_tags', 'repo_tags', 'delete_branches'):
        cp.setdefault(key, [])
    problems = validate(cp, plan, mig)
    if problems:
        c.die(f"cleanup-plan.json has {len(problems)} problem(s):\n  " + '\n  '.join(problems[:30]))
    repos = {r['name']: r for r in plan['repos']}
    tag_index = {(r['name'], t['name']): i for r in plan['repos'] for i, t in enumerate(r['tags'])}
    maps = {name: c.load_commit_map(work, name) for name in names}

    imported = {}
    out = c.git(['for-each-ref', '--format=%(refname) %(objectname)', 'refs/imported-tags'], cwd=output)
    for ref, oid in (line.split(' ') for line in out.splitlines()):
        _, _, repo, tag = ref.split('/', 3)
        imported[(repo, int(tag[1:]))] = oid

    def fill_commit(rn, spec, date):
        """The source commit a repository without the tag contributes to a release, or None."""
        if spec.get('commit'):
            return spec['commit']
        ref = next(b['ref'] for b in repos[rn]['branches'] if b['target'] == spec['branch'])
        snap = os.path.join(work, 'snapshot', rn + '.git')
        at = spec.get('at') or f'@{date}'
        return c.git(['rev-list', '-1', '--first-parent', f'--before={at}', ref], cwd=snap).strip() or None

    name_, email = c.identity()
    tagger = f'{name_} <{email}>'
    cat = c.CatFile(output)
    combined, updates, kept = [], [], []
    for t in cp['release_tags']:
        members = {rn: {'tag': tag, 'source': repos[rn]['tags'][tag_index[(rn, tag)]]['commit']}
                   for rn, tag in t['members'].items()}
        date = max(repos[rn]['tags'][tag_index[(rn, m['tag'])]]['date'] for rn, m in members.items())
        fill_spec = t.get('fill', 'auto')
        if fill_spec == 'auto':
            fill_spec = {r['name']: {'branch': r['production']} for r in plan['repos'] if r['name'] not in members}
        fill = {}
        for rn, spec in fill_spec.items():
            src = fill_commit(rn, spec, date)
            if src:
                fill[rn] = {'branch': spec.get('branch') or src[:12], 'source': src}
        parents, entries = [], []
        for name in names:
            src = (members.get(name) or fill.get(name) or {}).get('source')
            if not src:
                continue
            if src not in maps[name]:
                c.die(f"release tag {t['name']}: {name} commit {src} was not migrated")
            commit = maps[name][src]
            parents.append(commit)
            found = cat.oid(f'{commit}:{name}')
            if found:
                entries.append((name, found[0]))
        tree = c.mktree(output, entries)
        tagged = []
        for rn, m in sorted(members.items()):
            subject = repos[rn]['tags'][tag_index[(rn, m['tag'])]].get('subject')
            tagged.append(f"- {rn}: {m['tag']}" + (f' ({subject})' if subject else ''))
        filled = [f"- {rn}: {f['branch']}" for rn, f in sorted(fill.items())]
        missing = [n for n in names if n not in members and n not in fill]
        message = f"Release {t['name']}\n\nTagged in {len(tagged)} repositories:\n" + '\n'.join(tagged) + '\n'
        if filled:
            message += (f"\nNot tagged, taken from their branch as of {c.day(date)}:\n" + '\n'.join(filled) + '\n')
        if missing:
            message += f"\nNot included: {', '.join(missing)}\n"
        cmd = ['commit-tree', tree]
        for p in parents:
            cmd += ['-p', p]
        commit = c.git(cmd, cwd=output, input=message, env=c.commit_env(date)).strip()
        # The tag object is written now, its ref only in the final transaction below.
        tag_object = c.git(['mktag'], cwd=output, input=(
            f"object {commit}\ntype commit\ntag {t['name']}\ntagger {tagger} {date} +0000\n\n{message}")).strip()
        updates.append(f"create refs/tags/{t['name']} {tag_object}\n")
        kept.append(commit)
        combined.append({'name': t['name'], 'commit': commit, 'tagged': len(tagged), 'filled': len(filled),
                         'missing': len(missing), 'date': date, 'members': members, 'fill': fill,
                         'note': t.get('note', '')})
    cat.close()

    per_repo = []
    for t in cp['repo_tags']:
        i = tag_index[(t['repo'], t['tag'])]
        updates.append(f"create refs/tags/{t['name']} {imported[(t['repo'], i)]}\n")
        kept.append(imported[(t['repo'], i)])
        per_repo.append({'name': t['name'], 'repo': t['repo'], 'tag': t['tag'],
                         'source': repos[t['repo']]['tags'][i]['commit'],
                         'reason': t.get('reason', ''), 'note': t.get('note', '')})

    # Deleting a branch may only lose its combining commit: everything else on it must stay reachable from
    # the remaining branches or the new tags. Checked before anything is changed.
    deleted = {b['name']: b for b in cp['delete_branches']}
    heads = dict(line.split(' ') for line in c.git(['for-each-ref', '--format=%(refname:lstrip=2) %(objectname)',
                                                     'refs/heads'], cwd=output).splitlines())
    pruned = [{'name': n, 'tip': heads[n], 'owners': mig['branches'][n]['owners'], 'reason': b.get('reason', '')}
              for n, b in deleted.items()]
    if pruned:
        others = [tip for n, tip in heads.items() if n not in deleted] + kept
        total = lost_commits(output, [p['tip'] for p in pruned], others)
        if total != len(pruned):
            unsafe = [p['name'] for p in pruned if lost_commits(output, [p['tip']], others) > 1]
            c.die(f'Deleting these branches would lose {total - len(pruned)} commit(s) that are on no other branch '
                  f"or tag: {', '.join(unsafe) or 'a combination of them'}. Remove them from delete_branches. "
                  'Nothing was changed.')
    updates += [f"delete refs/heads/{p['name']} {p['tip']}\n" for p in pruned]
    out = c.git(['for-each-ref', '--format=%(refname)', 'refs/sources', 'refs/imported-tags'], cwd=output)
    updates += [f'delete {ref}\n' for ref in out.split()]
    # One transaction: either every tag and deletion happens, or none does.
    c.git(['update-ref', '--stdin'], cwd=output, input='start\n' + ''.join(updates) + 'commit\n')
    c.log(f'Created {len(combined)} release tags and {len(per_repo)} repository tags; deleted {len(pruned)} '
          'branches and the helper refs')

    if not no_gc:
        c.log('Running git gc')
        c.git(['gc', '--quiet'], cwd=output)

    proposed_path = os.path.join(work, 'cleanup-plan.proposed.json')
    changes = describe_changes(cp, c.load_json(proposed_path)) if os.path.exists(proposed_path) else []
    shutil.copyfile(path, os.path.join(work, 'cleanup-plan.applied.json'))
    state = {'created': c.now_iso(), 'combined_tags': combined, 'per_repo_tags': per_repo, 'pruned': pruned,
             'review_changes': changes, 'seconds': round(time.time() - started)}
    c.save_json(os.path.join(work, 'cleanup.json'), state)
    c.write_text(os.path.join(work, 'cleanup.md'), render_result(state, mig, no_gc))
    c.log(f"Done in {state['seconds']}s")


def render_result(state, mig, no_gc):
    combined, per_repo, pruned = state['combined_tags'], state['per_repo_tags'], state['pruned']
    lines = ['# Cleanup', '',
             f'- **{len(combined)} release tags** combine the same release across repositories '
             f'({sum(t["filled"] for t in combined)} repository snapshots taken from a branch at the release '
             'date, because those repositories had no such tag).',
             f'- **{len(per_repo)} tags** are kept under their repository name.',
             f'- **{len(pruned)} branches deleted**; {len(mig["branches"]) - len(pruned)} branches remain.',
             '- Helper refs (`refs/sources/`, `refs/imported-tags/`) removed' +
             ('; repository garbage-collected.' if not no_gc else '.')]
    if state['review_changes']:
        lines += ['', '## Changed in review', '', 'The proposed plan was changed before it was applied:', '']
        lines += [f'- {x}' for x in state['review_changes']]
    notes = [(t['name'], t['note']) for t in combined + per_repo if t.get('note')]
    if notes:
        lines += ['', '## Review notes', '']
        lines += [f'- `{n}`: {note}' for n, note in notes]
    if combined:
        lines += ['', '## Release tags', '', '| Tag | Date | Tagged | From a branch | Not included |',
                  '|---|---|---:|---:|---:|']
        lines += [f"| `{t['name']}` | {c.day(t['date'])} | {t['tagged']} | {t['filled']} | {t['missing']} |"
                  for t in combined]
    if per_repo:
        lines += ['', '## Tags kept under the repository name', '',
                  ', '.join(f"`{t['name']}`" for t in per_repo)]
    if pruned:
        lines += ['', '## Deleted branches', '',
                  'Restore one with `git branch <name> <tip>` (within two weeks, before garbage collection '
                  'removes the combining commit); the repositories\' commits themselves are all still in the history.',
                  '', '| Branch | Repositories | Reason | Tip |', '|---|---|---|---|']
        lines += [f"| `{p['name']}` | {', '.join(p['owners'])} | {p['reason']} | `{p['tip'][:12]}` |" for p in pruned]
    return '\n'.join(lines) + '\n'


def main():
    c.set_prefix('cleanup')
    args = parse_args()
    work = os.path.abspath(args.work)
    plan = c.load_json(os.path.join(work, 'analysis.json'))
    mig = c.load_json(os.path.join(work, 'migration.json'))
    if args.plan:
        propose(work, plan, mig)
    else:
        apply(work, plan, mig, args.no_gc)


if __name__ == '__main__':
    main()
