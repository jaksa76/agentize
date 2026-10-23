# Copyright (c) 2026 Codomain D.O.O. All rights reserved.
# Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
# See LICENSE.md for details.
"""Helpers shared by the merge phases (analyze, migrate, cleanup, verify, report).

All phases keep their state in one work directory:

    <work>/analysis.json      the plan: every decision is taken here, by analyze.py
    <work>/snapshot/<r>.git   untouched copy of each source repository (the reference for verification)
    <work>/commit-maps/<r>    source commit -> rewritten commit, written by git filter-repo
    <work>/migration.json     what migrate.py built
    <work>/cleanup.json       what cleanup.py changed
    <work>/verification.json  what verify.py checked
    <work>/*.md               one summary per phase; report.py joins them into migration-report.md
"""
import datetime
import json
import os
import re
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


def fallback_branch(repo, branch):
    """The branch of `repo` that a combined branch it does not have should contain (git-flow)."""
    if branch in repo['targets']:
        return branch
    lower = branch.lower()
    if lower in PRODUCTION_BRANCHES or PRODUCTION_CHILD.match(branch):
        return repo['production']
    if lower == DEVELOP_BRANCH:
        return repo['develop'] or repo['production']
    return repo['develop'] or repo['default_target']
