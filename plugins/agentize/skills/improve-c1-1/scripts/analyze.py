#!/usr/bin/env python3
# Copyright (c) 2026 Codomain D.O.O. All rights reserved.
# Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
# See LICENSE.md for details.
"""Phase 1 — Analysis: snapshot the source repositories and plan the migration.

Usage:
    python analyze.py --work <dir> --workspace <folder with the clones>
    python analyze.py --work <dir> --repo <name>=<path-or-url> [--repo ...]

Every source is copied into <work>/snapshot/<name>.git: its local branches and tags, and its remote's
branches and tags, fetched fresh (the source checkouts are never changed). The analysis then takes every
decision the later phases execute, and writes them to <work>/analysis.json and <work>/analysis.md:

- which branch to migrate when the local and the remote branch differ (behind, ahead, diverged), and which
  local branches to leave out because they hold no commits that are not on the remote
- one spelling for branch names that differ only in letter case, and new names for branches that clash
  with a folder of another branch (`a` and `a/b`)
- the content of each combined branch: which branch every repository contributes (git-flow fallback)
- which branches cleanup removes (merged into develop/master and inactive)
- how the tags are combined into release tags
- what needs attention after the migration (submodules, LFS, CI files, long paths, local changes, ...)
"""
import argparse
import os
import re
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor

import common as c

NAME_RE = re.compile(r'^[A-Za-z0-9_][A-Za-z0-9_.-]*$')
WINDOWS_RESERVED = re.compile(r'^(con|prn|aux|nul|com[1-9]|lpt[1-9])(\..*)?$', re.I)
WINDOWS_BAD_CHARS = re.compile(r'[<>:"|?*\\]')
CI_FILE = re.compile(r'^(azure-pipelines[^/]*\.ya?ml|\.azure-pipelines/.*|\.azuredevops/.*|\.github/workflows/.*'
                     r'|\.gitlab-ci\.yml|Jenkinsfile[^/]*|bitbucket-pipelines\.yml|\.circleci/.*)$'
                     r'|(^|/)[^/]*pipelines?[^/]*\.ya?ml$', re.I)
HOOK_FILE = re.compile(r'^(\.husky/|\.githooks/|\.pre-commit-config\.yaml$|lefthook\.ya?ml$)', re.I)
VERSION_TAG = re.compile(r'^(?:v|version[-_]?|release[-_/]?|rel[-_]?)?(\d+(?:\.\d+)*(?:[-+._].*)?)$', re.I)


def parse_args():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--work', required=True, help='work directory for the migration state')
    ap.add_argument('--repo', action='append', default=[], metavar='NAME=SOURCE',
                    help='a source repository (local path or URL); NAME becomes its folder')
    ap.add_argument('--workspace', help='merge every git repository found directly inside this folder')
    ap.add_argument('--no-fetch', action='store_true',
                    help="don't contact the remotes; use the sources' remote-tracking branches as they are")
    ap.add_argument('--jobs', type=int, default=4, help='repositories processed in parallel')
    return ap.parse_args()


def source_specs(args):
    specs = []
    if args.workspace:
        for entry in sorted(os.listdir(args.workspace)):
            path = os.path.join(args.workspace, entry)
            if os.path.isdir(path) and os.path.exists(os.path.join(path, '.git')):
                specs.append((entry, os.path.abspath(path)))
    for spec in args.repo:
        if '=' not in spec:
            c.die(f"Invalid --repo '{spec}'. Expected NAME=SOURCE.")
        name, src = spec.split('=', 1)
        src = os.path.abspath(src) if os.path.isdir(src) else src
        specs = [s for s in specs if s[0] != name] + [(name, src)]
    if not specs:
        c.die('No source repositories. Pass --workspace or --repo.')
    seen = {}
    for name, _ in specs:
        if not NAME_RE.match(name):
            c.die(f"Folder name '{name}' may only contain A-Z a-z 0-9 _ . - and not start with '.' or '-'.")
        if name.lower() in seen:
            c.die(f"Folder names '{seen[name.lower()]}' and '{name}' differ only in letter case.")
        seen[name.lower()] = name
    return sorted(specs, key=lambda s: s[0].lower())


# ---------------------------------------------------------------------------
# Snapshot
# ---------------------------------------------------------------------------

def snapshot(name, src, work, fetch, ref_format):
    """Copies one source into <work>/snapshot/<name>.git and records its state."""
    snap = os.path.join(work, 'snapshot', name + '.git')
    if not os.path.isdir(snap):
        c.git(['init', '--bare', '-q'] + ref_format + [snap])
    info = {'name': name, 'source': src, 'warnings': [], 'local': None}
    is_local = os.path.isdir(src) and c.git_ok(['rev-parse', '--git-dir'], cwd=src)[0] == 0
    info['kind'] = 'local' if is_local else 'url'
    origin = src
    if is_local:
        rc, out, _ = c.git_ok(['remote', 'get-url', 'origin'], cwd=src)
        origin = out.strip() if rc == 0 else None
        c.git(['fetch', '-q', '--prune', '--no-tags', src,
               '+refs/heads/*:refs/local/*', '+refs/tags/*:refs/local-tags/*'], cwd=snap)
    info['origin_url'] = origin

    status = 'none'
    if origin and (fetch or not is_local):
        rc, _, err = c.git_ok(['fetch', '-q', '--prune', '--no-tags', origin,
                               '+refs/heads/*:refs/remote/*', '+refs/tags/*:refs/remote-tags/*'], cwd=snap)
        if rc == 0:
            status = 'fetched'
        elif not is_local:
            raise c.GitError(f'cannot fetch {origin}: {err.strip()}')
        else:
            info['warnings'].append(f'Could not fetch {origin} ({err.strip().splitlines()[-1] if err.strip() else rc}); '
                                    'used the remote-tracking branches of the local clone, which may be out of date.')
    if status == 'none' and is_local and origin:
        c.git(['fetch', '-q', '--prune', '--no-tags', src, '+refs/remotes/origin/*:refs/remote/*'], cwd=snap)
        c.git_ok(['update-ref', '-d', 'refs/remote/HEAD'], cwd=snap)
        status = 'stale'
    info['remote_status'] = status

    default, default_from = None, None
    if status == 'fetched':
        out = c.git(['ls-remote', '--symref', origin, 'HEAD'], cwd=snap)
        m = re.search(r'^ref: refs/heads/(\S+)\tHEAD', out, re.M)
        if m:
            default, default_from = m.group(1), "remote's default branch"
    if not default and is_local and origin:
        rc, out, _ = c.git_ok(['symbolic-ref', '-q', '--short', 'refs/remotes/origin/HEAD'], cwd=src)
        if rc == 0 and out.strip().startswith('origin/'):
            default, default_from = out.strip()[len('origin/'):], 'origin/HEAD of the local clone'
    if not default and is_local:
        rc, out, _ = c.git_ok(['symbolic-ref', '-q', '--short', 'HEAD'], cwd=src)
        if rc == 0:
            default, default_from = out.strip(), 'checked-out branch (no remote default known)'
    info['default'], info['default_from'] = default, default_from

    if is_local:
        bare = c.git(['rev-parse', '--is-bare-repository'], cwd=src).strip() == 'true'
        local = {'changed': 0, 'untracked': 0, 'stashes': 0, 'worktrees': 0, 'upstreams': {}}
        if not bare:
            status_lines = c.git(['status', '--porcelain'], cwd=src).splitlines()
            local['changed'] = sum(1 for line in status_lines if not line.startswith('??'))
            local['untracked'] = sum(1 for line in status_lines if line.startswith('??'))
        local['stashes'] = len(c.git_ok(['stash', 'list'], cwd=src)[1].splitlines())
        local['worktrees'] = max(0, c.git(['worktree', 'list', '--porcelain'], cwd=src).count('worktree ') - 1)
        local['shallow'] = c.git(['rev-parse', '--is-shallow-repository'], cwd=src).strip() == 'true'
        out = c.git(['for-each-ref', '--format=%(refname:short)%00%(upstream)', 'refs/heads'], cwd=src)
        for line in out.splitlines():
            branch, upstream = line.split('\0')
            if upstream.startswith('refs/remotes/origin/'):
                local['upstreams'][branch] = upstream[len('refs/remotes/origin/'):]
        info['local'] = local
    return info


# ---------------------------------------------------------------------------
# Per-repository analysis
# ---------------------------------------------------------------------------

REF_FORMAT = ('%(refname)%00%(objectname)%00%(objecttype)%00%(*objectname)%00%(*objecttype)'
              '%00%(creatordate:unix)%00%(committerdate:unix)%00%(*committerdate:unix)%00%(contents:subject)')


def read_refs(snap, info):
    refs = {'local': {}, 'remote': {}, 'local-tags': {}, 'remote-tags': {}}
    out = c.git(['for-each-ref', '--format=' + REF_FORMAT,
                 'refs/local', 'refs/remote', 'refs/local-tags', 'refs/remote-tags'], cwd=snap)
    for line in out.splitlines():
        ref, oid, typ, peeled, peeled_type, created, cdate, peeled_cdate, subject = line.split('\0')
        space = ref.split('/')[1]
        short = ref[len('refs/') + len(space) + 1:]
        if space in ('local', 'remote'):
            refs[space][short] = {'ref': ref, 'commit': oid, 'date': int(cdate or 0)}
            continue
        if typ == 'tag':
            commit = peeled if peeled_type == 'commit' else c.git_ok(['rev-parse', '-q', '--verify', ref + '^{commit}'],
                                                                      cwd=snap)[1].strip()
            date = int(created or peeled_cdate or 0)
        else:
            commit, date = (oid, int(cdate or 0)) if typ == 'commit' else (None, 0)
        if not commit:
            info['warnings'].append(f"Tag '{short}' does not point to a commit; it is not migrated.")
            continue
        refs[space][short] = {'ref': ref, 'commit': commit, 'date': date, 'annotated': typ == 'tag',
                              'subject': subject if typ == 'tag' else ''}
    return refs


def count(snap, args):
    return int(c.git(['rev-list', '--count'] + args, cwd=snap).strip())


def plan_branches(snap, info, refs):
    """Chooses, per branch name, the local or the remote branch, and drops branches with nothing to add."""
    remote, local = refs['remote'], refs['local']
    upstreams = (info['local'] or {}).get('upstreams', {})
    has_remote = info['remote_status'] != 'none'
    plan, dropped = [], []

    def add(branch, src, origin, note='', name=None):
        plan.append({'source_branch': branch, 'name': name or branch, 'ref': src['ref'], 'commit': src['commit'],
                     'date': src['date'], 'origin': origin, 'note': note})

    for b in sorted(set(remote) | set(local), key=str.lower):
        r, l = remote.get(b), local.get(b)
        if r and not l:
            add(b, r, 'remote')
        elif l and not r:
            if not has_remote:
                add(b, l, 'local', 'repository has no remote')
                continue
            unique = count(snap, [l['commit'], '--not', '--glob=refs/remote/*', '--glob=refs/remote-tags/*'])
            if unique:
                add(b, l, 'local', f'local only: {unique} commit(s) not on the remote')
            else:
                upstream = upstreams.get(b)
                why = (f"its remote branch '{upstream}' was deleted" if upstream and upstream not in remote
                       else f"it tracks '{upstream}'" if upstream else 'it was never pushed')
                dropped.append({'branch': b, 'commit': l['commit'], 'date': l['date'],
                                'reason': f'local branch with no commits of its own ({why})'})
        elif r['commit'] == l['commit']:
            add(b, r, 'remote')
        else:
            behind, ahead = (int(x) for x in c.git(['rev-list', '--left-right', '--count',
                                                     f"{r['commit']}...{l['commit']}"], cwd=snap).split())
            if not ahead:
                add(b, r, 'remote', f'local branch was {behind} commit(s) behind; used the remote')
            elif not behind:
                add(b, l, 'local', f'local branch has {ahead} unpushed commit(s); used the local one')
            else:
                add(b, r, 'remote', f"local branch diverged ({ahead} ahead, {behind} behind); kept as 'local/{b}'")
                add(b, l, 'local', f'diverged local branch ({ahead} unpushed commit(s))', name=f'local/{b}')
    return plan, dropped


def plan_tags(info, refs):
    tags = []
    for name, t in sorted(refs['remote-tags'].items()):
        tags.append(dict(t, name=name, origin='remote'))
        lt = refs['local-tags'].get(name)
        if lt and lt['commit'] != t['commit']:
            info['warnings'].append(f"Local tag '{name}' differs from the remote tag of the same name; "
                                    'the remote one is migrated.')
    for name, t in sorted(refs['local-tags'].items()):
        if name not in refs['remote-tags']:
            tags.append(dict(t, name=name, origin='local' if info['remote_status'] != 'none' else 'remote'))
    return tags


def tree_checks(snap, cat, name, ref):
    """Looks at the default branch for things that behave differently inside a subfolder."""
    checks = {'max_path': 0, 'long_paths': [], 'invalid_names': [], 'case_paths': [], 'submodules': False,
              'gitlinks': 0, 'lfs': False, 'ci': [], 'hooks': [], 'files': 0}
    if not ref:
        return checks
    out = c.git(['ls-tree', '-r', '-z', '--full-tree', ref], cwd=snap)
    lowered = Counter()
    for entry in out.split('\0'):
        if not entry:
            continue
        meta, path = entry.split('\t', 1)
        mode, _, oid = meta.split(' ')
        checks['files'] += 1
        full = len(name) + 1 + len(path)
        checks['max_path'] = max(checks['max_path'], full)
        if full > c.LONG_PATH and len(checks['long_paths']) < 5:
            checks['long_paths'].append(path)
        if any(WINDOWS_RESERVED.match(p) or WINDOWS_BAD_CHARS.search(p) or p.endswith(('.', ' '))
               for p in path.split('/')) and len(checks['invalid_names']) < 5:
            checks['invalid_names'].append(path)
        lowered[path.lower()] += 1
        if mode == '160000':
            checks['gitlinks'] += 1
        if path == '.gitmodules':
            checks['submodules'] = True
        if path.endswith('.gitattributes'):
            blob = cat.read(oid)
            if blob and b'filter=lfs' in blob[2]:
                checks['lfs'] = True
        if CI_FILE.search(path) and len(checks['ci']) < 10:
            checks['ci'].append(path)
        if HOOK_FILE.match(path) and path.split('/')[0] not in [h.split('/')[0] for h in checks['hooks']]:
            checks['hooks'].append(path)
    checks['case_paths'] = [p for p, n in lowered.items() if n > 1][:5]
    return checks


def analyze_repo(info, work):
    name = info['name']
    snap = os.path.join(work, 'snapshot', name + '.git')
    refs = read_refs(snap, info)
    info['branches'], info['dropped'] = plan_branches(snap, info, refs)
    info['tags'] = plan_tags(info, refs)
    if not info['branches']:
        info['warnings'].append('The repository has no branches; it is left out.')
        return info
    sources = {b['source_branch'] for b in info['branches'] if not b['name'].startswith('local/')}
    if info['default'] not in sources:
        fallback = next((p for p in c.PRODUCTION_BRANCHES if p in sources), sorted(sources)[0])
        if info['default']:
            info['warnings'].append(f"Default branch '{info['default']}' does not exist; using '{fallback}'.")
        info['default'], info['default_from'] = fallback, 'guessed'
    info['production_source'] = next((p for p in c.PRODUCTION_BRANCHES if p in sources), info['default'])
    info['develop_source'] = c.DEVELOP_BRANCH if c.DEVELOP_BRANCH in sources else None

    prefixes = Counter(b['source_branch'].split('/')[0] + '/' if '/' in b['source_branch'] else '(no prefix)'
                       for b in info['branches'])
    info['prefixes'] = dict(prefixes.most_common())
    if info['develop_source']:
        info['strategy'] = 'git-flow' + (' with release branches' if prefixes.get('release/') else '')
    else:
        info['strategy'] = 'single main line (trunk-based)'

    size = c.git(['count-objects', '-v'], cwd=snap)
    info['size_kib'] = sum(int(v) for k, v in (line.split(': ') for line in size.splitlines())
                           if k in ('size', 'size-pack'))
    commits ='\n'.join({b['commit'] for b in info['branches']} | {t['commit'] for t in info['tags']}) + '\n'
    info['commits'] = int(c.git(['rev-list', '--count', '--stdin'], cwd=snap, input=commits).strip())
    info['roots'] = sorted(set(c.git(['rev-list', '--max-parents=0', '--stdin'], cwd=snap, input=commits).split()))
    info['shallow_snapshot'] = c.git(['rev-parse', '--is-shallow-repository'], cwd=snap).strip() == 'true'

    default_ref = next(b['ref'] for b in info['branches'] if b['source_branch'] == info['default'])
    cat = c.CatFile(snap)
    try:
        info['checks'] = tree_checks(snap, cat, name, default_ref)
    finally:
        cat.close()

    # Branches already merged into production or develop (candidates for removal in cleanup).
    info['merged'] = set()
    for base in filter(None, [info['production_source'], info['develop_source']]):
        base_ref = next(b['ref'] for b in info['branches']
                        if b['source_branch'] == base and not b['name'].startswith('local/'))
        out = c.git(['for-each-ref', f'--merged={base_ref}', '--format=%(refname)', 'refs/remote', 'refs/local'],
                    cwd=snap)
        info['merged'].update(out.split())
    return info


# ---------------------------------------------------------------------------
# Cross-repository decisions
# ---------------------------------------------------------------------------

def combine(repos):
    renames = []
    weights = Counter()
    for r in repos:
        for name in {b['name'] for b in r['branches']}:
            weights[name] += 1

    # One spelling per case-insensitive name, folder by folder.
    spelling = c.canonical_case(weights)
    for r in repos:
        for b in r['branches']:
            b['target'] = spelling[b['name']]
            if b['target'] != b['name']:
                renames.append({'repo': r['name'], 'from': b['name'], 'to': b['target'],
                                'reason': 'same branch as in other repositories, spelled with different letter case'})
        # Two branches of one repository that differ only in case (possible on a case-sensitive server).
        groups = defaultdict(list)
        for b in r['branches']:
            groups[b['target'].lower()].append(b)
        for same in groups.values():
            for k, b in enumerate(sorted(same, key=lambda x: -x['date'])[1:], start=2):
                old, b['target'] = b['target'], f"{b['target']}-{k}"
                renames.append({'repo': r['name'], 'from': b['name'], 'to': b['target'],
                                'reason': f"another branch of this repository differs from '{old}' only in letter case"})

    # One production branch: a repository on `main` joins the others' `master` (or the other way round).
    production = Counter(spelling[r['production_source']] for r in repos)
    production_name = sorted(production.items(), key=lambda kv: (-kv[1], kv[0] not in c.PRODUCTION_BRANCHES, kv[0]))[0][0]
    if production_name.lower() in c.PRODUCTION_BRANCHES:
        for r in repos:
            if production_name in {b['target'] for b in r['branches']}:
                continue
            for b in r['branches']:
                if b['source_branch'] == r['production_source'] and not b['name'].startswith('local/'):
                    renames.append({'repo': r['name'], 'from': b['name'], 'to': production_name,
                                    'reason': f"production branch, joined with the other repositories' "
                                              f"'{production_name}'"})
                    b['target'] = production_name

    # A branch cannot also be a folder of another branch.
    clashes = c.resolve_dir_file({b['target'] for r in repos for b in r['branches']}, '-branch')
    for r in repos:
        for b in r['branches']:
            if b['target'] in clashes:
                renames.append({'repo': r['name'], 'from': b['name'], 'to': clashes[b['target']],
                                'reason': f"'{b['target']}' is also a folder of other branch names"})
                b['target'] = clashes[b['target']]

    for r in repos:
        by_source = {b['source_branch']: b['target'] for b in r['branches'] if not b['name'].startswith('local/')}
        r['targets'] = sorted(b['target'] for b in r['branches'])
        r['default_target'] = by_source[r['default']]
        r['production'] = by_source[r['production_source']]
        r['develop'] = by_source.get(r['develop_source']) if r['develop_source'] else None
        keep = {r['production'], r['develop'], r['default_target']} - {None}
        dated = sorted(r['branches'], key=lambda b: -b['date'])
        r['recent_cutoff'] = dated[0]['date'] - c.RECENT_DAYS * 86400
        r['recent'] = sorted({b['target'] for b in dated if b['date'] >= r['recent_cutoff']}
                             | {b['target'] for b in dated[:c.MIN_RECENT_BRANCHES]} | keep)

    defaults = Counter(r['default_target'] for r in repos)
    default_branch = sorted(defaults.items(), key=lambda kv: (-kv[1], kv[0] not in c.PRODUCTION_BRANCHES, kv[0]))[0][0]

    owners = defaultdict(dict)
    for r in repos:
        for b in r['branches']:
            owners[b['target']][r['name']] = b
    protected_names = {default_branch} | {r['default_target'] for r in repos}
    by_repo = {r['name']: r for r in repos}
    branches = []
    for name in sorted(owners, key=str.lower):
        composition = {r['name']: c.fallback_branch(r, name) for r in repos}
        protected = (name in protected_names or name.lower() in c.PRODUCTION_BRANCHES + (c.DEVELOP_BRANCH,)
                     or bool(c.LONG_LIVED.match(name)))
        # Removed in cleanup when every repository that has it merged it and stopped using it.
        prune, why = False, ''
        if not protected:
            own = owners[name]
            prune = all(b['origin'] == 'remote' and b['ref'] in by_repo[rn]['merged']
                        and name not in by_repo[rn]['recent'] for rn, b in own.items())
            if prune:
                last = max(b['date'] for b in own.values())
                why = f'merged into develop or the production branch; inactive since {c.day(last)}'
        branches.append({'name': name, 'owners': sorted(owners[name]), 'composition': composition,
                         'protected': protected, 'prune': prune, 'prune_reason': why})
    return default_branch, branches, renames


def tag_key(name):
    m = VERSION_TAG.match(name.strip())
    return (m.group(1) if m else name).lower()


def plan_combined_tags(repos, work):
    groups = defaultdict(lambda: defaultdict(list))
    for r in repos:
        for i, t in enumerate(r['tags']):
            groups[tag_key(t['name'])][r['name']].append((i, t))
    combined, per_repo = [], []
    for key in sorted(groups):
        by_repo = groups[key]
        if len(by_repo) < 2:
            for repo, tags in by_repo.items():
                for i, t in tags:
                    per_repo.append({'repo': repo, 'tag_index': i, 'name': t['name'], 'final': f"{repo}/{t['name']}",
                                     'reason': 'only this repository has this tag'})
            continue
        spellings = Counter(t['name'] for tags in by_repo.values() for _, t in tags)
        name = sorted(spellings.items(), key=lambda kv: (-kv[1], len(kv[0]), kv[0]))[0][0]
        members = {}
        for repo, tags in by_repo.items():
            ordered = sorted(tags, key=lambda it: (it[1]['name'] != name, -it[1]['date']))
            i, t = ordered[0]
            members[repo] = {'tag_index': i, 'name': t['name'], 'commit': t['commit'], 'date': t['date'],
                             'annotated': t['annotated'], 'subject': t.get('subject', '')}
            for j, extra in ordered[1:]:
                per_repo.append({'repo': repo, 'tag_index': j, 'name': extra['name'],
                                 'final': f"{repo}/{extra['name']}",
                                 'reason': f"the repository also has '{t['name']}' for the same release"})
        date = max(m['date'] for m in members.values())
        fill = {}
        for r in repos:
            if r['name'] in members or not r['branches']:
                continue
            ref = next(b['ref'] for b in r['branches'] if b['target'] == r['production'])
            snap = os.path.join(work, 'snapshot', r['name'] + '.git')
            commit = c.git(['rev-list', '-1', '--first-parent', f'--before=@{date}', ref], cwd=snap).strip()
            if commit:
                fill[r['name']] = {'branch': r['production'], 'commit': commit}
        combined.append({'name': name, 'final': name, 'key': key, 'date': date, 'members': members, 'fill': fill,
                         'variants': sorted(set(spellings) - {name})})
    # Final names must not clash with each other or be a folder of another tag.
    finals = [t['final'] for t in combined] + [t['final'] for t in per_repo]
    clashes = c.resolve_dir_file(finals, '-tag')
    for t in combined + per_repo:
        t['final'] = clashes.get(t['final'], t['final'])
    lowered = Counter(t['final'].lower() for t in combined + per_repo)
    for t in per_repo:
        k = 2
        while lowered[t['final'].lower()] > 1:
            lowered[t['final'].lower()] -= 1
            t['final'] = f"{t['final']}-{k}"
            lowered[t['final'].lower()] += 1
            k += 1
    return combined, per_repo


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def collect_warnings(repos):
    out = []
    shared = defaultdict(list)
    for r in repos:
        for root in r.get('roots', []):
            shared[root].append(r['name'])
    for r in repos:
        w = [f"**{r['name']}**: {x}" for x in r['warnings']]
        loc = r['local']
        if loc:
            if loc['changed'] or loc['untracked']:
                w.append(f"**{r['name']}**: the local clone has {loc['changed']} uncommitted change(s) and "
                         f"{loc['untracked']} untracked file(s); they are not migrated.")
            if loc['stashes']:
                w.append(f"**{r['name']}**: {loc['stashes']} stash(es) in the local clone are not migrated.")
            if loc.get('shallow'):
                w.append(f"**{r['name']}**: the local clone is shallow.")
        if r.get('shallow_snapshot'):
            w.append(f"**{r['name']}**: the snapshot is shallow, so the full history cannot be migrated. "
                     'Fetch the full history (git fetch --unshallow) and run the analysis again.')
        if r['remote_status'] == 'stale':
            w.append(f"**{r['name']}**: remote branches are from the clone's last fetch, not fresh.")
        if r['default_from'] and 'checked-out' in r['default_from'] or r['default_from'] == 'guessed':
            w.append(f"**{r['name']}**: default branch '{r['default']}' was guessed ({r['default_from']}).")
        ch = r.get('checks') or {}
        if ch.get('submodules') or ch.get('gitlinks'):
            w.append(f"**{r['name']}**: uses git submodules ({ch.get('gitlinks', 0)} gitlink(s)). Git only reads "
                     '`.gitmodules` at the repository root, so they stop working under the subfolder.')
        if ch.get('lfs'):
            w.append(f"**{r['name']}**: uses Git LFS. The LFS objects must be copied separately "
                     '(`git lfs fetch --all` from the source, `git lfs push --all` to the new remote).')
        if ch.get('long_paths'):
            w.append(f"**{r['name']}**: paths up to {ch['max_path']} characters inside the monorepo, "
                     f"e.g. `{r['name']}/{ch['long_paths'][0]}`; on Windows this needs core.longpaths.")
        if ch.get('invalid_names'):
            w.append(f"**{r['name']}**: file names that cannot be checked out on Windows, e.g. "
                     f"`{ch['invalid_names'][0]}`.")
        if ch.get('case_paths'):
            w.append(f"**{r['name']}**: paths that differ only in letter case, e.g. `{ch['case_paths'][0]}`; "
                     'they clash on Windows and macOS checkouts.')
        out.extend(w)
    for root, names in shared.items():
        if len(names) > 1:
            out.append(f"{', '.join(names)} share history (same first commit {root[:10]}): forks or copies.")
    return out


def render(state):
    repos, comb = state['repos'], state['combined']
    lines = ['# Analysis', '', f"Snapshot taken {state['created']} of {len(repos)} repositories.", '',
             '## Repositories', '',
             '| Repository | Default branch | Strategy | Branches | Left out | Tags | Commits | Size (MiB) | Remote |',
             '|---|---|---|---:|---:|---:|---:|---:|---|']
    for r in repos:
        lines.append(f"| {r['name']} | {r['default']} | {r.get('strategy', '-')} | {len(r['branches'])} | "
                     f"{len(r['dropped'])} | {len(r['tags'])} | {r.get('commits', 0)} | "
                     f"{r.get('size_kib', 0) / 1024:.0f} | {r['remote_status']} |")
    br = comb['branches']
    prune = [b for b in br if b['prune']]
    lines += ['', '## Decisions', '',
              f"- Combined default branch: **{comb['default_branch']}** (the most common default branch).",
              f"- Combined branches: **{len(br)}**, of which **{len(prune)}** are merged and inactive and will be "
              'removed in cleanup.',
              f"- Combined release tags: **{len(comb['tags']['combined'])}**; tags kept under the repository name: "
              f"**{len(comb['tags']['per_repo'])}**.",
              f'- A branch is recent when its last commit is at most {c.RECENT_DAYS} days older than the newest '
              f'branch of its repository; the {c.MIN_RECENT_BRANCHES} newest branches always count as recent.',
              '- A repository without a combined branch contributes, git-flow style: its production branch '
              '(master/main) for master, main, hotfix/* and support/*; its develop branch (or its default branch '
              'without develop) for everything else.']
    notes = [(r['name'], b) for r in repos for b in r['branches'] if b['note']]
    if notes:
        lines += ['', '### Local and remote branches that differ', '', '| Repository | Branch | Decision |', '|---|---|---|']
        lines += [f"| {rn} | `{b['name']}` | {b['note']} |" for rn, b in notes]
    dropped = [(r['name'], d) for r in repos for d in r['dropped']]
    if dropped:
        lines += ['', '### Local branches left out', '', '| Repository | Branch | Last commit | Reason |', '|---|---|---|---|']
        lines += [f"| {rn} | `{d['branch']}` | {c.day(d['date'])} | {d['reason']} |" for rn, d in dropped]
    if comb['renames']:
        lines += ['', '### Renamed branches', '', '| Repository | Branch | New name | Reason |', '|---|---|---|---|']
        lines += [f"| {x['repo']} | `{x['from']}` | `{x['to']}` | {x['reason']} |" for x in comb['renames']]
    variants = [t for t in comb['tags']['combined'] if t['variants']]
    if variants:
        lines += ['', '### Tags spelled differently across repositories', '']
        lines += [f"- `{t['final']}` also combines {', '.join('`' + v + '`' for v in t['variants'])}" for t in variants]
    if comb['ambiguous']:
        lines += ['', '### Names used for both a branch and a tag', '',
                  ', '.join(f'`{n}`' for n in comb['ambiguous'][:20]) +
                  ' (git warns about ambiguous refs; use `refs/heads/...` or `refs/tags/...` to be explicit).']
    root_files = [(r['name'], r['checks']) for r in repos if r.get('checks') and (r['checks']['ci'] or r['checks']['hooks'])]
    if root_files:
        lines += ['', '### Files that assume they are at the repository root', '',
                  'They keep working only after the build/CI phase adapts them.', '',
                  '| Repository | CI pipeline files | Git hooks |', '|---|---|---|']
        lines += [f"| {rn} | {', '.join('`' + p + '`' for p in ch['ci'][:4]) or '-'} | "
                  f"{', '.join('`' + p + '`' for p in ch['hooks']) or '-'} |" for rn, ch in root_files]
    lines += ['', '## Needs attention', '']
    lines += [f'- {w}' for w in state['warnings']] or ['- Nothing.']
    return '\n'.join(lines) + '\n'


def main():
    c.set_prefix('analyze')
    args = parse_args()
    specs = source_specs(args)
    work = os.path.abspath(args.work)
    os.makedirs(os.path.join(work, 'snapshot'), exist_ok=True)
    if c.git_version() < (2, 29):
        c.die('git 2.29 or newer is required.')
    # reftable keeps branch names that differ only in case apart, even on Windows and macOS.
    ref_format = ['--ref-format=reftable'] if c.git_version() >= (2, 45) else []
    started = time.time()

    def one(spec):
        name, src = spec
        c.log(f'{name}: snapshot of {src}')
        info = snapshot(name, src, work, not args.no_fetch, ref_format)
        info = analyze_repo(info, work)
        c.log(f"{name}: {len(info['branches'])} branches, {len(info['tags'])} tags, default '{info['default']}'")
        return info

    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        repos = list(pool.map(one, specs))
    excluded = [r['name'] for r in repos if not r['branches']]
    repos = [r for r in repos if r['branches']]
    if not repos:
        c.die('No source repository has any branch.')

    default_branch, branches, renames = combine(repos)
    combined_tags, per_repo_tags = plan_combined_tags(repos, work)
    tag_names = {t['final'] for t in combined_tags} | {t['final'] for t in per_repo_tags}
    ambiguous = sorted({b['name'] for b in branches} & tag_names)
    for r in repos:
        del r['merged']

    state = {'created': c.now_iso(), 'work': work, 'recent_days': c.RECENT_DAYS, 'excluded': excluded,
             'repos': repos,
             'combined': {'default_branch': default_branch, 'branches': branches, 'renames': renames,
                          'tags': {'combined': combined_tags, 'per_repo': per_repo_tags}, 'ambiguous': ambiguous}}
    state['warnings'] = collect_warnings(repos) + [f'**{n}**: has no branches and is left out.' for n in excluded]
    c.save_json(os.path.join(work, 'analysis.json'), state)
    c.write_text(os.path.join(work, 'analysis.md'), render(state))
    errors = [r['name'] for r in repos if r.get('shallow_snapshot')]
    c.log(f"Done in {time.time() - started:.0f}s: {len(repos)} repositories, {len(branches)} combined branches "
          f"({sum(b['prune'] for b in branches)} to prune), {len(combined_tags)} combined tags, "
          f"{len(per_repo_tags)} per-repository tags, {len(state['warnings'])} warning(s).")
    c.log(f"Wrote {os.path.join(work, 'analysis.md')}")
    if errors:
        c.die(f"Shallow snapshot(s) cannot be migrated: {', '.join(errors)}")


if __name__ == '__main__':
    main()
