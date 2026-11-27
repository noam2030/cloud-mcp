# Agent instructions

- `server.py` is the whole server: one `MCPServer` with `@mcp.tool()` functions.
- Run: `uv run python server.py`. Image: `docker build -t cloud-mcp .`
- MCP Python SDK is 2.x: `from mcp.server import MCPServer` (not 1.x `FastMCP`); fields are snake_case (`input_schema`).
- Raise `ToolError` for failures the model should read. Bound any echoed input.
- Deploys to the private Cloud Run service `cloud-mcp` on merge to `main`. Only `cloud-agent-runtime` may invoke it.
- Keep it simple. This is a learning project.
