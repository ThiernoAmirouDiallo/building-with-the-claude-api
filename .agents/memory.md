# Notes to self

Contains things that aren't obvious from reading the code.

**What this repo is.** Working through Anthropic's "Building with the
Claude API" Coursera course. Notebooks in `src/building_with_the_claude_api/`
are numbered roughly in course order.

**claude_mcp_cli_project/** used to live at `~/src/claude_mcp_cli_project`,
moved it in here since it's the MCP-module exercise and belongs with
everything else. It's its own `uv` project though — own venv, own lockfile —
don't try to fold it into the notebooks' environment.

A couple of things bit me getting it running again after the move:

- Its `uv.lock` had every package's registry pointing at some internal
  Artifactory (`artifactory.infra.ant.dev`) — presumably from wherever it
  was originally scaffolded. My machine can't auth to that, got 401s on
  every install. Fix was just re-locking against public PyPI.
- `mcp[cli]` had no upper bound, so re-locking grabbed 2.x, which renamed
  `FastMCP` to `MCPServer` and broke the import in `mcp_server.py`. Pinned
  to `<2` at first to unblock, then migrated properly once the project was
  confirmed working: `mcp_server.py` now imports `MCPServer` from
  `mcp.server.mcpserver`, and `core/tools.py` uses `input_schema`/`is_error`
  instead of the old camelCase `inputSchema`/`isError`. Running on `mcp==2.2.0`
  now, no cap.
- `core/claude.py`'s `chat()` had `temperature=1.0` baked in, which the
  newer anthropic SDK doesn't accept anymore. First pass replaced it with
  `output_config.effort` + a try/except fallback for models that reject it
  — turned out to be overkill. `claude-sonnet-4-5` (what's in `.env` right
  now) just doesn't support `effort` at all, so simpler to default it off
  and only send it when someone explicitly asks. No fallback needed then.
