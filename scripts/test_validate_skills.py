#!/usr/bin/env python3
"""Regression tests for scripts/validate_skills.py.

Each test copies the repository's skill set into a temporary directory,
introduces one known-bad state, and asserts the validator rejects it. The
first two reproduce defects that actually shipped.

Run: python3 scripts/test_validate_skills.py
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VALIDATOR = "scripts/validate_skills.py"
COPY = [".claude", "plugins", "scripts", "README.md"]

failures: list[str] = []


def sandbox(tmp: Path) -> Path:
    work = tmp / "repo"
    work.mkdir()
    for item in COPY:
        src = ROOT / item
        dst = work / item
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
    return work


def run(work: Path) -> tuple[int, str]:
    proc = subprocess.run([sys.executable, VALIDATOR], cwd=work,
                          capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def edit(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    assert old in text, f"fixture text not found in {path}: {old!r}"
    path.write_text(text.replace(old, new), encoding="utf-8")


def check(name: str, mutate, expect: str) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        work = sandbox(Path(tmp))
        mutate(work)
        code, out = run(work)
        if code == 0:
            failures.append(f"{name}: validator accepted a state it should reject")
        elif not re.search(expect, out):
            failures.append(f"{name}: expected /{expect}/ in output, got:\n{out}")
        else:
            print(f"  pass  {name}")


def test_clean_repo_passes() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        work = sandbox(Path(tmp))
        code, out = run(work)
        if code != 0:
            failures.append(f"clean repository fails validation:\n{out}")
        else:
            print("  pass  clean repository validates")


# --- Defect 1: criterion name and maximum disagreeing across skills ---------

def test_name_mismatch() -> None:
    def mutate(work: Path) -> None:
        edit(work / ".claude/skills/assess-readiness/SKILL.md",
             "| C6.1 | Coding Guidelines |", "| C6.1 | Static Analysis |")
    check("assessment renaming a criterion", mutate,
          r"names C6\.1 'Static Analysis' but verify-c6-1")


def test_max_mismatch() -> None:
    def mutate(work: Path) -> None:
        edit(work / ".claude/skills/assess-readiness/SKILL.md",
             "| C6.1 | Coding Guidelines | [score] | 2 |",
             "| C6.1 | Coding Guidelines | [score] | 3 |")
    check("assessment inflating a maximum score", mutate,
          r"maximum of 3 but verify-c6-1 tops out at 2")


def test_verifier_internal_max_mismatch() -> None:
    def mutate(work: Path) -> None:
        edit(work / ".claude/skills/verify-c6-1/SKILL.md",
             "Reports fulfillment level 0–2.", "Reports fulfillment level 0–3.")
    check("verifier description disagreeing with its own table", mutate,
          r"description says max level 3")


def test_improver_max_mismatch() -> None:
    def mutate(work: Path) -> None:
        edit(work / ".claude/skills/improve-c6-1/SKILL.md",
             "- Level 2: Design principles and patterns additionally documented",
             "- Level 2: Design principles and patterns additionally documented\n"
             "- Level 3: Something beyond the criterion")
    check("improver exceeding the criterion maximum", mutate,
          r"improve-c6-1: tops out at level 3")


# --- Defect 2: an improver targeting behaviour unrelated to its verifier ----

def test_improver_targets_unrelated_behaviour() -> None:
    def mutate(work: Path) -> None:
        target = work / ".claude/skills/improve-c1-1/SKILL.md"
        text = target.read_text(encoding="utf-8")
        # Replace the level definitions with agent-context-file ones, which is
        # what improve-c1-1 used to do: real work, wrong criterion.
        text = re.sub(
            r"\| 0 \|.*?\| 2 \|[^\n]*\n",
            "| 0 | No README and no CLAUDE.md or AGENTS.md |\n"
            "| 1 | README exists but no CLAUDE.md or AGENTS.md |\n"
            "| 2 | CLAUDE.md or AGENTS.md exists with substantive conventions, "
            "commands, and navigation guidance |\n",
            text, flags=re.S)
        target.write_text(text, encoding="utf-8")
    check("improver aimed at a different criterion", mutate,
          r"improve-c1-1: level definitions look unrelated")


# --- Cross-references and mirror sync --------------------------------------

def test_dangling_skill_reference() -> None:
    def mutate(work: Path) -> None:
        edit(work / ".claude/skills/improve-readiness/SKILL.md",
             "`/improve-c6-1`", "`/improve-c6-9`")
    check("reference to a non-existent skill", mutate,
          r"references /improve-c6-9, which is not a skill directory")


def test_dangling_bundled_resource() -> None:
    def mutate(work: Path) -> None:
        edit(work / ".claude/skills/improve-c1-1/SKILL.md",
             "`.claude/skills/improve-c1-1/scripts/merge-repos.sh`",
             "`.claude/skills/improve-c1-1/scripts/absent.sh`")
    check("reference to a missing bundled script", mutate,
          r"references bundled resource `.claude/skills/improve-c1-1/scripts/absent\.sh`")


def test_plugin_mirror_drift() -> None:
    def mutate(work: Path) -> None:
        edit(work / ".claude/skills/verify-c6-1/SKILL.md",
             "# Verify C6.1 — Coding Guidelines",
             "# Verify C6.1 — Coding Guidelines\n\nAn upstream-only edit.")
    check("plugin mirror drifting from source", mutate,
          r"plugins: verify-c6-1/SKILL\.md is out of sync")


def test_readme_name_drift() -> None:
    def mutate(work: Path) -> None:
        edit(work / "README.md",
             "| `/agentize:verify-c3-1` | C3.1 — Architecture Depth |",
             "| `/agentize:verify-c3-1` | C3.1 — Documentation Depth |")
    check("README table renaming a criterion", mutate,
          r"README\.md: names C3\.1 'Documentation Depth'")


def main() -> int:
    print("validate_skills regression tests")
    test_clean_repo_passes()
    test_name_mismatch()
    test_max_mismatch()
    test_verifier_internal_max_mismatch()
    test_improver_max_mismatch()
    test_improver_targets_unrelated_behaviour()
    test_dangling_skill_reference()
    test_dangling_bundled_resource()
    test_plugin_mirror_drift()
    test_readme_name_drift()

    if failures:
        print()
        for f in failures:
            print(f"FAIL  {f}")
        print(f"\n{len(failures)} test(s) failed")
        return 1
    print("\nall tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
