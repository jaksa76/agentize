# Agentize

Skills for helping you adopt agentic coding.

---

## Installation

```
/plugin marketplace add jaksa76/agentize
/plugin install agentize@agentize
```


## Usage

To assess the agent readiness of your project:

```
/agentize:assess-readiness
```

to evaluate a single criterion:

```
/agentize:verify-c1-1
```

### Available criteria

| Command | Criterion |
|---------|-----------|
| `/agentize:verify-c1-1` | C1.1 — Codebase Accessibility |
| `/agentize:verify-c2-1` | C2.1 — DevEnv Setup Automation |
| `/agentize:verify-c3-1` | C3.1 — Documentation Depth |
| `/agentize:verify-c4-1` | C4.1 — Requirements Accessibility |
| `/agentize:verify-c5-1` | C5.1 — Runnability |
| `/agentize:verify-c5-2` | C5.2 — Unit Test Coverage |
| `/agentize:verify-c5-3` | C5.3 — Integration and E2E Test Maturity |
| `/agentize:verify-c6-1` | C6.1 — Coding Guidelines |
| `/agentize:verify-c7-1` | C7.1 — Test Isolation |
| `/agentize:verify-c8-1` | C8.1 — CI/CD Automation |
| `/agentize:verify-c8-2` | C8.2 — Observability |


## Additional Skills

Besides the Readiness assesment skills, this project contains additional skills for assessing the agentic adoption level and also skills to improve agent readiness and adoption levels by implementing the missing criteria. These additional skills are still under refinement and not yet documented, but you can already install them and use them in your projects.

**Personal install** (available in all your projects):

```bash
git clone https://github.com/jaksa76/agentize.git
cp -r agentize/.claude/skills/* ~/.claude/skills/
```

**Project install** (available in one project only):

```bash
cp -r agentize/.claude/skills/* /your/project/.claude/skills/
```

Once installed, you can invoke the skills directly:

```
/assess-adoption
/verify-adoption-c1-1
/improve-readiness-c1-1
```

## Theory

See [READINESS.md](READINESS.md) and [ADOPTION.md](ADOPTION.md) for the full maturity model specifications.
