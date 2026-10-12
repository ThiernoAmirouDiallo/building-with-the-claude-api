# Automating code review and PR work with Claude

Notes on three ways to get Claude to work on pull requests without me sitting in a terminal. I haven't turned any of them on for this repo yet, so this is how they work, not what I've set up.

| | Where it runs | Needs | Good for |
| --- | --- | --- | --- |
| [`/code-review`](#1-code-review-locally) | My machine | Claude Code | A check before I push |
| [Managed Code Review](#2-managed-code-review-claude-github-app) | Anthropic's cloud | Team or Enterprise plan | Every PR reviewed automatically |
| [Claude Code GitHub Action](#3-claude-code-github-action) | GitHub's runners | An API key or subscription token | `@claude` requests and my own automations |

Managed Code Review and the GitHub Action are separate products. Both use the same Claude GitHub App, but the Action is a workflow file in my repo that I control, and Code Review is a service I switch on in admin settings.

## 1. `/code-review` locally

Reviews a diff in the terminal, no GitHub App needed. It looks for correctness bugs and, depending on model and effort, also reuse, simplification and efficiency cleanups.

```text
/code-review
```

With no target it reviews my branch's commits ahead of upstream plus uncommitted changes. It runs as a background subagent, so it doesn't fill my conversation, and the findings come back when it's done.

Targets and flags:

| Usage | What it does |
| --- | --- |
| `/code-review 42` | Review PR number 42 (also takes a branch, a file path, or a range like `main...my-feature`) |
| `/code-review high` | Set the effort level: `low` (fewest, most confident findings) up to `max`. It reuses the last level I typed |
| `/code-review --fix` | Apply the findings to my working tree afterwards |
| `/code-review --comment` | Post the findings on the GitHub PR as inline comments |
| `/code-review ultra` | Deeper multi-agent review in the cloud (needs a claude.ai login) |
| `/code-review --max-findings all` | Report every finding instead of the usual limit |

Things to remember:

- `/review` is an alias.
- It follows `CLAUDE.md`, but it does **not** read `REVIEW.md` (that's only for managed Code Review).
- `--fix` edits aren't covered by `/rewind` when the review ran in the background, so undo them with git.
- Claude can also start it on its own if I ask for a review in plain words. To stop that and keep it manual, add this to `~/.claude/settings.json`:

```json
{
  "skillOverrides": {
    "code-review": "user-invocable-only"
  }
}
```

## 2. Managed Code Review (Claude GitHub App)

A service that reviews every pull request on Anthropic's infrastructure and posts the findings as inline comments. Several agents look at the diff in the context of the whole codebase, then a verification step checks each candidate against the real code to drop false positives.

**Availability.** Research preview, for Team and Enterprise plans only. Not available with Zero Data Retention or the HIPAA configuration. On a personal plan like mine I can't enable it, but I can still use `/code-review` above.

### Setup

An Owner of the Claude organization does this once:

1. Go to [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) and find the Code Review section. This needs the Owner role and permission to install GitHub Apps in the GitHub organization.
2. Click **Setup** and install the [Claude GitHub App](https://github.com/apps/claude) on the GitHub organization.
3. Pick which repositories it can access, then which ones get Code Review.
4. For each repo, set **Review Behavior**:
   - **Once after PR creation**: one review when the PR is opened or marked ready.
   - **After every push**: a review on each push, and threads get auto-resolved when the issue is fixed. Most thorough and most expensive.
   - **Manual**: nothing happens until someone comments.
5. Open a test PR. A check run called **Claude Code Review** should appear within a few minutes.

### Triggering by comment

Post these as a top-level PR comment (not on a diff line), at the start of the comment. I need write access, and the PR has to be open. They work in every mode and on draft PRs.

| Comment | Effect |
| --- | --- |
| `@claude review` | One review, no subscription to future pushes |
| `@claude review once` | Same as above |
| `@claude review always` | Review now and on every later push to that PR |

Forks are never reviewed automatically. Someone with write access to the base repo has to comment `@claude review`. If my GitHub organization membership is private, the command can be ignored unless I'm added as a direct collaborator.

### What comes back

- Inline comments on the lines with problems, plus a summary in the review body.
- Severity markers: 🔴 **Important** (fix before merging), 🟡 **Nit** (minor), 🟣 **Pre-existing** (a bug that was already there).
- A **Claude Code Review** check run with a table of all findings. It always ends *neutral*, so it never blocks a merge. To gate merges I'd have to read the severity counts from the check output in my own CI.
- 👍 / 👎 on each comment. Anthropic uses them to tune the reviewer. Replying to a comment doesn't make Claude respond; to dismiss one I resolve the thread.

### Tuning it: `CLAUDE.md` and `REVIEW.md`

- `CLAUDE.md`: general project rules. New violations are flagged as nits.
- `REVIEW.md` at the repo root: instructions only for reviews. It can change what counts as Important, cap the number of nits, list paths to skip (generated code, lockfiles), add checks that run on every PR, and say how the summary should look. Keep it short, since a long file dilutes the rules that matter.

A small example:

```markdown
# Review instructions

## What Important means here
Reserve Important for broken behavior, leaked data, or changes that block a rollback.
Style and naming are Nit at most.

## Cap the nits
Report at most five Nits. If there are more, say "plus N similar items" in the summary.

## Do not report
- Anything CI already enforces (lint, formatting)
- Generated files and lockfiles
```

### Cost

Billed by token usage through usage credits, separate from the plan's included usage. Reviews average about $15 to $25 each and take around 20 minutes. "After every push" multiplies that by the number of pushes, so Manual or Once is cheaper. A monthly spend cap can be set at [claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage), and spend shows up at [claude.ai/analytics/code-review](https://claude.ai/analytics/code-review).

If a review fails or times out, comment `@claude review` again or click **Re-run** on the check (re-run doesn't work on fork PRs).

## 3. Claude Code GitHub Action

[`anthropics/claude-code-action`](https://github.com/anthropics/claude-code-action) runs Claude Code inside my own GitHub workflows. It has two modes, picked automatically:

- **Interactive** (no `prompt` input): waits for `@claude` in a PR or issue comment, a PR review, or a new issue, then answers. This is the "tag Claude" mode.
- **Automation** (a `prompt` input): runs on whatever event I choose, without a mention. This is the "runs by itself" mode.

### Setup

**Quick:** open `claude` in the repo and run `/install-github-app`. It installs the GitHub App, saves the secret, and opens a PR with the workflow files. I merge that PR and `@claude` works. It needs the GitHub CLI (`gh auth login`), admin access to the repo, and a github.com repo.

**Manual:**

1. Install the [Claude GitHub App](https://github.com/apps/claude) on the repo.
2. Add one secret in the repo settings:
   - `ANTHROPIC_API_KEY`: an API key from the Claude Console, or
   - `CLAUDE_CODE_OAUTH_TOKEN`: a subscription token, made by running `claude setup-token` locally (Pro, Max, Team, Enterprise). Then use `claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}` instead of the `anthropic_api_key` line below.
3. Add a workflow file under `.github/workflows/`.

Never commit a key or token. It always goes in GitHub Secrets.

### Trigger 1: `@claude` mentions

`.github/workflows/claude.yml`:

```yaml
name: Claude Code
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
jobs:
  claude:
    if: contains(github.event.comment.body, '@claude')
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
      id-token: write
      actions: read
    steps:
      - uses: actions/checkout@v6
        with:
          fetch-depth: 1
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

What the odd lines are for: `id-token: write` is needed for the default GitHub App authentication, `actions: read` lets Claude read CI results, the `if` stops runners starting on comments that don't mention Claude, and `actions/checkout` gives Claude a copy of the repo.

Then in any issue or PR comment:

```text
@claude implement this feature based on the issue description
@claude how should I implement user authentication for this endpoint?
@claude fix the TypeError in the user dashboard component
```

Claude answers in a comment on the same thread and updates it as it works, and it can push commits.

### Trigger 2: automated runs

Give the action a `prompt` and it runs on any event. Two examples.

**Review every PR automatically.** This installs the `code-review` plugin and runs its skill when a PR is opened, updated, reopened or marked ready. It's the do-it-yourself version of managed Code Review, so it works without a Team plan:

```yaml
name: Code Review
on:
  pull_request:
    types: [opened, synchronize, ready_for_review, reopened]
jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: read
      issues: read
      id-token: write
    steps:
      - uses: actions/checkout@v6
        with:
          fetch-depth: 1
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          plugin_marketplaces: "https://github.com/anthropics/claude-code.git"
          plugins: "code-review@claude-code-plugins"
          prompt: "/code-review:code-review --comment ${{ github.repository }}/pull/${{ github.event.pull_request.number }}"
          claude_args: '--allowedTools "mcp__github_inline_comment__create_inline_comment"'
```

- `--comment` is what makes Claude post on the PR. Without it the findings only go to the workflow run log.
- Keep the `claude_args` line. The action only starts the inline-comment tool when `--allowedTools` names it.
- It skips drafts, closed PRs, PRs it thinks don't need review, and PRs that already have a comment from Claude.
- On public repos GitHub withholds secrets from fork PRs, so it only runs on branches in the same repo.

**On a schedule.** A daily report in the run log at 09:00 UTC:

```yaml
name: Daily Report
on:
  schedule:
    - cron: "0 9 * * *"
  workflow_dispatch:   # adds a "Run workflow" button in the Actions tab
jobs:
  report:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      issues: read
      id-token: write
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Generate a summary of yesterday's commits and open issues"
          claude_args: |
            --model claude-opus-5-5
            --allowedTools "mcp__github__list_commits,mcp__github__list_issues"
```

With a plain-text prompt Claude has no shell or GitHub access until I grant tools with `--allowedTools`. Scheduled workflows only run from the default branch, and on public repos GitHub switches the schedule off after 60 days without repo activity.

**Running one by hand (`workflow_dispatch`).** Adding `workflow_dispatch:` under `on:` puts a "Run workflow" button in the Actions tab, and `gh workflow run <file>.yml` does the same from the terminal. It's handy for testing the schedule without waiting for the cron. The workflow file has to be on the default branch for the button to show up. It only suits automation mode, since the `@claude` mode needs a comment to answer.

For the review workflow a manual run has no `github.event.pull_request`, so it needs the PR number as an input (untested, I haven't run this one):

```yaml
on:
  pull_request:
    types: [opened, synchronize, ready_for_review, reopened]
  workflow_dispatch:
    inputs:
      pr_number:
        description: PR number to review
        required: true
```

and in the step, use whichever one exists:

```yaml
prompt: "/code-review:code-review --comment ${{ github.repository }}/pull/${{ github.event.pull_request.number || inputs.pr_number }}"
```

The prompt can also be a skill from the repo (`/skill-name`, with a checkout step before the action so the files exist).

### Useful inputs

| Input | What it does |
| --- | --- |
| `prompt` | Instructions or a `/skill`. Leave it out for the `@claude` mode |
| `claude_args` | Any Claude Code CLI flag: `--max-turns`, `--model`, `--allowedTools`, `--mcp-config`, `--debug` |
| `anthropic_api_key` / `claude_code_oauth_token` | How it authenticates |
| `trigger_phrase` | Change `@claude` to something else |
| `plugin_marketplaces` / `plugins` | Install plugins before the run |
| `settings` | Claude Code settings as JSON or a path |
| `use_bedrock` / `use_vertex` / `use_foundry` | Send inference through a cloud provider instead |

### Who can trigger it

- The person must have **write access** to the repo (issue and PR events).
- A **bot** is rejected unless it's listed in `allowed_bots`, which keeps bots from setting off loops. That includes scheduled runs if the last person to edit the cron line was a bot.

### Keeping costs down

Each run uses GitHub Actions minutes plus API tokens (or subscription usage if I use the OAuth token). To limit it: write specific `@claude` requests, keep `CLAUDE.md` short because it's read every run, set `--max-turns`, add a workflow `timeout-minutes`, and use GitHub concurrency controls.

### If it doesn't respond

- The App isn't installed on the repo, or workflows are disabled.
- The secret is missing or wrong.
- The comment doesn't contain `@claude` as a whole word (`/claude` and `@claude-bot` don't count).
- The commenter doesn't have write access.
- CI doesn't run on Claude's commits: that happens if I pass `github_token: ${{ secrets.GITHUB_TOKEN }}`, because GitHub doesn't trigger workflows from that token. Remove it.

### Removing it

Delete the workflow files, delete the secret (and the key in the Console if I want to retire it), and uninstall the GitHub App only if nothing else uses it. Code Review needs the same App.

## Which one when

- Checking my own work before pushing: `/code-review`.
- A team on Team or Enterprise that wants every PR reviewed with no upkeep: managed Code Review.
- A personal repo like this one, or full control over prompt, model and triggers: the GitHub Action with the review workflow, plus `@claude` for ad hoc requests.
- Both the managed review and the Action's review workflow on the same PR would post two reviews, so I'd pick one.

## Sources

- [Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)
- [Code Review](https://code.claude.com/docs/en/code-review)
- [claude-code-action on GitHub](https://github.com/anthropics/claude-code-action)
