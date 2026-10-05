---
description: Create a git worktree and feature/<name> branch for parallel work
argument-hint: [feature-name]
allowed-tools: Bash(bash .claude/skills/new-worktree/create-worktree.sh:*), Bash(git worktree list:*)
---

Create a new git worktree for a feature branch.

Feature name from the user: `$ARGUMENTS`

If that is empty, ask the user for the feature name with AskUserQuestion first. The `feature/` prefix is added automatically.

Then run, from the repo root:

```bash
bash .claude/skills/new-worktree/create-worktree.sh "<feature-name>"
```

Report the worktree path and branch, then run `git worktree list`. Do not commit or push. If the script refuses (branch or path already exists, invalid name), show its message and ask for a different name.
