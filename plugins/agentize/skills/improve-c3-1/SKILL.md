---
name: improve-c3-1
description: Improve readiness criterion C3.1 (Architecture Depth) in the current project by generating architecture and design documentation.
allowed-tools: Bash Read Write Edit
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Improve C3.1 — Architecture Depth

Preparation: Determine if this is a monolith project or a microservice/multirepo setup.

## Writing Documentation for a Monolith

- where appropriate, divide the work into subagents to reduce context load and parallelize tasks.

Step 1: Analyse the sources
    
- examine the dependencies of the application (e.g., package.json, requirements.txt, go.mod, etc.)
- for each source file, identify its purpose and relationships, use of external libraries/systems/APIs.

Step 2: Identify entry points

- identify all entry points of the application (e.g., APIs, other triggers, background jobs).
- if the application has a user interface, identify user operations and how they map to entry points.
- if the application is a web application, identify the main routes and how they map to entry points.

Step 3: Identify main flows

- identify which components are involved in each main flow.

Step 4: Analyse the database schema

- identify the main entities and their relationships.

Step 5: Find any noteworthy architectural patterns or decisions

- identify any non-standard design patterns used in the application
- note any significant architectural decisions, such as choice of frameworks, libraries, or infrastructure components.

Step 6: Write the design documentation.

- if there is existing design documentation, update it with the new findings. Otherwise, create a new design document in `docs/DESIGN.md`.
- the design document should have:
  - a high level introduction (100 words)
  - a list of entry points (API endpoints, background jobs, etc.) (1 line per entry point)
  - a description of the main flows (1 paragraph per flow)
  - an overview of the database schema (only main entities and relationships)
  - an index of source files and their purposes (1 line per source file)
  - any third-party systems used
  - any noteworthy architectural patterns or decisions

Step 7: Write the architecture documentation.

- if there is existing architecture documentation, update it with the new findings. Otherwise, create a new architecture document in `docs/ARCHITECTURE.md`.
- the architecture document should have:
  - a high-level system context (users, actors, external systems)
  - an overview of major components and their interactions
  - critical flows (sequence diagrams or step descriptions)
  - any noteworthy architectural patterns or decisions

Step 8: Update README.md, CLAUDE.md and other entry point documentation.

- if there are existing README.md, CLAUDE.md, or other entry point documentation, add references to the new documentation.
- ensure that any instructions or descriptions in these files are consistent with the latest architecture and design decisions.



## Writing Documentation for a Microservice/Multirepo

- use subagents where appropriate to reduce context load and parallelize tasks.
- the architecture document should live in `docs/ARCHITECTURE.md` in either the root of the main repository (if monorepo), a designated documentation directory or a "main" repository of the system.
- if it is an interactive session, ask the user where to place the architecture documentation.
- the design documentation should either live in `docs/DESIGN.md` in the root of the respective repository or a designated documentation repo (e.g. 'docs/<service>_DESIGN.md').
- if it is an interactive session, ask the user where to place the design documentation.

Step 1: Document each microservice or repository individually.

- follow a process similar to the one for a monolith for each service or repository.
- produce a separate design documents for each microservice or repository.

Step 2: Document the overall architecture of the system.

- produce a single architecture document that integrates the architecture of all microservices or repositories.
- the architecture document should contain:
  - a high-level system context (users, actors, external systems)
  - an overview of major services and their interactions (pointing to the relevant design documentation)
  - critical flows (sequence diagrams or step descriptions)
  - any noteworthy architectural patterns or decisions