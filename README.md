# Building with the Claude API

Personal practice repo for Anthropic's Coursera course, [Building with the Claude API](https://www.coursera.org/learn/building-with-the-claude-api) (taught by Anthropic and Stephen Grider). Contains exercises and notes as I work through the course modules.

## Course modules

1. Getting Started with Claude — API fundamentals, model selection, authentication, multi-turn conversations, system prompts, structured outputs
2. Prompt Engineering & Evaluation — evaluation pipelines, test dataset generation, model-based and code-based grading, prompt optimization
3. Claude Features and Tool Use — tool calling, multi-turn tool conversations, extended thinking, multimodal support (images/PDFs), prompt caching, code execution
4. Model Context Protocol (MCP) — building reusable tool/resource integrations with standardized servers and clients
5. Retrieval Augmented Generation (RAG) — text chunking, embeddings, vector search, BM25 lexical search, reranking, contextual retrieval
6. Claude Code & Computer Use — development acceleration tools and automated interface interactions
7. Agentic Workflows — parallelization, sequential chaining, conditional routing, autonomous task handling

## Setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and requires Python 3.12+.

```bash
uv sync
```

Create a `.env` file in the project root with your API keys:

```
ANTHROPIC_API_KEY=your-api-key-here
VOYAGE_API_KEY=your-voyage-api-key-here
```

### Embeddings (RAG)

Claude doesn't offer its own embeddings model, so the RAG notebooks use [Voyage AI](https://www.voyageai.com/) to generate embeddings. `VOYAGE_API_KEY` is only needed for those notebooks.

## Structure

Exercises live under `src/building_with_the_claude_api/` as numbered Jupyter notebooks (e.g. `001_requests_exercice.ipynb`), roughly following the order of the course modules.

## Working with Claude Code

Two built-in slash commands are handy when working in this repo with [Claude Code](https://claude.com/claude-code).

### `/init`

Scans the codebase and generates a `CLAUDE.md` file in the project root: a summary of the project's structure, commands and conventions. Claude Code loads `CLAUDE.md` at the start of every session, so it starts out already knowing how the repo works. Run it once after cloning, or again after big structural changes. If a `CLAUDE.md` already exists, it suggests improvements instead of overwriting it.

This repo doesn't have a `CLAUDE.md` yet. Its agent-facing notes live in [`.agents/`](.agents/): `RULES.md` has working rules such as never committing without being asked, and `memory.md` has context that isn't obvious from the code.

### `/clear`

Clears the current conversation and starts a fresh one, dropping the message history from the context window. Use it when switching to an unrelated task, or when the context is full of old output (for example, long notebook results) that is slowing down or distracting the session. Your files and git state are not touched, and `CLAUDE.md` is loaded again in the new conversation. Anything you want to keep must be in a file, since the cleared conversation is gone from context.

### Git worktrees (`/new-worktree`)

A git worktree is an extra checkout of the same repo in its own folder, on its own branch. It lets you work on a feature without stashing or switching branches in your main checkout, and you can run a separate Claude Code session in each worktree. All worktrees share one `.git` history, so commits, branches and remotes are the same everywhere.

There are three ways to create one. All of them run the same script, [`.claude/skills/new-worktree/create-worktree.sh`](.claude/skills/new-worktree/create-worktree.sh).

**1. The slash command.** Start Claude Code in the repo root and type `/new-worktree` followed by the feature name:

```
> /new-worktree login-page
```

If you leave the name out, Claude asks for it. The `feature/` prefix is added automatically, so `login-page` becomes the branch `feature/login-page`. The command and the skill share the name `new-worktree`, so Claude Code may list them as a single entry in the `/` menu. Typing `/new-worktree` works either way. Slash commands and skills are loaded when a session starts, so restart Claude Code if you just pulled them.

**2. The skill.** Ask in plain words and Claude picks the skill up by itself, for example "create a worktree for the login page feature".

**3. The script directly, without Claude.** From the repo root in a normal terminal:

```bash
bash .claude/skills/new-worktree/create-worktree.sh login-page
```

An optional second argument sets the base branch (default `master`): `... login-page develop`.

The script:

1. creates the branch `feature/<name>` (the `feature/` prefix is added for you) from `master`
2. checks it out at `.worktrees/<name>/` (gitignored)
3. copies `.env` into it
4. runs `uv sync` there to build its own `.venv`

Then work in it:

```bash
cd .worktrees/login-page
claude
```

Manual commands:

```bash
git worktree list                                    # show all worktrees
git worktree remove .worktrees/login-page     # delete a worktree folder
git branch -d feature/login-page                     # delete the branch once merged
git worktree prune                                   # clean up records of folders deleted by hand
```

Things to know:

- A branch can be checked out in only one worktree at a time.
- `.env` and `.venv` are gitignored, so each worktree gets its own: `.env` is copied, and `.venv` is rebuilt rather than copied (a copied `.venv` would still point at the main repo's code).
- Notebooks keep working, since their relative paths (`./csv`, `./mds`, `./tmp`) resolve inside the worktree's own copy of the repo.
- The script never commits or pushes.

### Subagents

A subagent is a helper that Claude hands a task to. It runs in its own fresh context window, does the work, and sends back one summary, so a long review or search doesn't fill up the main conversation. It's one Markdown file: the frontmatter configures it and the body is its system prompt.

Where Claude Code looks for them:

- `.claude/agents/<name>.md` for this repo (commit it to share it)
- `~/.claude/agents/<name>.md` for every project on your machine

(The `.agents/` folder in this repo is not one of these. Claude Code doesn't load anything from it.)

This repo has one example, [`notebook-reviewer`](.claude/agents/notebook-reviewer.md), a read-only agent that checks a notebook for pasted keys, leftover cells, and old SDK habits. The file looks like this:

```markdown
---
name: notebook-reviewer
description: Read-only reviewer for the course notebooks. Use after editing a notebook, or when asked to check one.
tools: Read, Grep, Glob
model: sonnet
---

You review Jupyter notebooks in this repo. You only read and report, you never edit.
...
```

| Field | What it does |
|---|---|
| `name` | Identifier, lowercase with dashes. |
| `description` | Tells Claude when to use the agent. Write it as "use when ...". |
| `tools` | Allowlist of tools. Leave it out to inherit all of them. A reviewer should only get read tools. |
| `model` | `sonnet`, `opus`, `haiku` or `inherit`. |

To run one, ask for it by name, let Claude pick it from the `description`, or `@`-mention it:

```
> Use the notebook-reviewer agent on 018_reranking.ipynb
> @notebook-reviewer check 019_contextual.ipynb
> review the notebooks I changed
```

Agents are loaded when a session starts, so start a new session after adding or editing one. In a terminal `claude` session, `/agents` lists, creates and edits them.

### Creating skills and slash commands

A skill is a folder with a `SKILL.md` that teaches Claude how to do one kind of task. Claude reads only its short `description` up front and loads the full instructions when the task matches, or when you type `/<name>`. This repo's [`new-worktree`](.claude/skills/new-worktree/SKILL.md) skill is a working example.

Where they live:

- `.claude/skills/<name>/SKILL.md` for this repo
- `~/.claude/skills/<name>/SKILL.md` for every project

To make one:

1. Create the folder and file, `.claude/skills/<name>/SKILL.md`. The folder name should match `name`.
2. Add frontmatter with a `name` and a `description`. The description is what makes Claude pick the skill, so say what it does and when to use it ("Use when the user wants to ...").
3. Write the steps in the body, as you'd brief a colleague. Say what to ask the user, what to run, and what not to do (for example "don't commit").
4. Put anything fiddly in a script next to `SKILL.md` and call it from the steps, like `create-worktree.sh` does. A script is easier to test than a paragraph of instructions.
5. Start a new session, since skills are loaded at start, then try `/<name>` or ask for the task in plain words.

```markdown
---
name: my-skill
description: One sentence on what it does. Use when the user asks for X.
---

# Title

1. Step one.
2. Run `bash .claude/skills/my-skill/do-it.sh "<arg>"`.
3. Report the result. Do not commit or push.
```

A slash command is the simpler cousin: a single file `.claude/commands/<name>.md` with no folder. The filename becomes the command, `$ARGUMENTS` is whatever you type after it, and the frontmatter can set `description`, `argument-hint` and `allowed-tools` (the tools it may use without asking for permission). Use a command for a short fixed prompt and a skill when it needs supporting files or you want Claude to trigger it by itself. See [`.claude/commands/new-worktree.md`](.claude/commands/new-worktree.md).
