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

Create a `.env` file in the project root with your Anthropic API key:

```
ANTHROPIC_API_KEY=your-api-key-here
```

## Structure

Exercises live under `src/building_with_the_claude_api/` as numbered Jupyter notebooks (e.g. `001_requests_exercice.ipynb`), roughly following the order of the course modules.
