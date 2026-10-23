#!/usr/bin/env python3
# Copyright (c) 2026 Codomain D.O.O. All rights reserved.
# Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
# See LICENSE.md for details.
"""Phase 2 — Migration: build the monorepo from the plan in <work>/analysis.json.

Usage:
    python migrate.py --work <dir> --output <new repository folder> [options] [--jobs 4] [--keep-rewrites]

1. Each repository's planned branches and tags are copied from its snapshot and its history is rewritten
   with git filter-repo so that every commit has its files under <name>/. Commits shared by branches map
   to the same rewritten commit, so merge bases are kept. Author, committer, dates and messages are kept;
   commit hashes change (filter-repo also updates hashes quoted in commit messages).
2. One combined branch is created per branch name: a commit whose tree holds every repository's folder and
   whose parents are the branches each repository contributes. The defaults are those shown in analysis.md;
   the options below change them.
3. The rewritten branches stay in refs/sources/<name>/ and the tags in refs/imported-tags/<name>/ for the
   cleanup phase. Uncommitted work, stashes and reflogs are not carried over.

Options (each may be repeated where it takes a branch):
    --mixed-bases split|combine   branches created from different trunks: the minority moves to
                                  <repo>/<branch> (split, default) or all stay together (combine)
    --split BRANCH                split this branch by trunk even with --mixed-bases combine
    --split BRANCH:REPO           move REPO's BRANCH to <repo>/<branch> (e.g. the name was reused)
    --combine BRANCH              keep this branch together even though its trunks differ
    --merged-content target|tip   a repository that already merged a branch others still work on contributes
                                  the branch it merged into (target, default) or its old branch tip (tip)
    --fallback PATTERN=KIND       what repositories without a matching branch contribute; PATTERN is a glob
                                  (`release/*`), KIND one of base, develop, production, default, none
    --contribute BRANCH:REPO=SRC  REPO contributes its branch SRC (or `none`) to BRANCH; only for
                                  repositories that don't have BRANCH themselves
    --default-branch NAME         the monorepo's default branch
"""
import argparse
import fnmatch
import os
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import common as c


def parse_args():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--work', required=True)
    ap.add_argument('--output', required=True, help='the new repository; must not exist or be empty')
    ap.add_argument('--jobs', type=int, default=min(4, os.cpu_count() or 1))
    ap.add_argument('--keep-rewrites', action='store_true', help='keep <work>/rewrite/ for debugging')
    ap.add_argument('--mixed-bases', choices=('split', 'combine'), default='split')
    ap.add_argument('--split', action='append', default=[], metavar='BRANCH[:REPO]')
    ap.add_argument('--combine', action='append', default=[], metavar='BRANCH')
    ap.add_argument('--merged-content', choices=('target', 'tip'), default='target')
    ap.add_argument('--fallback', action='append', default=[], metavar='PATTERN=KIND')
    ap.add_argument('--contribute', action='append', default=[], metavar='BRANCH:REPO=SRC')
    ap.add_argument('--default-branch')
    return ap.parse_args()


def options(args, plan):
    """The command-line options as compose() takes them, checked against the plan."""
    repos = {r['name']: r for r in plan['repos']}
    names = {b['target'] for r in plan['repos'] for b in r['branches']}
    o = {'mixed_bases': args.mixed_bases, 'merged_content': args.merged_content, 'split': [], 'combine': [],
         'fallbacks': [], 'contribute': [], 'default_branch': args.default_branch}
    for item in args.split:
        branch, _, repo = item.partition(':')
        if branch not in names or (repo and repo not in repos):
            c.die(f"--split {item}: no branch '{branch}'" + (f" or repository '{repo}'" if repo else ''))
        if repo and branch not in repos[repo]['targets']:
            c.die(f"--split {item}: {repo} has no branch '{branch}'")
        o['split'].append(item)
    for branch in args.combine:
        if branch not in names:
            c.die(f"--combine {branch}: no such branch")
        o['combine'].append(branch)
    for item in args.fallback:
        pattern, _, kind = item.rpartition('=')
        if not pattern or kind not in c.FALLBACK_KINDS:
            c.die(f"--fallback {item}: expected PATTERN=KIND, KIND one of {', '.join(c.FALLBACK_KINDS)}")
        if not any(fnmatch.fnmatchcase(n.lower(), pattern.lower()) for n in names):
            c.warn(f'--fallback {item}: matches no branch')
        o['fallbacks'].append((pattern, kind))
    for item in args.contribute:
        branch, _, rest = item.partition(':')
        repo, _, src = rest.partition('=')
        if repo not in repos or not src:
            c.die(f'--contribute {item}: expected BRANCH:REPO=SRC with a known repository')
        if branch in repos[repo]['targets']:
            c.die(f"--contribute {item}: {repo} has its own '{branch}'; use --split or --merged-content")
        if src != 'none' and src not in repos[repo]['targets']:
            c.die(f"--contribute {item}: {repo} has no branch '{src}'")
        o['contribute'].append({'branch': branch, 'repo': repo, 'source': None if src == 'none' else src})
    return o


def changed_options(o):
    """The options that differ from the defaults, as they were given on the command line."""
    d, out = c.default_options(), []
    for key, flag in (('mixed_bases', '--mixed-bases'), ('merged_content', '--merged-content'),
                      ('default_branch', '--default-branch')):
        if o[key] != d[key]:
            out.append(f'{flag} {o[key]}')
    out += [f'--split {x}' for x in o['split']] + [f'--combine {x}' for x in o['combine']]
    out += [f"--fallback '{p}={k}'" for p, k in o['fallbacks']]
    out += [f"--contribute {x['branch']}:{x['repo']}={x['source'] or 'none'}" for x in o['contribute']]
    return out


def rewrite(repo, work):
    """Rewrites one repository under <name>/; branches become refs/heads/b<i>, tags refs/tags/t<i>."""
    name = repo['name']
    snap = os.path.join(work, 'snapshot', name + '.git')
    dest = os.path.join(work, 'rewrite', name + '.git')
    c.rmtree(dest)
    c.git(['init', '--bare', '-q', dest])
    # Neutral ref names: the real names may differ only in case, which this files-backed repo can't hold.
    refspecs = [f"+{b['ref']}:refs/heads/b{i}" for i, b in enumerate(repo['branches'])]
    refspecs += [f"+{t['ref']}:refs/tags/t{i}" for i, t in enumerate(repo['tags'])]
    c.git(['fetch', '-q', '--no-tags', '--stdin', snap], cwd=dest, input='\n'.join(refspecs) + '\n')
    p = subprocess.run([sys.executable, '-m', 'git_filter_repo', '--force', '--quiet',
                        '--to-subdirectory-filter', name, '--replace-refs', 'delete-no-add',
                        '--preserve-commit-encoding'], cwd=dest, capture_output=True, text=True)
    if p.returncode != 0:
        raise c.GitError(f'git filter-repo failed for {name}: {p.stderr.strip() or p.stdout.strip()}')
    os.makedirs(os.path.join(work, 'commit-maps'), exist_ok=True)
    shutil.copyfile(os.path.join(dest, 'filter-repo', 'commit-map'), os.path.join(work, 'commit-maps', name))
    c.log(f'{name}: rewritten')
    return dest


def main():
    c.set_prefix('migrate')
    args = parse_args()
    work = os.path.abspath(args.work)
    output = os.path.abspath(args.output)
    plan = c.load_json(os.path.join(work, 'analysis.json'))
    if subprocess.run([sys.executable, '-c', 'import git_filter_repo'], capture_output=True).returncode != 0:
        c.die('git-filter-repo is not installed for this Python. Install it: python -m pip install git-filter-repo')
    if os.path.exists(output) and os.listdir(output):
        c.die(f'{output} already exists and is not empty. This is a one-time migration; choose a new folder.')
    repos = plan['repos']
    names = [r['name'] for r in repos]
    opts = options(args, plan)
    try:
        default, branches = c.compose(plan, opts)
    except ValueError as e:
        c.die(str(e))
    unknown = {x['branch'] for x in opts['contribute']} - {b['name'] for b in branches}
    if unknown:
        c.die(f"--contribute: no combined branch {', '.join(sorted(unknown))}")
    started = time.time()

    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        rewritten = dict(zip(names, pool.map(lambda r: rewrite(r, work), repos)))

    os.makedirs(output, exist_ok=True)
    c.git(['init', '-q', '-b', default, output])
    # Deep paths under <name>/ need long path support on Windows; a no-op elsewhere.
    c.git(['config', 'core.longpaths', 'true'], cwd=output)
    for name in names:
        c.git(['fetch', '-q', '--no-tags', rewritten[name],
               f'+refs/heads/*:refs/sources/{name}/*', f'+refs/tags/*:refs/imported-tags/{name}/*'], cwd=output)
    c.log(f'Imported {len(names)} rewritten repositories')

    # Rewritten tip and date of every repository branch, by target name.
    tips = {}
    out = c.git(['for-each-ref', '--format=%(refname) %(objectname) %(committerdate:unix)', 'refs/sources'], cwd=output)
    by_ref = {ref: (oid, int(ts)) for ref, oid, ts in (line.split(' ') for line in out.splitlines())}
    for r in repos:
        for i, b in enumerate(r['branches']):
            tips[(r['name'], b['target'])] = by_ref[f"refs/sources/{r['name']}/b{i}"]

    cat = c.CatFile(output)
    subtrees = {}

    def subtree(commit, name):
        if (commit, name) not in subtrees:
            found = cat.oid(f'{commit}:{name}')
            subtrees[(commit, name)] = found[0] if found else None
        return subtrees[(commit, name)]

    roles = {'own': '', 'fallback': ' (does not have this branch)', 'override': ' (chosen for this migration)',
             'merged': ' (already merged its own branch there)'}
    created, updates, placement = {}, [], {}
    moved = {(b['split_from'], b['owners'][0]): b['name'] for b in branches if b['split_from']}
    for n, b in enumerate(branches, start=1):
        parents, entries, msg, dates = [], [], [], []
        for name in names:
            part = b['composition'][name]
            if part['role'] == 'own':
                placement.setdefault(name, {})[part['content']] = b['name']
            for p in part['parents']:
                commit, ts = tips[(name, p)]
                parents.append(commit)
                dates.append(ts)
            if part['content']:
                tree = subtree(tips[(name, part['content'])][0], name)
                if tree:
                    entries.append((name, tree))
            msg.append(f"- {name}: {part['content']}{roles[part['role']]}" if part['content']
                       else f'- {name}: not included (no history in common with this branch)')
            if part['role'] == 'merged' and len(part['parents']) > 1:
                msg[-1] += f"; its branch '{part['parents'][1]}' is the next parent"
            if (b['name'], name) in moved:
                msg[-1] = (f"- {name}: {part['content'] or 'not included'} "
                           f"(its own branch is {moved[(b['name'], name)]})")
        tree = c.mktree(output, entries)
        message = (f"Combine branch '{b['name']}' from {len(names)} repositories\n\n"
                   f"Each parent is one repository's branch:\n" + '\n'.join(msg) + '\n')
        args_ = ['commit-tree', tree]
        for p in parents:
            args_ += ['-p', p]
        tip = c.git(args_, cwd=output, input=message, env=c.commit_env(max(dates))).strip()
        created[b['name']] = dict(b, tip=tip, parents=parents)
        updates.append(f"create refs/heads/{b['name']} {tip}\n")
        if n % 50 == 0 or n == len(branches):
            c.log(f'Combined branches: {n}/{len(branches)}')
    cat.close()
    c.git(['update-ref', '--stdin'], cwd=output, input=''.join(updates))

    c.log(f"Checking out '{default}'")
    c.git(['symbolic-ref', 'HEAD', f'refs/heads/{default}'], cwd=output)
    c.git(['reset', '-q', '--hard'], cwd=output)
    if not args.keep_rewrites:
        c.rmtree(os.path.join(work, 'rewrite'))

    counts = {}
    for name in names:
        with open(os.path.join(work, 'commit-maps', name), encoding='ascii') as f:
            counts[name] = sum(1 for _ in f) - 1
    changed = changed_options(opts)
    state = {'created': c.now_iso(), 'output': output, 'default_branch': default, 'repos': names,
             'options': opts, 'changed_options': changed, 'branches': created, 'placement': placement,
             'rewritten_commits': counts, 'seconds': round(time.time() - started)}
    c.save_json(os.path.join(work, 'migration.json'), state)
    lines = ['# Migration', '', f'Created `{output}` on {state["created"]} in {state["seconds"]} s.', '',
             f'- {len(names)} repositories rewritten under their own folder: '
             f'{sum(counts.values())} commits, history and authorship kept, new commit hashes.',
             f'- {len(created)} combined branches; each is one commit whose parents are the repositories\' '
             'branches, so `git log -- <folder>` shows that repository\'s full history.',
             f"- Default branch: `{default}` (checked out).",
             '- Options: ' + (', '.join(f'`{x}`' for x in changed) if changed else 'the defaults shown in the analysis.'),
             '- Not migrated: uncommitted changes, stashes, reflogs, and the remotes\' pull requests, reviews and '
             'build history (they are not part of git).']
    decided = [b for b in branches if b['notes']]
    if decided:
        lines += ['', '## Branches not combined as is', '', '| Branch | What was done |', '|---|---|']
        lines += [f"| `{b['name']}` | {'; '.join(n['text'] for n in b['notes'])} |" for b in decided]
    c.write_text(os.path.join(work, 'migration.md'), '\n'.join(lines) + '\n')
    c.log(f"Done in {state['seconds']}s: {output}")


if __name__ == '__main__':
    main()
