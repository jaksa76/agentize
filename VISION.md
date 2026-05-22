This project is focused on creating maturity models for evaluating the readiness and adoption of agentic coding in software projects. The goal is to provide a framework for categorising projects based on their preparedness for agentic coding and their level of adoption of this approach.

# 1. Agent Readiness Maturity Model

## Why a Readiness Model

Applying agentic coding to a project can have very different outcomes. It tends to emphasise all good and all bad aspects of that project. Depending on how the project is set up, agentic coding can be a productivity booster or an agent of chaos.

## Levels

We will create a maturity model for evaluating Agentic Coding Readiness. This will allow us to categorise projects into different tiers in terms of how ready a project is. For example

- Level 0 - very little or no benefit from applying agents, agents have no context or feedback mechanism
- Level 1 - agents would be able to perform small steps, but humans needs to micromanage; agents have some feedback (e.g. compilation, unit tests)
- Level 2 - humans still guide but agents now have context to perform larger steps (plan a story, write tests, etc.)
- Level 3 - humans provide oversight, agents have full context and strong feedback loops (e2e tests, screenshots) and can autonomously implement most stories

## Project Features

In order to categorise a project into the appropriate level we will perform a series of checks. For example:

- is the entirety of code accessible (monorepo, git modules, multi-repo)
- reproducible dev env (devcontainers, setup script, setup instructions, none)
- requrements overview documentation (in repository, via MCP server)
- C0 system context architecture documentation (in repository, via MCP server)
- C1 container level architecture documentation (in repository, via MCP server)
- C2 component level architecture documentation (in repository, hierarchical)
- critical flows documentation (hierarchical)
- automated test presence
- unit test coverage > 80%
- e2e testing (including UI if present)
- people preparedness
- ability to test integration with 3rd parties
- reproducible data (database)
- access to requirements (discovery)
- ability to stakeholders (product owners)
- tooling compatibililty (IDE)
- automated deployment

## Automatic verification

To automate the verification of the project features through the use of agents. We will create a set of skills that can be used by an agent like Claude Code. Using these skills, the agent will clone the repository and verify features in order, determining the agent readiness level of the project.

## Automatic enablement

Additionally we will develop a set of skills that automatically improve the agentic readiness of the project. For example, if the project does not have a reproducible dev environment, the agent can create a devcontainer configuration based on the project structure and dependencies. If the project does not have automated tests, the agent can create unit tests based on the code. If the project does not have architecture documentation, the agent can generate it based on the codebase.

# 2. Agent Adoption Maturity Model

Create a set of skills to evaluate agentic coding adoption

Like for readiness, we can automate adoption level evalution

## Example levels:

- Level 0: no vibe coding
- Level 1 (vibe coding): agent assists humans
- Level 2 (agentic engineering): agents can fully implement most user stories
- Level 3 (software factories): workers continuously pull stories from task mgt
- Level 4 (sustainable): automated tech debt mgt, security reviews

## Bonus Levels

- automated fixing of production issues
- automated user story generation
- automated project management

## Automated verification and enablement

Similar to the readiness model, we can create a set of skills that can be used by an agent to evaluate the adoption level of a project. The agent can check for the presence of agents in the development process, the extent to which they are used, and the impact they have on productivity and quality.

---

*Copyright (c) 2026 Codomain D.O.O. All rights reserved. Licensed under [CC BY-NC 4.0](LICENSE.md). Licensed clients may use and modify this material for internal business purposes.*
