# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

Requires a `.env` file with:
```
ANTHROPIC_API_KEY=""
CLAUDE_MODEL=""        # e.g. claude-opus-4-6
USE_UV=0               # Set to 1 to run servers via uv instead of python
```

## Commands

```bash
# Run the app
uv run main.py              # with uv
python main.py              # without uv

# Pass additional MCP server scripts as args
python main.py extra_server.py

# Lint
ruff check .
ruff format .
```

No test suite is currently configured.

## Architecture

The app is an interactive CLI that chains together an MCP server, MCP client(s), and the Anthropic API.

**Startup flow** (`main.py`):
1. Creates a `Claude` service (Anthropic API wrapper)
2. Spawns `mcp_server.py` as a subprocess and connects an `MCPClient` to it (called `doc_client`)
3. Optionally connects additional MCP servers passed as CLI args
4. Wires everything into `CliChat`, then `CliApp`, and runs the async loop

**Key classes:**
- `MCPClient` (`mcp_client.py`) — wraps `mcp.ClientSession` over stdio transport. Most methods (`list_tools`, `call_tool`, `list_prompts`, `get_prompt`, `read_resource`) are stubs with `# TODO` comments — this is intentional as it's a training project.
- `Claude` (`core/claude.py`) — thin wrapper around `anthropic.Anthropic`. Supports tool use and extended thinking via `thinking=True`.
- `Chat` (`core/chat.py`) — base class managing the message history and the tool-use loop: sends messages → if `stop_reason == "tool_use"`, executes tools via `ToolManager` and loops; otherwise returns final text.
- `CliChat` (`core/cli_chat.py`) — extends `Chat` with document retrieval (`@doc_id` mentions), slash command dispatch (`/command doc_id`), and resource listing. It talks to `doc_client` for prompts/resources.
- `CliApp` (`core/cli.py`) — `prompt_toolkit`-based UI with tab-completion for `/commands` and `@resources`, key bindings, and in-memory history.
- `ToolManager` (`core/tools.py`) — collects tools from all clients, routes `tool_use` blocks to the correct client, and returns `ToolResultBlockParam` lists.
- `mcp_server.py` — a `FastMCP` server exposing an in-memory `docs` dict. Has one real tool (`read_doc_contents`) and several `# TODO` stubs for additional tools, resources, and prompts.

**MCP interaction pattern:**
- Resources use `docs://documents` (list all) and `docs://documents/{doc_id}` (single doc) URI scheme
- Prompts accept `{"doc_id": "..."}` as arguments
- Tools are standard MCP tools discovered at runtime
