#!/usr/bin/env python3
"""
Agentic Coding Maturity Quiz
Evaluate your project against the Agent Readiness and Adoption models.
"""

import sys

# ── Criteria definitions ──────────────────────────────────────────────────────

READINESS_CRITERIA = [
    {
        "id": "C1.1",
        "name": "Codebase Accessibility",
        "note": None,
        "levels": [
            "Code split across unlinked repos with no entry point",
            "All code reachable from a single root with a basic README",
            "Comprehensive entry-point guide (CLAUDE.md or equivalent) with conventions and navigation hints",
        ],
    },
    {
        "id": "C2.1",
        "name": "Setup Automation",
        "note": None,
        "levels": [
            "No setup instructions",
            "Written step-by-step instructions",
            "Single script installs all dependencies",
            "Containerised environment (devcontainer, Nix, etc.)",
        ],
    },
    {
        "id": "C3.1",
        "name": "Architecture Depth",
        "note": None,
        "levels": [
            "No in-repo architecture docs",
            "System context documented (users, external systems)",
            "Container/service level documented",
            "Component level documented + critical flows documented",
        ],
    },
    {
        "id": "C4.1",
        "name": "Requirements Access",
        "note": None,
        "levels": [
            "No documented requirements",
            "Product vision and goals documented",
            "User stories or acceptance criteria accessible",
            "Full programmatic access via MCP server or API",
        ],
    },
    {
        "id": "C5.1",
        "name": "Runnability",
        "note": None,
        "levels": [
            "Project does not build",
            "Project builds without errors",
            "App can be run locally or in an ephemeral environment",
        ],
    },
    {
        "id": "C5.2",
        "name": "Unit Test Coverage",
        "note": None,
        "levels": [
            "No unit tests",
            "Some tests present (<50% coverage)",
            "≥50% coverage",
            "≥80% coverage",
        ],
    },
    {
        "id": "C5.3",
        "name": "Integration and E2E Coverage",
        "note": "Level 3 (UI visual regression) may be omitted for projects without a UI.",
        "levels": [
            "No automated integration or E2E tests",
            "Integration tests cover key boundaries",
            "E2E tests cover critical flows",
            "E2E + UI visual regression (if UI present)",
        ],
    },
    {
        "id": "C6.1",
        "name": "Static Analysis",
        "note": None,
        "levels": [
            "No quality tooling",
            "Linting and/or formatting configured",
            "Linting + type checking enforced",
            "Linting + type checking + security scanning (SAST)",
        ],
    },
    {
        "id": "C7.1",
        "name": "Test Isolation",
        "note": "May be omitted for projects without a database or external dependencies.",
        "levels": [
            "No isolation from external systems or data",
            "In-code mocks/stubs and basic fixtures",
            "Reproducible DB state via seed scripts + sandbox environments from vendors",
        ],
    },
    {
        "id": "C8.1",
        "name": "CI/CD Automation",
        "note": None,
        "levels": [
            "No access to pipeline",
            "Agents can read pipeline status",
            "Agents can trigger pipeline runs",
            "Full pipeline control including deployment",
        ],
    },
    {
        "id": "C8.2",
        "name": "Observability",
        "note": None,
        "levels": [
            "No access to logs or metrics",
            "Read-only access to logs/metrics",
            "Queryable monitoring and logs",
            "Automated anomaly detection and alerting",
        ],
    },
]

ADOPTION_CRITERIA = [
    {
        "id": "A1",
        "name": "Agent Context Availability",
        "note": None,
        "levels": [
            "No agent context files; agents must infer everything from raw code",
            "Basic README or project description exists; agents have a starting point but no conventions or navigation guidance",
            "CLAUDE.md or AGENTS.md provides project-specific guidance: conventions, architecture overview, key commands",
            "Comprehensive agent context including architecture docs for agent consumption AND MCP servers exposing project knowledge (requirements, diagrams, runbooks)",
        ],
    },
    {
        "id": "A2",
        "name": "Agent-Authored Contributions",
        "note": "'Recent' = last 90 days or last 50 commits, whichever covers more changes.",
        "levels": [
            "No agent-authored code in git history; all commits are purely human-written",
            "Occasional co-authored commits; agents contributed to fewer than 25% of recent changes",
            "Regular agent contributions; agents co-authored 25–75% of recent changes",
            "Agents autonomously create pull requests; more than 75% of implementation work has significant agent involvement",
        ],
    },
    {
        "id": "A3",
        "name": "Feedback Loop Closure",
        "note": None,
        "levels": [
            "Agents produce output and hand it directly to the human; no self-verification",
            "Agents run basic checks (compilation, syntax) but do not iterate on failures",
            "Agents run the full test suite and linter, iterate on failures, and present only passing results",
            "Agents have access to CI pipeline results, production monitoring, and MCP-connected tool outputs; includes post-deployment checks",
        ],
    },
    {
        "id": "A4",
        "name": "Task Scope",
        "note": None,
        "levels": [
            "Agents only answer questions or explain code; they do not make changes",
            "Agents handle bounded edits: a single function, a bug fix, a single-file change",
            "Agents implement complete features spanning multiple files, writing and running tests",
            "Agents implement entire user stories end-to-end, including cross-service changes, test suites, documentation, and migration scripts",
        ],
    },
    {
        "id": "A5",
        "name": "Workflow Integration",
        "note": None,
        "levels": [
            "Agents are used in isolation; all handoffs (PRs, reviews, CI, deployments) are managed by humans",
            "Agents assist with individual tasks but humans handle all handoffs",
            "Agents create pull requests with generated descriptions; agents observe CI results",
            "Agents are fully embedded: create PRs, post review comments, monitor CI, trigger and observe deployments",
        ],
    },
    {
        "id": "A6",
        "name": "Autonomous Operation",
        "note": None,
        "levels": [
            "Agents are always manually started by a developer; no automated triggering",
            "Agents are occasionally triggered by events but are mostly started manually",
            "Agents are systematically event-triggered for common workflows (push hooks, PR events, failing monitors)",
            "A continuous agent pipeline pulls from the backlog and implements stories on a schedule, with no per-story human initiation",
        ],
    },
    {
        "id": "A7",
        "name": "Proactive Quality Management",
        "note": None,
        "levels": [
            "No proactive quality management by agents; quality work is entirely human-initiated",
            "Agents run quality checks (security scans, dependency audits) when explicitly asked",
            "Agents automatically flag or report tech debt, security issues, and dependency updates (but do not open PRs to fix them)",
            "Agents proactively open PRs for tech debt reduction, dependency updates, security remediations, and standards enforcement",
        ],
    },
    {
        "id": "A8",
        "name": "Planning Integration",
        "note": None,
        "levels": [
            "Agents play no role in planning or requirements; all planning is done by humans",
            "Agents assist with planning when explicitly prompted",
            "Agents participate in story generation or decomposition as a configured step in the planning workflow",
            "Agents automatically generate, refine, and decompose stories from high-level goals without human initiation",
        ],
    },
]

# ── Thresholds ────────────────────────────────────────────────────────────────

READINESS_THRESHOLDS = {
    1: {"C1.1": 1, "C2.1": 1, "C5.1": 1, "C5.2": 1},
    2: {"C1.1": 2, "C2.1": 2, "C3.1": 1, "C4.1": 1, "C5.1": 2, "C5.2": 2,
        "C5.3": 1, "C6.1": 1, "C8.1": 1},
    3: {"C1.1": 2, "C2.1": 3, "C3.1": 3, "C4.1": 3, "C5.1": 2, "C5.2": 3,
        "C5.3": 2, "C6.1": 2, "C7.1": 2, "C8.1": 3, "C8.2": 2},
}

ADOPTION_THRESHOLDS = {
    1: {"A1": 1, "A2": 1, "A4": 1},
    2: {"A1": 2, "A2": 2, "A3": 2, "A4": 2, "A5": 1},
    3: {"A1": 3, "A2": 3, "A3": 2, "A4": 3, "A5": 3, "A6": 3},
    4: {"A1": 3, "A2": 3, "A3": 3, "A4": 3, "A5": 3, "A6": 3, "A7": 3, "A8": 2},
}

READINESS_NAMES = {
    0: "Uninstrumented",
    1: "Foundation",
    2: "Guided Autonomy",
    3: "Supervised Autonomy",
}

ADOPTION_NAMES = {
    0: "Unassisted",
    1: "Vibe Coding",
    2: "Agentic Engineering",
    3: "Software Factory",
    4: "Sustainable Autonomy",
}

# Minimum readiness level recommended for each adoption level
RECOMMENDED_READINESS = {0: 0, 1: 1, 2: 2, 3: 3, 4: 3}

# ── Helpers ───────────────────────────────────────────────────────────────────

W = 64


def hr(char="─"):
    return char * W


def ask(criterion):
    cid = criterion["id"]
    name = criterion["name"]
    note = criterion["note"]
    descriptions = criterion["levels"]
    max_level = len(descriptions) - 1

    print(f"\n{hr()}")
    print(f"  {cid} — {name}")
    if note:
        print(f"  Note: {note}")
    print(hr("·"))
    for i, desc in enumerate(descriptions):
        print(f"  {i}  {desc}")

    while True:
        try:
            raw = input(f"\n  Your level [0–{max_level}]: ").strip()
            val = int(raw)
            if 0 <= val <= max_level:
                return val
        except (ValueError, KeyboardInterrupt, EOFError):
            print("\nQuiz cancelled.")
            sys.exit(0)
        print(f"  Please enter a number between 0 and {max_level}.")


def compute_level(scores, thresholds):
    """Return (level_achieved, gaps_for_next_level_or_empty)."""
    level = 0
    for lvl in sorted(thresholds.keys()):
        if all(scores.get(c, 0) >= req for c, req in thresholds[lvl].items()):
            level = lvl
        else:
            gaps = {
                c: (req, scores.get(c, 0))
                for c, req in thresholds[lvl].items()
                if scores.get(c, 0) < req
            }
            return level, gaps
    return level, {}

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(hr("═"))
    print("  Agentic Coding Maturity Quiz")
    print("  Agent Readiness & Adoption Models")
    print(hr("═"))
    print("""
For each criterion, select the level that best describes your
project today. Be honest — this is for your own assessment.
Press Ctrl-C at any time to quit.
""")

    # Part 1: Readiness
    print(f"\n{hr('═')}")
    print("  PART 1: Agent Readiness")
    print("  How ready is your project's structure for agentic coding?")
    print(hr("═"))

    readiness_scores = {}
    for c in READINESS_CRITERIA:
        readiness_scores[c["id"]] = ask(c)

    # Part 2: Adoption
    print(f"\n\n{hr('═')}")
    print("  PART 2: Agent Adoption")
    print("  To what degree are agents embedded in your workflow?")
    print(hr("═"))

    adoption_scores = {}
    for c in ADOPTION_CRITERIA:
        adoption_scores[c["id"]] = ask(c)

    # ── Results ──────────────────────────────────────────────────────────────

    r_level, r_gaps = compute_level(readiness_scores, READINESS_THRESHOLDS)
    a_level, a_gaps = compute_level(adoption_scores, ADOPTION_THRESHOLDS)
    r_name = READINESS_NAMES[r_level]
    a_name = ADOPTION_NAMES[a_level]

    r_map = {c["id"]: c["name"] for c in READINESS_CRITERIA}
    a_map = {c["id"]: c["name"] for c in ADOPTION_CRITERIA}

    print(f"\n\n{hr('═')}")
    print("  RESULTS")
    print(hr("═"))
    print(f"\n  Readiness : Level {r_level} — {r_name}")
    print(f"  Adoption  : Level {a_level} — {a_name}")

    if r_gaps:
        r_next = r_level + 1
        print(f"\n  To reach Readiness Level {r_next} ({READINESS_NAMES[r_next]}), improve:")
        for cid, (req, cur) in sorted(r_gaps.items()):
            print(f"    • {cid} {r_map[cid]}: currently {cur}, need {req}")
    else:
        print("\n  Readiness: maximum level reached.")

    if a_gaps:
        a_next = a_level + 1
        print(f"\n  To reach Adoption Level {a_next} ({ADOPTION_NAMES[a_next]}), improve:")
        for cid, (req, cur) in sorted(a_gaps.items()):
            print(f"    • {cid} {a_map[cid]}: currently {cur}, need {req}")
    else:
        print("  Adoption: maximum level reached.")

    # Readiness-adoption compatibility
    rec = RECOMMENDED_READINESS[a_level]
    print(f"\n  Readiness–Adoption Compatibility")
    if r_level < rec:
        print(f"    ⚠  Adoption Level {a_level} ({a_name}) works best with")
        print(f"       Readiness Level {rec} ({READINESS_NAMES[rec]}) or higher.")
        print(f"       Your readiness ({r_level} — {r_name}) may limit")
        print(f"       the reliability and benefit of agent adoption.")
    else:
        print(f"    ✓  Your readiness (Level {r_level}) supports your")
        print(f"       adoption level (Level {a_level}) well.")

    print(f"\n{hr('═')}\n")


if __name__ == "__main__":
    main()
