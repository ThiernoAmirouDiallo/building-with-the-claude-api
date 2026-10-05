#!/usr/bin/env bash
# Usage: create-worktree.sh <feature-name> [base-branch]
# Creates branch feature/<feature-name> in a new worktree at .worktrees/<feature-name>.
set -euo pipefail

if [ $# -lt 1 ] || [ -z "${1// /}" ]; then
    echo "Usage: $0 <feature-name> [base-branch]" >&2
    exit 1
fi

name="${1#feature/}"
base="${2:-master}"
branch="feature/$name"
slug="${name//\//-}"

# Resolve the main repo root even when run from inside another worktree.
main_root="$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")"
path="$main_root/.worktrees/$slug"

if ! git check-ref-format --branch "$branch" >/dev/null 2>&1; then
    echo "Invalid branch name: $branch" >&2
    exit 1
fi

if git -C "$main_root" show-ref --verify --quiet "refs/heads/$branch"; then
    echo "Branch $branch already exists." >&2
    exit 1
fi

if [ -e "$path" ]; then
    echo "Worktree path already exists: $path" >&2
    exit 1
fi

git -C "$main_root" worktree add -b "$branch" "$path" "$base"

# .env is gitignored, so a new worktree doesn't get it.
if [ -f "$main_root/.env" ]; then
    cp "$main_root/.env" "$path/.env"
    echo "Copied .env (contains secrets; it is gitignored)."
fi

# A copied .venv would still point at the main repo, so build a fresh one.
(cd "$path" && uv sync)

echo
echo "Worktree ready: $path"
echo "Branch:         $branch (from $base)"
echo "Next:           cd \"$path\" && claude"
