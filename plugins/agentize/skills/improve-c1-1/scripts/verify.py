#!/usr/bin/env python3
# Copyright (c) 2026 Codomain D.O.O. All rights reserved.
# Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
# See LICENSE.md for details.
"""Phase 4 — Verification: check the monorepo against the untouched snapshots of the sources.

Usage:
    python verify.py --work <dir>

Checks (each PASS or FAIL; the script exits 1 if any fails):

1. Branches      every planned branch exists, the pruned ones are gone, tips unchanged since migration.
2. Structure     for every branch and every repository, the <repo>/ folder has exactly the source branch's
                 tree, and the branch's parents are the rewritten source commits.
3. Content       for the recent branches of every repository (production, develop, and the branches used
                 in the last 90 days, at least five per repository): every file's bytes, mode and name
                 compared with the source, read from both object stores. A pair of folders that was
                 already compared (unchanged between branches) is not compared again.
4. History       for the same branches: the same number of commits, with the same authors, committers,
                 dates, parents and subjects (hashes quoted in subjects are ignored, as they were rewritten).
5. Commits       every source commit is reachable in the monorepo (the counts add up).
6. Tags          every source tag is in the monorepo and its folder matches the tagged source tree.
7. Working tree  the default branch is checked out and `git status` is clean on this machine.
"""
import argparse
import os
import re
import time

import common as c

HASH = re.compile(r'\b[0-9a-f]{7,64}\b')


def parse_args():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--work', required=True)
    return ap.parse_args()


class Contents:
    """Compares source and monorepo trees file by file, never comparing the same pair of trees twice."""

    def __init__(self, out_cat, oid_len):
        self.out = out_cat
        self.oid_len = oid_len
        self.done_trees, self.done_blobs = set(), set()
        self.trees = self.reused = self.blobs = self.bytes = 0

    def tree(self, src_cat, src_oid, out_oid, path, problems):
        if (src_oid, out_oid) in self.done_trees:
            self.reused += 1
            return
        before = len(problems)
        src, out = src_cat.read(src_oid), self.out.read(out_oid)
        if not src or not out or src[1] != 'tree' or out[1] != 'tree':
            problems.append(f'{path}/: folder missing or not a folder')
            return
        self.trees += 1
        se = {name: (mode, oid) for mode, name, oid in c.parse_tree(src[2], self.oid_len)}
        oe = {name: (mode, oid) for mode, name, oid in c.parse_tree(out[2], self.oid_len)}
        for name in sorted(set(se) ^ set(oe)):
            side = 'missing in the monorepo' if name in se else 'not in the source'
            problems.append(f"{path}/{name.decode('utf-8', 'replace')}: {side}")
        for name in sorted(set(se) & set(oe)):
            (smode, soid), (omode, ooid) = se[name], oe[name]
            sub = f"{path}/{name.decode('utf-8', 'replace')}"
            if smode != omode:
                problems.append(f'{sub}: mode {smode.decode()} became {omode.decode()}')
            elif smode == b'40000':
                self.tree(src_cat, soid, ooid, sub, problems)
            elif smode == b'160000':
                if soid != ooid:
                    problems.append(f'{sub}: submodule commit differs')
            else:
                self.blob(src_cat, soid, ooid, sub, problems)
        if len(problems) == before:
            self.done_trees.add((src_oid, out_oid))

    def blob(self, src_cat, soid, ooid, path, problems):
        if (soid, ooid) in self.done_blobs:
            return
        src, out = src_cat.read(soid), self.out.read(ooid)
        if not src or not out:
            problems.append(f'{path}: file missing')
        elif src[2] != out[2]:
            problems.append(f'{path}: content differs')
        else:
            self.blobs += 1
            self.bytes += len(src[2])
            self.done_blobs.add((soid, ooid))


def history(repo, commits):
    """One normalised line per commit reachable from `commits`, in git's log order."""
    fmt = '%P%x1f%an%x1f%ae%x1f%at%x1f%cn%x1f%ce%x1f%ct%x1f%s'
    out = c.git(['log', '--topo-order', f'--format={fmt}', '--stdin'], cwd=repo, input='\n'.join(commits) + '\n')
    lines = []
    for line in out.splitlines():
        parents, rest = line.split('\x1f', 1)
        lines.append(f'{len(parents.split())}\x1f' + HASH.sub('<hash>', rest))
    return lines


def main():
    c.set_prefix('verify')
    args = parse_args()
    work = os.path.abspath(args.work)
    plan = c.load_json(os.path.join(work, 'analysis.json'))
    mig = c.load_json(os.path.join(work, 'migration.json'))
    cln = c.load_json(os.path.join(work, 'cleanup.json'))
    output, names = mig['output'], mig['repos']
    repos = {r['name']: r for r in plan['repos']}
    started = time.time()
    results = []

    def check(title, problems, detail, seconds):
        ok = not problems
        results.append({'check': title, 'ok': ok, 'detail': detail, 'problems': problems[:25],
                        'problem_count': len(problems), 'seconds': round(seconds, 1)})
        c.log(f"{'PASS' if ok else 'FAIL'}  {title}: {detail}" + ('' if ok else f' ({len(problems)} problem(s))'))
        for p in problems[:5]:
            c.log(f'        {p}')

    oid_len = 32 if c.git(['rev-parse', '--show-object-format'], cwd=output).strip() == 'sha256' else 20
    out = c.git(['for-each-ref', '--format=%(refname)%00%(objectname)%00%(*objectname)', 'refs/heads', 'refs/tags'],
                cwd=output)
    heads, tags = {}, {}
    for line in out.splitlines():
        ref, oid, peeled = line.split('\0')
        if ref.startswith('refs/heads/'):
            heads[ref[len('refs/heads/'):]] = oid
        else:
            tags[ref[len('refs/tags/'):]] = peeled or oid
    maps = {name: c.load_commit_map(work, name) for name in names}
    snaps = {name: c.CatFile(os.path.join(work, 'snapshot', name + '.git')) for name in names}
    out_cat = c.CatFile(output)
    source_commit = {(r['name'], b['target']): b['commit'] for r in plan['repos'] for b in r['branches']}

    src_trees, out_trees = {}, {}

    def source_tree(name, commit):
        if (name, commit) not in src_trees:
            found = snaps[name].oid(f'{commit}^{{tree}}')
            src_trees[(name, commit)] = found[0] if found else None
        return src_trees[(name, commit)]

    def folder(commit, name):
        if (commit, name) not in out_trees:
            found = out_cat.oid(f'{commit}:{name}')
            out_trees[(commit, name)] = found[0] if found else None
        return out_trees[(commit, name)]

    empty_tree = c.git(['hash-object', '-t', 'tree', '--stdin'], cwd=output, input='').strip()

    def empty_or(tree):
        """A source commit with no files has no folder in the monorepo."""
        return 'empty' if not tree or tree == empty_tree else tree

    # 1. Branches
    t = time.time()
    planned = {b['name'] for b in plan['combined']['branches'] if not b['prune']}
    pruned = {p['name'] for p in cln['pruned']}
    problems = [f'missing branch {b}' for b in sorted(planned - set(heads))]
    problems += [f'unexpected branch {b}' for b in sorted(set(heads) - planned)]
    problems += [f'{b}: tip changed since migration' for b in sorted(planned & set(heads))
                 if heads[b] != mig['branches'][b]['tip']]
    check('Branches', problems, f'{len(planned)} branches present, {len(pruned)} pruned', time.time() - t)

    # 2. Structure
    t = time.time()
    problems, pairs = [], 0
    remaining = sorted(planned & set(heads))
    out = c.git(['rev-list', '--no-walk', '--parents', '--stdin'], cwd=output,
                input='\n'.join(heads[b] for b in remaining) + '\n')
    parents = {line.split()[0]: line.split()[1:] for line in out.splitlines()}
    by_name = {b['name']: b for b in plan['combined']['branches']}
    for b in remaining:
        tip = heads[b]
        expected_parents = []
        for name in names:
            target = by_name[b]['composition'][name]
            src = source_commit[(name, target)]
            expected_parents.append(maps[name].get(src))
            pairs += 1
            if empty_or(folder(tip, name)) != empty_or(source_tree(name, src)):
                problems.append(f"{b}: {name}/ differs from {name}'s '{target}'")
        if parents.get(tip) != expected_parents:
            problems.append(f'{b}: parents are not the rewritten source branches')
    check('Structure', problems, f'{pairs} repository folders in {len(remaining)} branches match their source tree',
          time.time() - t)

    # 3. Content and 4. History of the recent branches
    t = time.time()
    contents = Contents(out_cat, oid_len)
    problems, selected = [], []
    for name in names:
        for target in repos[name]['recent']:
            if target in heads:
                selected.append((name, target))
    for name, target in selected:
        src = source_commit[(name, target)]
        src_tree, out_tree = source_tree(name, src), folder(heads[target], name)
        if empty_or(src_tree) == 'empty' or not out_tree:
            if empty_or(src_tree) != empty_or(out_tree):
                problems.append(f'{target}:{name}/ is missing')
            continue
        found = []
        contents.tree(snaps[name], src_tree, out_tree, f'{target}:{name}', found)
        problems += found
    check('Content', problems,
          f'{len(selected)} recent repository branches: {contents.blobs} files ({contents.bytes / 2**20:.0f} MiB) and '
          f'{contents.trees} folders compared; {contents.reused} unchanged folders reused', time.time() - t)

    t = time.time()
    problems, commits_checked = [], 0
    for name in names:
        sources = sorted({source_commit[(n, tg)] for n, tg in selected if n == name})
        if not sources:
            continue
        before = history(os.path.join(work, 'snapshot', name + '.git'), sources)
        after = history(output, [maps[name][s] for s in sources])
        commits_checked += len(before)
        if before != after:
            first = next((i for i, (x, y) in enumerate(zip(before, after)) if x != y), min(len(before), len(after)))
            problems.append(f'{name}: history differs ({len(before)} source commits, {len(after)} migrated; '
                            f'first difference at commit #{first + 1})')
    check('History', problems, f'{commits_checked} commits of the recent branches have the same metadata',
          time.time() - t)

    # 5. Commits
    t = time.time()
    expected = sum(repos[n]['commits'] for n in names) + len(remaining) + len(cln['combined_tags'])
    actual = int(c.git(['rev-list', '--count', '--branches', '--tags'], cwd=output).strip())
    rewritten = sum(mig['rewritten_commits'].values())
    problems = []
    if actual != expected:
        problems.append(f'expected {expected} commits, found {actual}')
    if rewritten != sum(repos[n]['commits'] for n in names):
        problems.append(f"filter-repo rewrote {rewritten} commits, the sources have "
                        f"{sum(repos[n]['commits'] for n in names)}")
    check('Commits', problems, f"{sum(repos[n]['commits'] for n in names)} source commits + {len(remaining)} combining "
          f"+ {len(cln['combined_tags'])} release-tag commits = {actual}", time.time() - t)

    # 6. Tags
    t = time.time()
    problems, checked = [], 0
    for tag in plan['combined']['tags']['combined']:
        commit = tags.get(tag['final'])
        if not commit:
            problems.append(f"missing tag {tag['final']}")
            continue
        for name in names:
            src = (tag['members'].get(name) or tag['fill'].get(name) or {}).get('commit')
            checked += 1
            if src and empty_or(folder(commit, name)) != empty_or(source_tree(name, src)):
                problems.append(f"{tag['final']}: {name}/ differs from the source")
            if not src and folder(commit, name):
                problems.append(f"{tag['final']}: {name}/ should not be there")
    for tag in plan['combined']['tags']['per_repo']:
        commit = tags.get(tag['final'])
        checked += 1
        src = repos[tag['repo']]['tags'][tag['tag_index']]['commit']
        if not commit:
            problems.append(f"missing tag {tag['final']}")
        elif empty_or(folder(commit, tag['repo'])) != empty_or(source_tree(tag['repo'], src)):
            problems.append(f"{tag['final']}: differs from the source tag")
    total_src = sum(len(r['tags']) for r in plan['repos'])
    check('Tags', problems, f'all {total_src} source tags covered ({len(tags)} tags in the monorepo, '
          f'{checked} folders compared)', time.time() - t)

    # 7. Working tree
    t = time.time()
    problems = []
    head = c.git_ok(['symbolic-ref', '--short', 'HEAD'], cwd=output)[1].strip()
    if head != mig['default_branch']:
        problems.append(f"HEAD is '{head}', expected '{mig['default_branch']}'")
    status = c.git(['status', '--porcelain'], cwd=output).splitlines()
    problems += [f'git status: {line}' for line in status]
    check('Working tree', problems, f"'{mig['default_branch']}' checked out, git status clean", time.time() - t)

    for cat in list(snaps.values()) + [out_cat]:
        cat.close()
    failed = [r for r in results if not r['ok']]
    state = {'created': c.now_iso(), 'ok': not failed, 'checks': results, 'seconds': round(time.time() - started)}
    c.save_json(os.path.join(work, 'verification.json'), state)
    lines = ['# Verification', '',
             f"**{'All checks passed' if not failed else f'{len(failed)} check(s) failed'}** "
             f"({state['seconds']} s). Compared against the untouched snapshots of the sources.", '',
             '| Check | Result | Detail | Time (s) |', '|---|---|---|---:|']
    lines += [f"| {r['check']} | {'PASS' if r['ok'] else 'FAIL'} | {r['detail']} | {r['seconds']} |" for r in results]
    for r in failed:
        lines += ['', f"## {r['check']}: {r['problem_count']} problem(s)", '']
        lines += [f'- {p}' for p in r['problems']]
    c.write_text(os.path.join(work, 'verification.md'), '\n'.join(lines) + '\n')
    c.log(f"{'All checks passed' if not failed else f'{len(failed)} check(s) failed'} in {state['seconds']}s")
    if failed:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
