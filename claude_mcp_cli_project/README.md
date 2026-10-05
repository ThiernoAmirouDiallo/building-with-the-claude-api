# MCP Chat

MCP Chat is a command-line interface application that enables interactive chat capabilities with AI models through the Anthropic API. The application supports document retrieval, command-based prompts, and extensible tool integrations via the MCP (Model Control Protocol) architecture.

## Prerequisites

- Python 3.9+
- Anthropic API Key

## Setup

### Step 1: Configure the environment variables

1. Create or edit the `.env` file in the project root and verify that the following variables are set correctly:

```
ANTHROPIC_API_KEY=""  # Enter your Anthropic API secret key
```

### Step 2: Install dependencies

#### Option 1: Setup with uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

1. Install uv, if not already installed:

```bash
pip install uv
```

2. Create and activate a virtual environment:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
uv pip install -e .
```

4. Run the project

```bash
uv run main.py
```

#### Option 2: Setup without uv

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install anthropic python-dotenv prompt-toolkit "mcp[cli]==1.8.0"
```

3. Run the project

```bash
python main.py
```

## Usage

### Basic Interaction

Simply type your message and press Enter to chat with the model.

### Document Retrieval

Use the @ symbol followed by a document ID to include document content in your query:

```
> Tell me about @deposition.md
```

### Commands

Use the / prefix to execute commands defined in the MCP server:

```
> /summarize deposition.md
```

Commands will auto-complete when you press Tab.

## Development

### Adding New Documents

Edit the `mcp_server.py` file to add new documents to the `docs` dictionary.

### Implementing MCP Features

To fully implement the MCP features:

1. Server defined in `mcp_server.py`
2. Client functionality implemented in `mcp_client.py`
### MCP inspector 
The MCP inspector requires node. Install it with `brew install node`

Run `mcp dev mcp_server.py`. This will provide the url of the local browser based MCP debugger.

This MCP cli comes from the python dependency on the project.

### Using the server from Claude Code

`mcp_server.py` is a standard MCP server over stdio, so Claude Code (CLI or the desktop app's Code tab) can use its tools (`read_doc_contents`, `edit_document`), resources and prompts directly.

Register the **server** (`mcp_server.py`), not `main.py`. `main.py` is the interactive chat client, which needs a terminal and starts the server itself, so registering it fails with `CONNECTION_CLOSED`.

From this project's directory:

```bash
claude mcp add documents -- uv run --directory "$(pwd)" mcp_server.py
```

`--directory` makes the command work no matter which folder Claude Code is started from.

Check it connected:

```bash
claude mcp list
```

Start a new Claude Code session afterwards, since servers are loaded when a session starts. Inside a session, `/mcp` shows the status.

By default the server is added with local scope (private to you, for the current project). Add `-s project` to write it to a shared `.mcp.json` in the repo, or `-s user` to make it available in every project. To remove it:

```bash
claude mcp remove documents
```

The Claude Desktop chat app uses a separate config, `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "documents": {
      "command": "uv",
      "args": ["run", "--directory", "/absolute/path/to/claude_mcp_cli_project", "mcp_server.py"]
    }
  }
}
```

Restart the app after editing it. Use the full path to `uv` in `command` if the app can't find it.

### Linting and Typing Check

There are no lint or type checks implemented.
