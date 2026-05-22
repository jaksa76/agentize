---
name: do-next-task
description: Pick the top task from TODO.md, implement it fully, commit and push to git, then mark it complete. Use when you want to work on the next item in the project task list.
allowed-tools: Read Write Edit Bash
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

## Next task to implement

The top task in TODO.md is:

!`head -1 TODO.md`

## Full TODO list (for context)

!`cat TODO.md`

## Instructions

Use a subagent to implement the task. Follow the steps outlined in the "Follow these steps exactly" section below.

Follow these steps exactly:

1. **Read the top task** — it is shown above. Understand what needs to be done.

2. **Read relevant project files** for context before implementing:
   - Read VISION.md, CLAUDE.md (if present), and any files directly relevant to the task.

3. **Implement the task fully** — do not cut corners. Make all necessary file changes.

4. **Mark the task complete** in TODO.md — remove the first line (the task you just completed) from TODO.md. Do not add it back as "done"; just delete it so the next task becomes the new top.

5. **Stage and commit the implementation**:
   - Stage only the files changed for this task (including the TODO.md).
   - Write a concise commit message that describes what was done.

6. **Push to remote** — run `git push`. If no remote is configured, skip this step and note it.

7. **Report** what was implemented and which files were changed.
