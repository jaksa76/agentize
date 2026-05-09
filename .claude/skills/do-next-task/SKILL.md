---
name: do-next-task
description: Pick the top task from TODO.md, implement it fully, commit and push to git, then mark it complete. Use when you want to work on the next item in the project task list.
disable-model-invocation: true
allowed-tools: Read Write Edit Bash
---

## Next task to implement

The top task in TODO.md is:

!`head -1 TODO.md`

## Full TODO list (for context)

!`cat TODO.md`

## Instructions

Follow these steps exactly:

1. **Read the top task** — it is shown above. Understand what needs to be done.

2. **Read relevant project files** for context before implementing:
   - Read VISION.md, CLAUDE.md (if present), and any files directly relevant to the task.

3. **Implement the task fully** — do not cut corners. Make all necessary file changes.

4. **Ensure git is initialized** — if the working directory is not a git repo, run `git init && git add -A && git commit -m "initial commit"` first.

5. **Stage and commit the implementation**:
   - Stage only the files changed for this task (not TODO.md yet).
   - Write a commit message that describes what was done, ending with:
     `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>`

6. **Push to remote** — run `git push`. If no remote is configured, skip this step and note it.

7. **Mark the task complete** in TODO.md — remove the first line (the task you just completed) from TODO.md. Do not add it back as "done"; just delete it so the next task becomes the new top.

8. **Commit the TODO.md update**:
   ```
   git add TODO.md
   git commit -m "mark task complete: <short task description>"
   ```
   Then push: `git push` (skip if no remote).

9. **Report** what was implemented and which files were changed.
