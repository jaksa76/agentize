---
name: improve-c2-1
description: Improve readiness criterion C2.1 (Setup Automation) in the current project by adding or upgrading setup automation. Raises the fulfillment level by one step.
allowed-tools: Bash Read Write Edit
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Improve C2.1 — Setup Automation

## Levels

| Level | Description |
|-------|-------------|
| 0 | No setup instructions anywhere |
| 1 | Written instructions exist in README but no automation script |
| 2 | A setup script (setup.sh, Makefile target, or standard `npm install` / `pip install`) installs everything with one command |
| 3 | A containerised/declarative environment exists (.devcontainer, Nix, etc.) |

This skill raises the fulfillment level by **one step**.

## Current State

Examine the project to understand its current state:

- Check for a containerised or declarative environment (`.devcontainer/devcontainer.json`, `flake.nix`, `shell.nix`, `.gitpod.yml`).
- Look for setup or install scripts and relevant Makefile targets.
- Identify the dependency manager and installation command from the build manifest.
- Read the README setup section to understand the current manual steps required.
- Identify the project's **canonical build command** and **canonical test command** — they are needed to validate a devcontainer at Level 3.

---

## Instructions

### Step 1 — Determine the current level

Score the project 0–3 against the table above, then implement the single step to the next level.

**If already at level 3**, report that C2.1 is at its maximum level and no improvement is needed, and stop.

---

### Step 2 — Implement the improvement

#### If current level is 0 → raise to 1

Add a "Getting Started" section to `README.md` (create the file if missing) with step-by-step instructions for setting up the development environment. Include: prerequisites and their versions, dependency installation commands, environment variable setup, and how to verify the setup works.

Derive every step from the actual project — the real dependency manager, the real commands, the real env vars. Do not write generic placeholders.

#### If current level is 1 → raise to 2

Create a `setup.sh` script at the project root that automates all the steps described in the README. Detect the language and package manager from the evidence above and write an appropriate script:

- **Node.js** — install the node version if `.nvmrc` exists, run `npm ci` (or the lockfile's matching command), copy `.env.example` to `.env` if present
- **Python** — create a virtualenv, install from `requirements.txt` or `pyproject.toml`, install pre-commit hooks if configured
- **Java/Gradle** — run `./gradlew dependencies` (Maven: `./mvnw dependency:go-offline`)
- **Go** — run `go mod download`

Make it executable (`chmod +x setup.sh`) and add a note to the README to run `./setup.sh`.

Run the script on a clean checkout to confirm it completes, and report the result.

#### If current level is 2 → raise to 3

Create a `.devcontainer/devcontainer.json` and **validate it by actually building and running the project inside it**. Follow Step 3 below.

---

### Step 3 — Devcontainer creation and validation (level 2 → 3 only)

#### 3a. Docker preflight

Before creating or validating a devcontainer, confirm the container runtime is usable:

- Check Docker is installed: `docker --version`.
- Check the daemon is reachable: `docker version --format '{{.Server.Version}}'` or `docker info`.

If Docker is not installed, or the daemon is unreachable or hangs, **stop and report an external blocker.** Do not write or keep revising a `devcontainer.json` that cannot be validated — an unvalidated devcontainer is not evidence of Level 3. Say plainly that Docker is the blocker and what the user needs to do.

Also check whether the `devcontainer` CLI is available (`devcontainer --version`); if it is missing, install it (`npm install -g @devcontainers/cli`) or note it as a blocker if installation is not possible.

#### 3b. Validation loop

Run the following loop. It exits when `devcontainer up` succeeds, the project builds, and the project tests run (even if some tests fail) — or when a blocker outside the devcontainer configuration is confirmed.

**Assess** — read the repo for:
- Primary language and runtime version (`package.json`, `pom.xml`, `build.gradle`, `requirements.txt`, `go.mod`)
- Existing setup scripts or Makefile targets to wire into `postCreateCommand`
- Server ports exposed (`package.json` scripts, `Procfile`, `application.properties`)
- The canonical build command and canonical test command

**Write or revise `.devcontainer/devcontainer.json`** with:
- The correct Microsoft devcontainer base image for the detected language and version
- Any devcontainer features needed (Docker-in-Docker, aws-cli, Playwright, sbt, terraform)
- A `postCreateCommand` that runs the existing setup script or installs dependencies
- VS Code extensions appropriate for the detected language
- `forwardPorts` for any detected server port

Use real values derived from the project. Do not write generic placeholders.

**Bring it up:**

```bash
devcontainer up --workspace-folder <repo-path> --remove-existing-container
```

Capture the full output.

**Evaluate:**

- **`devcontainer up` failed** → read the error, identify the configuration mistake, revise `devcontainer.json`, and restart the loop.
- **`devcontainer up` succeeded** → run the project's real build and test commands inside the container:
  ```bash
  devcontainer exec --workspace-folder <repo-path> <build-command>
  devcontainer exec --workspace-folder <repo-path> <test-command>
  ```
  Use the project's actual commands, not a generic stand-in.

**Fallback when `exec` cannot attach.** If `devcontainer up` succeeded but `devcontainer exec` cannot find or attach to the container, do not treat that alone as a failure. Validate through the built image instead:
- identify the image `devcontainer up` produced (`docker images`, or the image referenced by the created container)
- run the same dependency install, build command, and test command in that image with the repository mounted at the expected workspace path, for example:
  ```bash
  docker run --rm -v <repo-path>:/workspaces/<repo-name> -w /workspaces/<repo-name> <image> bash -lc '<build-command>'
  ```
- use that result as the loop's validation result, and record that the fallback path was used

#### 3c. Classify every failure

Before revising anything, decide which kind of failure you are looking at:

- **Configuration failure** — a missing tool, wrong runtime version, missing devcontainer feature, or an env var the container should provide. This is fixable here: revise `devcontainer.json` and restart the loop.
- **External blocker** — unavailable secrets or credentials, a network restriction, an unreachable external service, or an integration test that requires infrastructure that does not exist in this environment. This is **not** a devcontainer defect. Note it, stop iterating on it, and report it.

A build that succeeds and tests that run but fail on their own merits count as a successful validation of the devcontainer: the environment did its job. Report the test failures separately from the C2.1 outcome.

---

## Report

State:

- **Before level** and **after level**
- **Files created or modified**
- For a level 2 → 3 improvement:
  - **Docker preflight** — whether Docker was installed and the daemon reachable
  - **`devcontainer up`** — whether it succeeded, and how many revision iterations were needed
  - **Validation method** — `devcontainer exec` or the fallback image-run path
  - **Build outcome** — the command run and its result
  - **Test outcome** — the command run, its result, and any failures, each classified as a configuration failure or an external blocker
- **Any external blockers** that prevented full validation, and what the user needs to do about them
