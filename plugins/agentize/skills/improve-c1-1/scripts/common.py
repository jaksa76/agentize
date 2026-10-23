# Copyright (c) 2026 Codomain D.O.O. All rights reserved.
# Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
# See LICENSE.md for details.
"""Helpers shared by the merge phases (analyze, migrate, cleanup, verify, report).

All phases keep their state in one work directory:

    <work>/analysis.json      the plan: every decision is taken here, by analyze.py
    <work>/snapshot/<r>.git   untouched copy of each source repository (the reference for verification)
    <work>/commit-maps/<r>    source commit -> rewritten commit, written by git filter-repo
    <work>/migration.json     what migrate.py built
    <work>/cleanup-plan.json  the cleanup proposed by cleanup.py --plan, edited in review
                              (cleanup-plan.proposed.json: as proposed; cleanup-plan.applied.json: as applied)
    <work>/cleanup.json       what cleanup.py --apply changed
    <work>/verification.json  what verify.py checked
    <work>/*.md               one summary per phase; report.py joins them into migration-report.md
"""
import datetime
import fnmatch
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import threading
from collections import Counter, defaultdict

# Branches whose tip is older than this (relative to the repository's newest branch) are not "recent".
RECENT_DAYS = 90
# The newest N branches of a repository always count as recent, so a dormant repo still gets checked.
MIN_RECENT_BRANCHES = 5
PRODUCTION_BRANCHES = ('master', 'main')
DEVELOP_BRANCH = 'develop'
# Branches created from the production branch in git-flow; everything else comes from develop.
PRODUCTION_CHILD = re.compile(r'^(hotfix|support)/', re.I)
# Long-lived branch kinds that cleanup never removes.
LONG_LIVED = re.compile(r'^(release|hotfix|support)/', re.I)
# A release tag: an optional prefix (`v`, `release-`, ...) and a version number.
VERSION_TAG = re.compile(r'^(?:v|version[-_]?|release[-_/]?|rel[-_]?)?(\d+(?:\.\d+)*(?:[-+._].*)?)$', re.I)
# Paths longer than this (inside the monorepo) are likely to hit Windows' 260-character limit.
LONG_PATH = 200

_lock = threading.Lock()
_prefix = 'merge'


def set_prefix(name):
    global _prefix
    _prefix = name
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding='utf-8', errors='replace')
        except (AttributeError, ValueError):
            pass


def log(msg):
    with _lock:
        print(f'[{_prefix}] {msg}', flush=True)


def warn(msg):
    with _lock:
        print(f'[{_prefix}] WARNING: {msg}', file=sys.stderr, flush=True)


def die(msg):
    with _lock:
        print(f'[{_prefix}] ERROR: {msg}', file=sys.stderr, flush=True)
    sys.exit(1)


class GitError(RuntimeError):
    pass


def _env(extra):
    if not extra:
        return None
    env = dict(os.environ)
    env.update(extra)
    return env


def git(args, cwd=None, input=None, env=None):
    """Runs git and returns its stdout; raises GitError on failure."""
    rc, out, err = git_ok(args, cwd=cwd, input=input, env=env)
    if rc != 0:
        raise GitError(f"git {' '.join(args)} failed in {cwd}: {err.strip()}")
    return out


def git_ok(args, cwd=None, input=None, env=None):
    """Runs git and returns (returncode, stdout, stderr) without raising."""
    # Bytes, not text mode: text-mode pipes on Windows turn '\n' into '\r\n'.
    data = input.encode('utf-8', 'surrogateescape') if input is not None else None
    p = subprocess.run(['git'] + list(args), cwd=cwd, input=data, capture_output=True, env=_env(env))
    return (p.returncode, p.stdout.decode('utf-8', 'surrogateescape'),
            p.stderr.decode('utf-8', 'replace'))


def git_version():
    out = git(['--version'])
    m = re.search(r'(\d+)\.(\d+)', out)
    return (int(m.group(1)), int(m.group(2))) if m else (0, 0)


class CatFile:
    """A long-running `git cat-file --batch`, for reading many objects quickly."""

    def __init__(self, repo):
        self.p = subprocess.Popen(['git', 'cat-file', '--batch'], cwd=repo,
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def _header(self, spec):
        self.p.stdin.write(spec.encode('utf-8', 'surrogateescape') + b'\n')
        self.p.stdin.flush()
        parts = self.p.stdout.readline().rstrip(b'\n').decode('utf-8', 'replace').split(' ')
        if len(parts) != 3 or parts[1] not in ('blob', 'tree', 'commit', 'tag'):
            return None
        return parts[0], parts[1], int(parts[2])

    def read(self, spec):
        """Returns (oid, type, bytes) or None when the object does not exist."""
        header = self._header(spec)
        if header is None:
            return None
        oid, typ, size = header
        data = self.p.stdout.read(size)
        self.p.stdout.read(1)
        return oid, typ, data

    def oid(self, spec):
        """Returns (oid, type) without keeping the content, or None."""
        found = self.read(spec)
        return (found[0], found[1]) if found else None

    def close(self):
        if self.p.poll() is None:
            self.p.stdin.close()
            self.p.wait()


def parse_tree(data, oid_len):
    """Parses a raw tree object into [(mode, name, oid)]."""
    entries, i = [], 0
    while i < len(data):
        sp = data.index(b' ', i)
        nul = data.index(b'\0', sp)
        entries.append((data[i:sp], data[sp + 1:nul], data[nul + 1:nul + 1 + oid_len].hex()))
        i = nul + 1 + oid_len
    return entries


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


def load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=1, ensure_ascii=False)


def write_text(path, text):
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)


def day(ts):
    return datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).strftime('%Y-%m-%d') if ts else '-'


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')


def load_commit_map(work, repo):
    """Source commit -> rewritten commit, as recorded by git filter-repo."""
    mapping = {}
    with open(os.path.join(work, 'commit-maps', repo), encoding='ascii') as f:
        next(f)
        for line in f:
            old, new = line.split()
            mapping[old] = new
    return mapping


def identity():
    """The author of the combining commits and tags: the user's git identity, if set."""
    name = git_ok(['config', 'user.name'])[1].strip() or 'Monorepo Migration'
    email = git_ok(['config', 'user.email'])[1].strip() or 'monorepo-migration@localhost'
    return name, email


def commit_env(ts):
    name, email = identity()
    date = f'{ts} +0000'
    return {'GIT_AUTHOR_NAME': name, 'GIT_AUTHOR_EMAIL': email, 'GIT_AUTHOR_DATE': date,
            'GIT_COMMITTER_NAME': name, 'GIT_COMMITTER_EMAIL': email, 'GIT_COMMITTER_DATE': date}


def mktree(repo, entries):
    """Creates a tree from [(name, subtree oid)] and returns its oid."""
    lines = ''.join(f'040000 tree {oid}\t{name}\n' for name, oid in entries)
    return git(['mktree'], cwd=repo, input=lines).strip()


# ---------------------------------------------------------------------------
# Ref names
# ---------------------------------------------------------------------------

def _uppercase(s):
    return sum(1 for ch in s if ch.isupper())


def _best_spelling(counts):
    """The most used spelling; on a tie the one with fewer capitals (typos like 'FIltering'), then a-z."""
    return sorted(counts.items(), key=lambda kv: (-kv[1], _uppercase(kv[0]), kv[0]))[0][0]


def canonical_case(weights):
    """Maps every ref name to one spelling per case-insensitive name.

    Windows, macOS and Azure Repos treat `Feature/x` and `feature/x` as the same ref, so names that differ
    only in case must become one. This is decided folder by folder, so `Feature/a` and `feature/b` also
    end up in the same folder. `weights` maps each name to how many repositories use that spelling.
    """
    prefixes = defaultdict(Counter)
    for name, weight in weights.items():
        parts = name.split('/')
        for i in range(1, len(parts) + 1):
            prefix = '/'.join(parts[:i])
            prefixes[prefix.lower()][prefix] += weight
    result = {}
    for name in weights:
        parts = name.split('/')
        result[name] = '/'.join(_best_spelling(prefixes['/'.join(parts[:i]).lower()]).split('/')[-1]
                                for i in range(1, len(parts) + 1))
    return result


def resolve_dir_file(names, suffix):
    """Renames names that are also a folder of another name.

    Git cannot store both `refs/heads/a` and `refs/heads/a/b`. Returns {old: new} for the renamed ones.
    """
    names = set(names)
    taken = {n.lower() for n in names}
    folders = set()
    for n in names:
        parts = n.lower().split('/')
        for i in range(1, len(parts)):
            folders.add('/'.join(parts[:i]))
    renamed = {}
    for n in sorted(names):
        if n.lower() in folders:
            new, k = n + suffix, 2
            while new.lower() in taken or new.lower() in folders:
                new, k = f'{n}{suffix}-{k}', k + 1
            taken.add(new.lower())
            renamed[n] = new
    return renamed


# ---------------------------------------------------------------------------
# Combined branches
# ---------------------------------------------------------------------------

# What a repository that doesn't have a combined branch contributes to it.
FALLBACK_KINDS = ('base', 'develop', 'production', 'default', 'none')


def default_options():
    """The migration's defaults; migrate.py's command-line options override them."""
    return {'mixed_bases': 'split', 'split': [], 'combine': [], 'merged_content': 'target', 'fallbacks': [],
            'contribute': [], 'default_branch': None}


def _source_for(repo, kind, base):
    """The branch of `repo` that a fallback of this kind means, or None."""
    if kind == 'none':
        return None
    if kind == 'production':
        return repo['production']
    if kind == 'develop':
        return repo['develop'] or repo['production']
    if kind == 'default':
        return repo['default_target']
    if base is None:
        return repo['develop'] or repo['default_target']
    if base.lower() == DEVELOP_BRANCH:
        return repo['develop'] or repo['production']
    return base if base in repo['targets'] else repo['production']


def _trunk_source(repo, name):
    """What a repository contributes to a trunk branch (production, develop, a default branch) it lacks."""
    lower = name.lower()
    if lower in PRODUCTION_BRANCHES:
        return repo['production']
    if lower == DEVELOP_BRANCH:
        return repo['develop'] or repo['production']
    return repo['develop'] or repo['default_target']


def _fallback(repo, name, base, trunk, options):
    for pattern, kind in options['fallbacks']:
        if fnmatch.fnmatchcase(name.lower(), pattern.lower()):
            return _source_for(repo, kind, base)
    if trunk:
        return _trunk_source(repo, name)
    # A release, hotfix or support branch ends up in production, so the others contribute production.
    if LONG_LIVED.match(name):
        return repo['production']
    # A branch with no history in common with any trunk (gh-pages, an imported project) stands alone.
    return _source_for(repo, 'base', base) if base else None


def note(kind, text):
    """A decision about a combined branch that differs from simply combining it."""
    return {'kind': kind, 'text': text}


def most_common(values):
    found = Counter(v for v in values if v)
    return sorted(found.items(), key=lambda kv: (-kv[1], kv[0]))[0][0] if found else None


def expected_base(name, production, develop):
    """The trunk git-flow creates a branch of this name from."""
    return production if PRODUCTION_CHILD.match(name) else develop or production


def compose(plan, options=None):
    """Decides every combined branch: its name and which branch each repository contributes.

    Repositories that have the branch contribute it, except that a repository which already merged it
    contributes the branch it was merged into while other repositories still work on theirs. When the
    repositories created the branch from different trunks, those that differ from the majority get their own
    branch, `<repo>/<branch>`. Repositories that don't have the branch contribute the trunk it was created
    from (production for release/hotfix/support), or nothing when it shares no history with any trunk.
    `options` (see default_options) override these rules. Returns (default_branch, branches).
    """
    o = dict(default_options(), **(options or {}))
    repos = plan['repos']
    by_repo = {r['name']: r for r in repos}
    owners = defaultdict(dict)
    for r in repos:
        for b in r['branches']:
            owners[b['target']][r['name']] = b
    production = most_common(r['production'] for r in repos)
    develop = most_common(r['develop'] for r in repos) or DEVELOP_BRANCH
    trunks = {r[k] for r in repos for k in ('production', 'develop', 'default_target') if r[k]}
    protected_names = {plan['combined']['default_branch']} | {r['default_target'] for r in repos}
    taken = {n.lower() for n in owners}
    folders = {'/'.join(n.lower().split('/')[:i]) for n in owners for i in range(1, n.count('/') + 1)}
    split_one = defaultdict(set)
    for item in o['split']:
        name, _, repo = item.partition(':')
        split_one[name].add(repo)

    def build(name, origin, members, base, notes):
        trunk = origin in trunks or origin.lower() in PRODUCTION_BRANCHES + (DEVELOP_BRANCH,)
        active = [rn for rn, b in members.items() if not b.get('merged')]
        composition = {}
        for r in repos:
            rn, b = r['name'], members.get(r['name'])
            if b and b.get('merged') and active and o['merged_content'] == 'target':
                parents = [b['merge_target']] + ([b['target']] if b['merged'] == 'squash' else [])
                composition[rn] = {'content': b['merge_target'], 'parents': parents, 'role': 'merged'}
                how = 'squash/rebase-merged' if b['merged'] == 'squash' else 'merged'
                notes.append(note('merged', f"{rn} already {how} it into {b['merge_target']}, so {rn}/ holds "
                                            f"{b['merge_target']}; its own branch stays in the history"))
            elif b:
                composition[rn] = {'content': b['target'], 'parents': [b['target']], 'role': 'own'}
            else:
                src = _fallback(r, origin, base, trunk, o)
                composition[rn] = {'content': src, 'parents': [src] if src else [],
                                   'role': 'fallback' if src else 'none'}
        for item in o['contribute']:
            if item['branch'] == name:
                src = item['source']
                composition[item['repo']] = {'content': src, 'parents': [src] if src else [], 'role': 'override'}
                notes.append(note('override', f"{item['repo']} contributes {src or 'nothing'} (command-line option)"))
        excluded = [rn for rn, x in composition.items() if x['role'] == 'none']
        if excluded:
            notes.append(note('excluded', f"shares no history with any trunk, so {', '.join(excluded)} "
                                          f"{'is' if len(excluded) == 1 else 'are'} left out of it"))
        protected = (origin in protected_names or origin.lower() in PRODUCTION_BRANCHES + (DEVELOP_BRANCH,)
                     or bool(LONG_LIVED.match(origin)))
        # Removed in cleanup when every repository that has it merged it and stopped using it.
        prune = not protected and all(b['origin'] == 'remote' and b.get('in_trunk')
                                      and origin not in by_repo[rn]['recent'] for rn, b in members.items())
        why = (f"merged into develop or the production branch; inactive since "
               f"{day(max(b['date'] for b in members.values()))}" if prune else '')
        return {'name': name, 'split_from': origin if name != origin else None, 'owners': sorted(members),
                'base': base, 'composition': composition, 'notes': notes, 'protected': protected,
                'prune': prune, 'prune_reason': why}

    branches = []
    for name in sorted(owners, key=str.lower):
        own = owners[name]
        groups = defaultdict(dict)
        for rn, b in own.items():
            groups[b.get('base')][rn] = b
        expected = expected_base(name, production, develop)
        main = sorted(groups, key=lambda k: (-len(groups[k]), k != expected,
                                             -max(b['date'] for b in groups[k].values())))[0]
        moved = {rn for rn in split_one.get(name, ()) if rn in own}
        if len(groups) > 1 and name not in o['combine'] and (o['mixed_bases'] == 'split' or name in o['split']):
            moved |= {rn for k, members in groups.items() if k != main for rn in members}
        # `<repo>/<branch>` must not be, contain or sit inside another branch name.
        clash = [f'{rn}/{name}' for rn in moved
                 if f'{rn}/{name}'.lower() in taken | folders
                 or any('/'.join(f'{rn}/{name}'.lower().split('/')[:i]) in taken
                        for i in range(1, name.count('/') + 2))]
        notes = []
        if clash:
            notes.append(note('split', f"not split: {', '.join(clash)} clashes with another branch name"))
            moved = set()
        stay = {rn: b for rn, b in own.items() if rn not in moved}
        if moved and not stay:
            stay, moved = own, set()
        for rn in sorted(moved):
            b = own[rn]
            why = (f"{rn} created it from {b.get('base') or 'no trunk'}, the others from {main or 'no trunk'}"
                   if b.get('base') != main else f'{rn} is kept apart (command-line option)')
            notes.append(note('split', f'{why}: moved to {rn}/{name}'))
        branches.append(build(name, name, stay, main, notes))
        for rn in sorted(moved):
            b = own[rn]
            branches.append(build(f'{rn}/{name}', name, {rn: b}, b.get('base'),
                                  [note('split-off', f"{rn}'s branch, split from {name}")]))
    names = {b['name'] for b in branches}
    default_branch = o['default_branch'] or plan['combined']['default_branch']
    if default_branch not in names:
        raise ValueError(f"default branch '{default_branch}' is not one of the combined branches")
    return default_branch, branches
