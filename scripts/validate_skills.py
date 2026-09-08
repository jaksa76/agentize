#!/usr/bin/env python3
"""Consistency validation for the agentize skill set.

Every criterion is described in four places: the verify-* skill that scores it,
the assess-* skill that aggregates it, the improve-* skill that raises it, and
the README skill table. This script checks that they agree, so that downstream
distributions (GitHub Copilot and others) can synchronise the skills without
silently importing a contradiction.

Checks performed:

  1. Criterion registry   - each verify-* skill declares a name and a maximum
                            level consistently in its frontmatter description,
                            its title, and its criterion-definition table.
  2. Assessment skills    - assess-readiness / assess-adoption use the same
                            criterion names and maximum scores.
  3. Improver skills      - each improve-* skill uses the same criterion name
                            and tops out at the same maximum level.
  4. Orchestrators        - improve-readiness / improve-adoption threshold
                            tables use the same names and thresholds within max.
  5. README tables        - the documented skill tables use the same names.
  6. Improver alignment   - an improver's level descriptions must be about the
                            same thing its verifier measures.
  7. Cross-references     - /skill and file-path references resolve to
                            something that exists.
  8. Plugin sync          - skills mirrored under plugins/ match their source.

Exit status is 0 when everything agrees, 1 otherwise.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / ".claude" / "skills"
PLUGIN_SKILLS = ROOT / "plugins" / "agentize" / "skills"

errors: list[str] = []
warnings: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def skill_id_to_criterion(skill_dir: str) -> str | None:
    """verify-c1-1 -> C1.1, improve-a3 -> A3."""
    m = re.fullmatch(r"(?:verify|improve)-([ca])(\d+)(?:-(\d+))?", skill_dir)
    if not m:
        return None
    letter, major, minor = m.groups()
    if minor:
        return f"{letter.upper()}{major}.{minor}"
    return f"{letter.upper()}{major}"


def frontmatter(text: str) -> dict[str, str]:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


# --------------------------------------------------------------------------
# 1. Build the criterion registry from the verify-* skills (the authority).
# --------------------------------------------------------------------------

class Criterion:
    def __init__(self, cid: str, name: str, max_level: int, levels: dict[int, str]):
        self.id = cid
        self.name = name
        self.max_level = max_level
        self.levels = levels


def build_registry() -> dict[str, Criterion]:
    registry: dict[str, Criterion] = {}
    for d in sorted(SKILLS.glob("verify-*")):
        cid = skill_id_to_criterion(d.name)
        if cid is None:
            fail(f"{d.name}: skill directory name does not map to a criterion id")
            continue
        text = read(d / "SKILL.md")

        # Name from the H1 title: "# Verify C1.1 — Codebase Accessibility"
        m = re.search(r"^#\s*Verify\s+([A-Z]\d+(?:\.\d+)?)\s*[—-]\s*(.+?)\s*$",
                      text, re.M)
        if not m:
            fail(f"{d.name}: no '# Verify <ID> — <Name>' title found")
            continue
        title_id, name = m.group(1), m.group(2)
        if title_id != cid:
            fail(f"{d.name}: title says {title_id}, directory implies {cid}")

        # Max from the frontmatter description: "Reports fulfillment level 0–N."
        desc = frontmatter(text).get("description", "")
        m = re.search(r"fulfillment level 0[–-](\d+)", desc)
        if not m:
            fail(f"{d.name}: description does not state 'fulfillment level 0–N'")
            continue
        desc_max = int(m.group(1))

        # Max and level text from the criterion-definition table.
        levels: dict[int, str] = {}
        for lm in re.finditer(r"^\|\s*(\d)\s*\|\s*(.+?)\s*\|\s*$", text, re.M):
            levels[int(lm.group(1))] = lm.group(2)
        if not levels:
            fail(f"{d.name}: no criterion-definition level table found")
            continue
        table_max = max(levels)

        if desc_max != table_max:
            fail(f"{d.name}: description says max level {desc_max} but the "
                 f"criterion-definition table tops out at {table_max}")

        # Report format must offer exactly the levels the criterion defines.
        rm = re.search(r"\*\*Level\*\*:\s*\[([^\]]+)\]", text)
        if rm:
            offered = [t.strip() for t in rm.group(1).split("/")]
            numeric = [t for t in offered if t.isdigit()]
            if numeric and max(int(t) for t in numeric) != table_max:
                fail(f"{d.name}: report format offers levels {offered} but the "
                     f"criterion maximum is {table_max}")

        registry[cid] = Criterion(cid, name, table_max, levels)
    return registry


# --------------------------------------------------------------------------
# 2 & 4. Assessment and orchestration skills.
# --------------------------------------------------------------------------

def check_assessment(skill: str, registry: dict[str, Criterion], prefix: str) -> None:
    path = SKILLS / skill / "SKILL.md"
    if not path.exists():
        fail(f"{skill}: SKILL.md not found")
        return
    text = read(path)
    seen = set()

    # Step 1 list: "- **C6.1 Coding Guidelines** — follow the `/verify-c6-1` skill"
    for m in re.finditer(
            r"^-\s*\*\*([A-Z]\d+(?:\.\d+)?)\s+(.+?)\*\*\s*[—-]\s*follow the\s*`/(\S+?)`",
            text, re.M):
        cid, name, target = m.group(1), m.group(2), m.group(3)
        target = target.split(":")[-1]
        if cid not in registry:
            fail(f"{skill}: references unknown criterion {cid}")
            continue
        seen.add(cid)
        if name != registry[cid].name:
            fail(f"{skill}: {cid} is named '{name}' but {target} names it "
                 f"'{registry[cid].name}'")
        expected = f"verify-{cid.lower().replace('.', '-')}"
        if target != expected:
            fail(f"{skill}: {cid} delegates to /{target}, expected /{expected}")

    # Score table: "| C6.1 | Coding Guidelines | [score] | 2 |"
    for m in re.finditer(
            r"^\|\s*([A-Z]\d+(?:\.\d+)?)\s*\|\s*(.+?)\s*\|\s*\[[^\]]*\]\s*\|\s*(\d+)\s*\|",
            text, re.M):
        cid, name, mx = m.group(1), m.group(2), int(m.group(3))
        if cid not in registry:
            fail(f"{skill}: score table references unknown criterion {cid}")
            continue
        if name != registry[cid].name:
            fail(f"{skill}: score table names {cid} '{name}' but verify-"
                 f"{cid.lower().replace('.', '-')} names it '{registry[cid].name}'")
        if mx != registry[cid].max_level:
            fail(f"{skill}: score table gives {cid} a maximum of {mx} but "
                 f"verify-{cid.lower().replace('.', '-')} tops out at "
                 f"{registry[cid].max_level}")

    expected_ids = {c for c in registry if c.startswith(prefix)}
    missing = expected_ids - seen
    if missing:
        fail(f"{skill}: does not score {', '.join(sorted(missing))}")


def check_orchestrator(skill: str, registry: dict[str, Criterion], prefix: str) -> None:
    path = SKILLS / skill / "SKILL.md"
    if not path.exists():
        fail(f"{skill}: SKILL.md not found")
        return
    text = read(path)

    # Threshold table: "| C6.1 Coding Guidelines | — | ≥ 1 | ≥ 2 |"
    for m in re.finditer(
            r"^\|\s*([A-Z]\d+(?:\.\d+)?)\s+([A-Za-z][^|]*?)\s*\|((?:[^|\n]*\|){2,})\s*$",
            text, re.M):
        cid, name, rest = m.group(1), m.group(2).strip(), m.group(3)
        if cid not in registry:
            continue
        if name != registry[cid].name:
            fail(f"{skill}: threshold table names {cid} '{name}' but verify-"
                 f"{cid.lower().replace('.', '-')} names it '{registry[cid].name}'")
        for tm in re.finditer(r"≥\s*(\d+)", rest):
            need = int(tm.group(1))
            if need > registry[cid].max_level:
                fail(f"{skill}: threshold table requires {cid} ≥ {need} but the "
                     f"criterion maximum is {registry[cid].max_level}")

    # Delegation list: "- **C6.1 is blocking** → follow the `/improve-c6-1` skill"
    for m in re.finditer(
            r"\*\*([A-Z]\d+(?:\.\d+)?) is blocking\*\*.*?`/(\S+?)`", text):
        cid, target = m.group(1), m.group(2).split(":")[-1]
        expected = f"improve-{cid.lower().replace('.', '-')}"
        if target != expected:
            fail(f"{skill}: {cid} delegates to /{target}, expected /{expected}")
        if not (SKILLS / target).is_dir():
            fail(f"{skill}: delegates to /{target}, which does not exist")


# --------------------------------------------------------------------------
# 3 & 6. Improver skills: naming, maximum, and topical alignment.
# --------------------------------------------------------------------------

STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "into", "level",
    "levels", "project", "projects", "exist", "exists", "existing", "some",
    "none", "other", "others", "than", "only", "also", "any", "all", "not",
    "but", "are", "was", "were", "has", "have", "had", "can", "via", "per",
    "its", "their", "there", "when", "where", "which", "while", "each",
    "must", "should", "documented", "configured", "basic", "full", "more",
    "less", "over", "under", "about", "requires", "required", "raise",
    "raises", "improve", "improvement", "current", "step", "state", "report",
    "criterion", "skill", "instructions", "evidence",
}


def content_terms(text: str) -> set[str]:
    words = re.findall(r"[A-Za-z][A-Za-z0-9._-]{3,}", text.lower())
    out = set()
    for w in words:
        w = w.strip("._-")
        if len(w) > 3 and w not in STOPWORDS:
            out.add(w)
            # crude singularisation so "repos"/"repo" and "tests"/"test" match
            if w.endswith("s") and len(w) > 4:
                out.add(w[:-1])
    return out


def improver_levels(text: str) -> dict[int, str]:
    """Improvers state levels either as a table or as a bullet list."""
    levels = {int(m.group(1)): m.group(2).strip()
              for m in re.finditer(r"^\|\s*(\d)\s*\|\s*(.+?)\s*\|\s*$", text, re.M)}
    for m in re.finditer(r"^-\s*Level\s*(\d)\s*:\s*(.+?)\s*$", text, re.M):
        levels.setdefault(int(m.group(1)), m.group(2).strip())
    return levels


ALIGNMENT_THRESHOLD = 0.25


def check_improver(cid: str, crit: Criterion) -> None:
    slug = f"improve-{cid.lower().replace('.', '-')}"
    path = SKILLS / slug / "SKILL.md"
    if not path.exists():
        warn(f"{slug}: no improver skill for {cid}")
        return
    text = read(path)

    m = re.search(r"^#\s*Improve\s+([A-Z]\d+(?:\.\d+)?)\s*[—-]\s*(.+?)\s*$", text, re.M)
    if not m:
        fail(f"{slug}: no '# Improve <ID> — <Name>' title found")
        return
    title_id, name = m.group(1), m.group(2)
    if title_id != cid:
        fail(f"{slug}: title says {title_id}, directory implies {cid}")
    if name != crit.name:
        fail(f"{slug}: names {cid} '{name}' but verify-"
             f"{cid.lower().replace('.', '-')} names it '{crit.name}'")

    levels = improver_levels(text)
    if not levels:
        fail(f"{slug}: states no level definitions")
        return
    if max(levels) != crit.max_level:
        fail(f"{slug}: tops out at level {max(levels)} but the criterion "
             f"maximum is {crit.max_level}")

    # Alignment: the improver must be about what the verifier measures.
    verifier_terms = content_terms(" ".join(crit.levels.values()) + " " + crit.name)
    improver_terms = content_terms(" ".join(levels.values()) + " " + name)
    if not verifier_terms:
        return
    overlap = verifier_terms & improver_terms
    ratio = len(overlap) / len(verifier_terms)
    if ratio < ALIGNMENT_THRESHOLD:
        fail(f"{slug}: level definitions look unrelated to what verify-"
             f"{cid.lower().replace('.', '-')} measures "
             f"(term overlap {ratio:.0%}, need {ALIGNMENT_THRESHOLD:.0%}). "
             f"The verifier measures: {list(crit.levels.values())[-1]!r}. "
             f"The improver targets: {list(levels.values())[-1]!r}.")


# --------------------------------------------------------------------------
# 5. README tables.
# --------------------------------------------------------------------------

def check_readme(registry: dict[str, Criterion]) -> None:
    text = read(ROOT / "README.md")
    rows = re.findall(
        r"^\|\s*`/(?:\w+:)?(verify-[a-z0-9-]+)`\s*\|\s*([A-Z]\d+(?:\.\d+)?)\s*[—-]\s*(.+?)\s*\|",
        text, re.M)
    if not rows:
        fail("README.md: no skill table rows found")
        return
    for slug, cid, name in rows:
        if not (SKILLS / slug).is_dir():
            fail(f"README.md: lists /{slug}, which is not a skill directory")
            continue
        if cid not in registry:
            fail(f"README.md: lists unknown criterion {cid}")
            continue
        expected = f"verify-{cid.lower().replace('.', '-')}"
        if slug != expected:
            fail(f"README.md: row for {cid} points at /{slug}, expected /{expected}")
        if name != registry[cid].name:
            fail(f"README.md: names {cid} '{name}' but {slug} names it "
                 f"'{registry[cid].name}'")


# --------------------------------------------------------------------------
# 7. Cross-references.
# --------------------------------------------------------------------------

# Skills in this repository are always named verify-*, improve-*, or assess-*.
# Skills that an improver *creates in the target project* (generate-story,
# decompose-epic, ...) use other names and are deliberately not checked here.
OWN_SKILL_PREFIXES = ("verify-", "improve-", "assess-")


def check_cross_references() -> None:
    skill_dirs = {d.name for d in SKILLS.iterdir() if d.is_dir()}
    for path in sorted(SKILLS.glob("*/SKILL.md")):
        text = read(path)
        owner = path.parent.name

        # `/skill-name` and `/agentize:skill-name` references in backticks.
        for m in re.finditer(r"`/(?:\w+:)?([a-z][a-z0-9-]+)`", text):
            target = m.group(1)
            if not target.startswith(OWN_SKILL_PREFIXES):
                continue
            if target not in skill_dirs:
                fail(f"{owner}: references /{target}, which is not a skill "
                     f"directory under .claude/skills/")

        # Resources bundled with this skill (scripts, templates, references).
        # Paths under another skill's directory, or under the *target* project's
        # .claude/, are not this repository's to resolve.
        prefix = f".claude/skills/{owner}/"
        for m in re.finditer(r"`(\.claude/[A-Za-z0-9._/-]+)`", text):
            ref = m.group(1)
            if not ref.startswith(prefix) or "<" in ref or ">" in ref:
                continue
            if not (ROOT / ref).exists():
                fail(f"{owner}: references bundled resource `{ref}`, "
                     f"which does not exist")


# --------------------------------------------------------------------------
# 8. Plugin mirror sync.
# --------------------------------------------------------------------------

def normalise(text: str) -> str:
    """Plugin copies differ only by the /agentize: skill-invocation prefix."""
    return re.sub(r"`/agentize:", "`/", text)


def check_plugin_sync() -> None:
    if not PLUGIN_SKILLS.is_dir():
        return
    for path in sorted(PLUGIN_SKILLS.glob("*/SKILL.md")):
        source = SKILLS / path.parent.name / "SKILL.md"
        if not source.exists():
            fail(f"plugins: {path.parent.name} has no counterpart under "
                 f".claude/skills/")
            continue
        if normalise(read(path)) != normalise(read(source)):
            fail(f"plugins: {path.parent.name}/SKILL.md is out of sync with "
                 f".claude/skills/{path.parent.name}/SKILL.md")


# --------------------------------------------------------------------------

def main() -> int:
    registry = build_registry()
    if not registry:
        print("no verify-* skills found", file=sys.stderr)
        return 1

    check_assessment("assess-readiness", registry, "C")
    check_assessment("assess-adoption", registry, "A")
    check_orchestrator("improve-readiness", registry, "C")
    check_orchestrator("improve-adoption", registry, "A")
    for cid, crit in sorted(registry.items()):
        check_improver(cid, crit)
    check_readme(registry)
    check_cross_references()
    check_plugin_sync()

    print(f"criteria checked: {len(registry)} "
          f"({', '.join(sorted(registry))})")
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"FAIL  {e}")
    if errors:
        print(f"\n{len(errors)} consistency error(s)")
        return 1
    print(f"\nall consistency checks passed"
          f"{f' ({len(warnings)} warning(s))' if warnings else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
