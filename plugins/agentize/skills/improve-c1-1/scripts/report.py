#!/usr/bin/env python3
# Copyright (c) 2026 Codomain D.O.O. All rights reserved.
# Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
# See LICENSE.md for details.
"""Phase 5 — Report: join the phase summaries into <work>/migration-report.md.

Usage:
    python report.py --work <dir>
"""
import argparse
import os

import common as c


def plural(n, word, many=None):
    return f"{n} {word if n == 1 else many or word + 's'}"


def demote(markdown):
    """Moves a phase summary's headings one level down, under the report's own sections."""
    return '\n'.join('#' + line if line.startswith('#') else line for line in markdown.splitlines())


def read(work, name):
    path = os.path.join(work, name)
    if not os.path.exists(path):
        return f'# {name}\n\nThis phase did not run.'
    with open(path, encoding='utf-8') as f:
        return f.read()


def main():
    c.set_prefix('report')
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--work', required=True)
    work = os.path.abspath(ap.parse_args().work)
    plan = c.load_json(os.path.join(work, 'analysis.json'))
    mig = c.load_json(os.path.join(work, 'migration.json'))
    cln = c.load_json(os.path.join(work, 'cleanup.json'))
    ver_path = os.path.join(work, 'verification.json')
    ver = c.load_json(ver_path) if os.path.exists(ver_path) else None
    repos, comb = plan['repos'], plan['combined']

    commits = sum(r['commits'] for r in repos)
    branches = len(mig['branches'])
    split = sum(1 for b in mig['branches'].values() if b['split_from'])
    merged = sum(1 for b in mig['branches'].values() for x in b['composition'].values() if x['role'] == 'merged')
    left_out = sum(1 for b in mig['branches'].values() for x in b['composition'].values() if x['role'] == 'none')
    pruned = len(cln['pruned'])
    dropped = sum(len(r['dropped']) for r in repos)
    local_used = [(r['name'], b) for r in repos for b in r['branches'] if b['origin'] == 'local']
    behind = [(r['name'], b) for r in repos for b in r['branches'] if 'behind; used the remote' in b['note']]
    result = ('not run' if ver is None else 'all checks passed' if ver['ok']
              else f"{sum(not x['ok'] for x in ver['checks'])} check(s) FAILED")
    ci = [(r['name'], r['checks']['ci']) for r in repos if r.get('checks', {}).get('ci')]

    lines = ['# Monorepo migration report', '',
             '| | |', '|---|---|',
             f"| Monorepo | `{mig['output']}` |",
             f"| Sources | {len(repos)} repositories: {', '.join(r['name'] for r in repos)} |",
             f"| Default branch | `{mig['default_branch']}` |",
             f"| History | {commits} commits, authorship and dates kept; new commit hashes |",
             f"| Branches | {branches} combined, {pruned} pruned, **{branches - pruned} remain** |",
             f"| Tags | {len(cln['combined_tags'])} release tags, {len(cln['per_repo_tags'])} kept as `<repo>/<tag>` |",
             f"| Verification | **{result}** |",
             f"| Work folder | `{work}` |", '',
             '## Changes made without asking', '',
             'Each one follows a fixed rule; the details are in the phase sections below.', '',
             f"- **{plural(len(comb['renames']), 'branch', 'branches')} renamed** so that names differing only in letter case, or a "
             'branch that is also a folder of other branch names, can coexist.',
             f"- **{plural(dropped, 'local branch', 'local branches')} left out**:"
             f' they hold no commits that are not on the remote.',
             f"- **{plural(len(behind), 'out-of-date local branch', 'out-of-date local branches')}** replaced by the newer remote "
             f"branch; **{plural(len(local_used), 'local branch', 'local branches')}** migrated"
             f' because they hold unpushed commits.',
             f"- **{plural(split, 'branch', 'branches')} split off** as `<repo>/<branch>`: the repository created it "
             'from a different trunk than the others, or the name was reused for different work.',
             f"- **{plural(merged, 'repository folder')}** in combined branches hold the branch the repository "
             'already merged into, because other repositories still work on that branch; '
             f"**{plural(left_out, 'repository folder')}** left out of branches that share no history with them.",
             '- Migration options: ' + (', '.join(f'`{x}`' for x in mig['changed_options'])
                                        if mig['changed_options'] else 'the defaults') + '.',
             f"- **{plural(pruned, 'branch', 'branches')} deleted**: their commits are all on other branches "
             '(merged and inactive, or chosen in the cleanup review).',
             f"- **{len(cln['combined_tags'])} release tags** created from the same release across repositories; "
             'repositories without that tag are included at their production branch as of the release date.',
             '- Cleanup review: ' + ('; '.join(cln['review_changes']) if cln.get('review_changes')
                                     else 'the proposed plan was applied unchanged') + '.',
             '', '## Needs attention', '']
    attention = list(plan['warnings'])
    if ver and not ver['ok']:
        attention = [f"Verification failed: {', '.join(x['check'] for x in ver['checks'] if not x['ok'])} "
                     '(see Verification below).'] + attention
    lines += [f'- {w}' for w in attention] or ['- Nothing.']
    lines += ['', '## Next steps (not part of this migration)', '',
              '- **Build and CI**: the pipelines still expect each repository at the root' +
              (f" ({sum(len(x) for _, x in ci)}+ pipeline files in {len(ci)} repositories)" if ci else '') +
              '; they are adapted in the next phase, together with the build scripts.',
              '- **Publish**: push to a new remote with `git push --all` and `git push --tags`; nothing has been '
              'pushed. Then make the old repositories read-only rather than deleting them, so links to their '
              'commits, pull requests and builds keep working.',
              '- **Open work**: anyone with unpushed work in the old repositories moves it over with '
              '`git format-patch` / `git am --directory=<folder>`.', '']
    for name in ('analysis.md', 'migration.md', 'cleanup.md', 'verification.md'):
        lines += [demote(read(work, name)), '']
    path = os.path.join(work, 'migration-report.md')
    c.write_text(path, '\n'.join(lines))
    c.log(f'Wrote {path}')


if __name__ == '__main__':
    main()
