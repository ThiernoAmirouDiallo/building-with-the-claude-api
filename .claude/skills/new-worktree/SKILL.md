---
name: new-worktree
description: Create an isolated git worktree and feature branch for new work. Use when the user wants to start a new feature, work on something in parallel, or asks for a worktree.
---

# Create a feature worktree

1. Get the feature name. If the user didn't give one, ask for it with AskUserQuestion. The `feature/` prefix is added automatically, so `login-page` becomes the branch `feature/login-page`.
2. Run the script from the repo root, passing the name (and a base branch only if the user asked for one other than `master`):

   ```bash
   bash .claude/skills/new-worktree/create-worktree.sh "<feature-name>"
   ```

   It creates the worktree at `.worktrees/<feature-name>/`, copies `.env`, and runs `uv sync` to build a separate `.venv`.
3. Report the worktree path and the branch, and show `git worktree list`.
4. Do not commit or push. Tell the user to `cd` into the path and start `claude` there to work on the branch.

If the script refuses (branch or path already exists, invalid name), show its message and ask for a different name.
