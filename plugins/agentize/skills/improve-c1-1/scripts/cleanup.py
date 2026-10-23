#!/usr/bin/env python3
# Copyright (c) 2026 Codomain D.O.O. All rights reserved.
# Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
# See LICENSE.md for details.
"""Phase 3 — Cleanup: tags, merged branches and helper refs, as planned in <work>/analysis.json.

Usage:
    python cleanup.py --work <dir> [--no-gc]

- Release tags: a tag name found in two or more repositories (`v1.2.0`, `1.2.0` and `release-1.2.0` count
  as the same) becomes one annotated tag on a commit that holds every repository at that release: the
  tagged commit where the repository has the tag, otherwise its production branch as of the release date
  (a repository that did not exist yet is left out). Tags of a single repository are kept as <repo>/<tag>.
- Branches merged into develop/master and inactive (see analysis.md) are deleted. Their commits stay in the
  history; the combining commit can be restored with `git branch <name> <tip>` until git's garbage
  collection removes it (two weeks by default).
- refs/sources/ and refs/imported-tags/ are removed and the repository is garbage-collected.
"""
import argparse
import os
import time

import common as c


def parse_args():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--work', required=True)
    ap.add_argument('--no-gc', action='store_true', help="don't run git gc at the end")
    return ap.parse_args()


def main():
    c.set_prefix('cleanup')
    args = parse_args()
    work = os.path.abspath(args.work)
    plan = c.load_json(os.path.join(work, 'analysis.json'))
    mig = c.load_json(os.path.join(work, 'migration.json'))
    output, names = mig['output'], mig['repos']
    started = time.time()
    maps = {name: c.load_commit_map(work, name) for name in names}

    imported = {}
    out = c.git(['for-each-ref', '--format=%(refname) %(objectname)', 'refs/imported-tags'], cwd=output)
    for ref, oid in (line.split(' ') for line in out.splitlines()):
        _, _, repo, tag = ref.split('/', 3)
        imported[(repo, int(tag[1:]))] = oid

    cat = c.CatFile(output)
    combined, used = [], set()
    for t in plan['combined']['tags']['combined']:
        parents, entries = [], []
        for name in names:
            src = (t['members'].get(name) or t['fill'].get(name) or {}).get('commit')
            if not src:
                continue
            commit = maps[name][src]
            parents.append(commit)
            found = cat.oid(f'{commit}:{name}')
            if found:
                entries.append((name, found[0]))
        tree = c.mktree(output, entries)
        tagged = [f"- {n}: {m['name']}" + (f" ({m['subject']})" if m.get('subject') else '')
                  for n, m in sorted(t['members'].items())]
        filled = [f"- {n}: {f['branch']}" for n, f in sorted(t['fill'].items())]
        missing = [n for n in names if n not in t['members'] and n not in t['fill']]
        message = (f"Release {t['final']}\n\nTagged in {len(tagged)} repositories:\n" + '\n'.join(tagged) + '\n')
        if filled:
            message += f"\nNot tagged, taken from their production branch as of {c.day(t['date'])}:\n" + '\n'.join(filled) + '\n'
        if missing:
            message += f"\nDid not exist yet: {', '.join(missing)}\n"
        cmd = ['commit-tree', tree]
        for p in parents:
            cmd += ['-p', p]
        env = c.commit_env(t['date'])
        commit = c.git(cmd, cwd=output, input=message, env=env).strip()
        c.git(['tag', '-a', '-F', '-', t['final'], commit], cwd=output, input=message, env=env)
        used.update((n, m['tag_index']) for n, m in t['members'].items())
        combined.append({'name': t['final'], 'commit': commit, 'tagged': len(tagged), 'filled': len(filled),
                         'missing': len(missing), 'date': t['date']})
    cat.close()
    c.log(f'Created {len(combined)} combined release tags')

    updates, per_repo = [], []
    for t in plan['combined']['tags']['per_repo']:
        oid = imported[(t['repo'], t['tag_index'])]
        updates.append(f"create refs/tags/{t['final']} {oid}\n")
        used.add((t['repo'], t['tag_index']))
        per_repo.append({'name': t['final'], 'reason': t['reason']})
    if updates:
        c.git(['update-ref', '--stdin'], cwd=output, input=''.join(updates))
    uncovered = set(imported) - used
    if uncovered:
        c.die(f'{len(uncovered)} imported tag(s) were not turned into a tag, e.g. {sorted(uncovered)[0]}; '
              'refs/imported-tags/ is left in place.')
    c.log(f'Kept {len(per_repo)} tags under their repository name')

    pruned, deletes = [], []
    for name, b in mig['branches'].items():
        if b['prune']:
            deletes.append(f"delete refs/heads/{name} {b['tip']}\n")
            pruned.append({'name': name, 'tip': b['tip'], 'owners': b['owners'], 'reason': b['prune_reason']})
    out = c.git(['for-each-ref', '--format=%(refname)', 'refs/sources', 'refs/imported-tags'], cwd=output)
    deletes += [f'delete {ref}\n' for ref in out.split()]
    c.git(['update-ref', '--stdin'], cwd=output, input=''.join(deletes))
    c.log(f'Deleted {len(pruned)} merged, inactive branches and the helper refs')

    if not args.no_gc:
        c.log('Running git gc')
        c.git(['gc', '--quiet'], cwd=output)

    state = {'created': c.now_iso(), 'combined_tags': combined, 'per_repo_tags': per_repo, 'pruned': pruned,
             'seconds': round(time.time() - started)}
    c.save_json(os.path.join(work, 'cleanup.json'), state)
    remaining = len(mig['branches']) - len(pruned)
    lines = ['# Cleanup', '',
             f'- **{len(combined)} release tags** combine the same tag across repositories '
             f'({sum(t["filled"] for t in combined)} repository snapshots taken from the production branch at the '
             'release date, because those repositories had no such tag).',
             f'- **{len(per_repo)} tags** exist in one repository only and are kept as `<repo>/<tag>`.',
             f'- **{len(pruned)} branches deleted**: merged into develop/master and inactive; '
             f'{remaining} branches remain.',
             '- Helper refs (`refs/sources/`, `refs/imported-tags/`) removed' +
             ('; repository garbage-collected.' if not args.no_gc else '.')]
    if combined:
        lines += ['', '## Release tags', '', '| Tag | Date | Tagged | From production branch | Did not exist |',
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
    c.write_text(os.path.join(work, 'cleanup.md'), '\n'.join(lines) + '\n')
    c.log(f"Done in {state['seconds']}s")


if __name__ == '__main__':
    main()
