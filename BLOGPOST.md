# Your Team Is Using AI Agents Wrong — Here's a Framework to Fix That

Most engineering teams I talk to have the same story: a handful of developers are using Copilot or Claude daily, a few more experiment occasionally, and the rest are skeptical. But even the enthusiastic adopters are usually doing something more modest than they realize — using agents as glorified autocomplete rather than as autonomous implementers. Meanwhile, the question no one on the team has actually sat down to answer is: is this codebase even structurally ready for agents to do more?

That gap — between "we use AI tools" and "we get systematic, reliable value from agents" — is what I've been trying to close. The result is Agentize, an open-source framework with two complementary maturity models and a full suite of Claude Code skills to assess and raise both dimensions.

---

## Two Things Have to Change Together

Here's the core insight the framework is built around: for agentic coding to deliver on its promise, two things have to happen simultaneously, and they almost never do.

First, the project needs to be structurally ready. This means conventions are documented somewhere an agent can find them, tests exist and cover enough ground to catch regressions, CI is wired up and queryable, architecture documentation lives in the repository rather than in someone's head. These are properties of the codebase and tooling — not developer behavior.

Second, the team needs to have actually changed how they work. Not "we added Copilot to our IDEs" but "we assign whole user stories to agents and review the resulting diff." The behavioral shift is often harder than the technical one. It requires trusting agents to run their own feedback loops, accepting that reviewing a completed diff is a legitimate engineering contribution, and letting agents fail and self-correct rather than micromanaging every step.

Most teams optimize one without the other. I've seen beautifully instrumented codebases — CLAUDE.md written, tests at 85% coverage, devcontainer configured — where agents are still used only for autocomplete because the team never changed their habits. I've also seen teams enthusiastically assigning full stories to agents on codebases with no tests, no documentation, and no CI — and getting output that breaks in ways that take hours to debug. The framework addresses both dimensions with distinct models.

---

## The Readiness Model: Is Your Codebase Agent-Ready?

The Agent Readiness Maturity Model measures structural, environmental, and documentary properties of a codebase — the things that determine whether an agent can understand, navigate, modify, and verify the project effectively. It has four levels.

**Level 0 — Uninstrumented.** The agent has nothing to work with. No documentation beyond scattered inline comments, no tests, no reproducible development environment. Applying agents here produces little benefit and real risk: regressions are invisible, the agent cannot verify its own output, and the context it needs is locked in people's heads.

**Level 1 — Foundation.** The project has enough structure for small, targeted steps, but every step requires human micromanagement. The build succeeds, a handful of unit tests exist, a README describes what the system does. An agent can make a change and confirm it compiles, but a human has to review every output and provide explicit context for every decision.

**Level 2 — Guided Autonomy.** Humans guide at the story or feature level rather than step by step. Agents have enough context to plan implementations, write tests, and navigate architecture. This typically means: a CLAUDE.md with project conventions and navigation guidance, an automated setup script (or devcontainer), architecture documentation covering at least the system context, 50%+ unit test coverage, integration tests at key service boundaries, linting configured, and read-only CI access so the agent can observe its own pipeline results.

**Level 3 — Supervised Autonomy.** Humans operate at a strategic level — defining goals, reviewing outcomes, handling exceptions. Agents can implement most stories end-to-end. This requires a fully containerized development environment, component-level architecture documentation including critical flows, 80%+ unit test coverage plus E2E tests, type checking on top of linting, reproducible database state for data-path testing, full CI/CD pipeline control including deployment triggers, and queryable observability so agents can verify production behavior after deploying.

What makes the model useful in practice is that it's scored across 11 specific criteria across 8 groups — codebase accessibility, setup automation, architecture depth, requirements access, runnability, unit test coverage, integration and E2E coverage, static analysis, test isolation, CI/CD automation, and observability. Each criterion has 2–4 fulfillment levels. The overall readiness level is the highest level at which *all* required criteria are met. This means you can identify exactly which criterion is dragging your level down, rather than getting a vague "you need to improve your testing."

The key insight the model encodes: agents amplify what's already there. A codebase with good tests and documented conventions lets an agent work autonomously and catch its own mistakes. A codebase without them produces agent output that breaks things in ways that are hard to detect, because there's nothing to catch the regressions and nothing for the agent to use as a reference for what the system is supposed to do.

---

## The Adoption Model: How Are You Actually Using Agents?

The Agent Adoption Maturity Model measures behavioral dimensions — not whether agents are installed, but how deeply they're embedded in how the team actually works. It has five levels.

**Level 0 — Unassisted.** Agents play no meaningful role. Individual developers might occasionally ask a chatbot a question, but there's no systematic use, no agent-authored code in git history, no tooling configured in the repository.

**Level 1 — Vibe Coding.** This is where most teams currently sit. Developers use agents as interactive assistants — autocomplete, code generation, explaining errors, generating tests for specific functions. The human remains the author; the agent is a smart tool. Every line of agent output is reviewed before acceptance. No agent autonomously runs tools, executes tests, or makes multi-file changes. The term "vibe coding" is sometimes used pejoratively, but it's a real and valid starting point — it's just not the productivity transformation that the hype promises.

**Level 2 — Agentic Engineering.** This is the jump most teams are trying to make, and the hardest. Agents plan and implement complete features or user stories. The developer provides high-level direction — "implement the password reset flow per the spec in STORIES.md" — and reviews the resulting diff rather than directing every step. Agents run their own feedback loops: they write tests, run them, fix failures, and present only passing results. The defining behavioral difference from Level 1 is self-verification. Without it, "assigning a story" is just a longer prompt — the human still closes all the loops.

The practical requirements for Level 2 are tightly tied to the readiness model: you need CLAUDE.md or AGENTS.md with project-specific guidance (conventions, architecture overview, key commands), regular agent contributions accounting for at least 25% of recent changes, agents that run the full test suite and iterate on failures before presenting results, and agents handling multi-file feature implementations rather than single-function edits.

**Level 3 — Software Factory.** Agents continuously pull stories from the backlog and implement them with minimal per-story human involvement. The team's role shifts from writing code to defining requirements, reviewing agent PRs, and handling exceptions. Multiple agents may work in parallel. The distinguishing characteristic is autonomous operation: a continuous pipeline that pulls from the backlog on a schedule, without a human initiating each story. This requires comprehensive agent context (including MCP servers that expose requirements and runbooks, not just a static CLAUDE.md), agents creating full pull requests including cross-service changes and migration scripts, agents fully embedded in PR creation, CI monitoring, and deployment workflows, and — critically — that continuous pipeline for backlog processing.

**Level 4 — Sustainable Autonomy.** The system self-sustains over time. Agents proactively open PRs for tech debt reduction, dependency updates, and security remediations — without anyone asking. Production incidents trigger automated diagnosis and, where safe, remediation. Agents participate in story generation and backlog grooming, reducing the manual overhead of feeding the factory. Most teams won't need this level; the few that do are effectively running software organizations with minimal human implementation overhead.

---

## How to Use the Framework

The framework is designed to be immediately actionable. There are three entry points.

**The quiz.** If you want a quick baseline before committing to a deeper assessment, run `python3 quiz.py` from the repository root. It walks through both models with multiple-choice questions and gives you a rough level for each. This takes about five minutes and is a reasonable starting point for a team conversation.

**The assessment skills.** For a detailed, evidence-based scoring with per-criterion analysis, open any software project in Claude Code and run `/assess-readiness` or `/assess-adoption`. These skills inspect the actual codebase — checking for the presence and content of CLAUDE.md, examining test files and coverage configuration, reading CI pipeline definitions, looking at git history for agent-authored commits — and produce a structured report with your achieved level, per-criterion scores, and a prioritized list of what's blocking the next level. Individual criteria can be verified in isolation with skills like `/verify-c5-2` (unit test coverage) or `/verify-a3` (feedback loop closure).

**The improvement skills.** Once you know your gaps, the framework can close them. `/improve-readiness` identifies every criterion blocking the next level and implements the improvements — generating architecture documentation from the codebase, creating a CLAUDE.md with observed conventions, setting up a devcontainer based on the project's dependency structure, adding CI workflow definitions. `/improve-adoption` does the analogous work on the behavioral side: creating agent context files, setting up workflow integration, configuring event-triggered agent pipelines.

Individual criteria can be improved one at a time with skills like `/improve-c3-1` (architecture depth) or `/improve-a5` (workflow integration). The natural workflow is: assess, identify your lowest-scoring criterion blocking the next level, improve that criterion, reassess. One level at a time is deliberate — jumping two levels at once tends to produce changes that are technically present but not operationally embedded.

---

## What the Framework Cannot Tell You

Two important limitations to be honest about.

The framework measures structural properties and behavioral patterns, not output quality. An agent that reliably passes tests can still produce bad code — over-engineered, hard to maintain, subtly wrong in ways that tests don't cover. The readiness model captures the feedback signals available to an agent; it does not guarantee the agent uses them well. Similarly, the adoption model measures *what* agents do and *how autonomously* they operate, not the quality of individual outputs. Teams should separately track agent error rates, PR rejection rates, and code review findings to calibrate their trust.

The framework also can't account for team and organizational dynamics. A high-readiness, high-adoption project where the team rubber-stamps agent PRs without meaningful review is worse than a lower-adoption team that reviews carefully. The adoption criteria for workflow integration (A5) and feedback loop closure (A3) create structural pressure toward review quality, but they don't measure whether reviews are actually substantive. How much to trust agent output without review is a judgment call that depends on the specific domain, the criticality of the system, the maturity of your test coverage, and accumulated experience with your particular agents on your particular codebase. The framework can tell you when the structural conditions for higher trust are met; it cannot tell you that the trust is warranted.

---

## Where to Start

If any of this resonates, the repository is at [github.com/jaksa76/agentize](https://github.com/jaksa76/agentize). Clone it, run `python3 quiz.py` against your current project (or just answer the questions in your head), and see where you land.

My suggestion for most teams currently at Adoption Level 1: don't try to jump to Level 3. Focus first on getting to Level 2 — assign one story to an agent and review the diff rather than directing every step. That single behavioral shift, done consistently, produces more value than any number of tooling improvements. The readiness improvements that matter most for enabling it are CLAUDE.md (so the agent has project context) and enough test coverage to close the feedback loop (so the agent can verify its own work).

The framework won't tell you what your team should aspire to. Some teams have good reasons to stay at Level 1 — high-stakes domains, regulatory constraints, team size, risk tolerance. Others have the right conditions for Level 3 and are leaving real leverage on the table. What the framework can do is tell you exactly where you are, exactly what's in the way of the next level, and give you tools to remove those blockers systematically.

That clarity, at least, seems worth having.
