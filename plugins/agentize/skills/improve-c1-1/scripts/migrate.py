#!/usr/bin/env python3
# Copyright (c) 2026 Codomain D.O.O. All rights reserved.
# Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
# See LICENSE.md for details.
"""Phase 2 — Migration: build the monorepo from the plan in <work>/analysis.json.

Usage:
    python migrate.py --work <dir> --output <new repository folder> [--jobs 4] [--keep-rewrites]

1. Each repository's planned branches and tags are copied from its snapshot and its history is rewritten
   with git filter-repo so that every commit has its files under <name>/. Commits shared by branches map
   to the same rewritten commit, so merge bases are kept. Author, committer, dates and messages are kept;
   commit hashes change (filter-repo also updates hashes quoted in commit messages).
2. One combined branch is created per planned branch name: a commit whose tree holds every repository's
   folder and whose parents are the branch each repository contributes (see analysis.md).
3. The rewritten branches stay in refs/sources/<name>/ and the tags in refs/imported-tags/<name>/ for the
   cleanup phase. Uncommitted work, stashes and reflogs are not carried over.
"""
import argparse
import os
import shutil
import stat
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
    return ap.parse_args()


def rmtree(path):
    """Deletes a folder, including git's read-only object files on Windows."""
    def writable(func, p, _):
        os.chmod(p, stat.S_IWRITE)
        func(p)
    if os.path.exists(path):
        if sys.version_info >= (3, 12):
            shutil.rmtree(path, onexc=writable)
        else:
            shutil.rmtree(path, onerror=writable)


def rewrite(repo, work):
    """Rewrites one repository under <name>/; branches become refs/heads/b<i>, tags refs/tags/t<i>."""
    name = repo['name']
    snap = os.path.join(work, 'snapshot', name + '.git')
    dest = os.path.join(work, 'rewrite', name + '.git')
    rmtree(dest)
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
    started = time.time()

    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        rewritten = dict(zip(names, pool.map(lambda r: rewrite(r, work), repos)))

    default = plan['combined']['default_branch']
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

    branches = plan['combined']['branches']
    created, updates = {}, []
    for n, b in enumerate(branches, start=1):
        parents, entries, msg = [], [], []
        own = set(b['owners'])
        for name in names:
            target = b['composition'][name]
            commit, ts = tips[(name, target)]
            parents.append(commit)
            tree = subtree(commit, name)
            if tree:
                entries.append((name, tree))
            msg.append(f"- {name}: {target}{'' if name in own else ' (does not have this branch)'}")
        tree = c.mktree(output, entries)
        date = max(tips[(name, b['composition'][name])][1] for name in names)
        message = (f"Combine branch '{b['name']}' from {len(names)} repositories\n\n"
                   f"Each parent is one repository's branch:\n" + '\n'.join(msg) + '\n')
        args_ = ['commit-tree', tree]
        for p in parents:
            args_ += ['-p', p]
        tip = c.git(args_, cwd=output, input=message, env=c.commit_env(date)).strip()
        created[b['name']] = {'tip': tip, 'parents': parents}
        updates.append(f"create refs/heads/{b['name']} {tip}\n")
        if n % 50 == 0 or n == len(branches):
            c.log(f'Combined branches: {n}/{len(branches)}')
    cat.close()
    c.git(['update-ref', '--stdin'], cwd=output, input=''.join(updates))

    c.log(f"Checking out '{default}'")
    c.git(['symbolic-ref', 'HEAD', f'refs/heads/{default}'], cwd=output)
    c.git(['reset', '-q', '--hard'], cwd=output)
    if not args.keep_rewrites:
        rmtree(os.path.join(work, 'rewrite'))

    counts = {}
    for name in names:
        with open(os.path.join(work, 'commit-maps', name), encoding='ascii') as f:
            counts[name] = sum(1 for _ in f) - 1
    state = {'created': c.now_iso(), 'output': output, 'default_branch': default, 'repos': names,
             'branches': created, 'rewritten_commits': counts, 'seconds': round(time.time() - started)}
    c.save_json(os.path.join(work, 'migration.json'), state)
    lines = ['# Migration', '', f'Created `{output}` on {state["created"]} in {state["seconds"]} s.', '',
             f'- {len(names)} repositories rewritten under their own folder: '
             f'{sum(counts.values())} commits, history and authorship kept, new commit hashes.',
             f'- {len(created)} combined branches; each is one commit whose parents are the repositories\' '
             'branches, so `git log -- <folder>` shows that repository\'s full history.',
             f"- Default branch: `{default}` (checked out).",
             '- Not migrated: uncommitted changes, stashes, reflogs, and the remotes\' pull requests, reviews and '
             'build history (they are not part of git).']
    c.write_text(os.path.join(work, 'migration.md'), '\n'.join(lines) + '\n')
    c.log(f"Done in {state['seconds']}s: {output}")


if __name__ == '__main__':
    main()
