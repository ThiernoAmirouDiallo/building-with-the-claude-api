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
