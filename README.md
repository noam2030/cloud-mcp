# Cloud MCP

A minimal [MCP](https://modelcontextprotocol.io) server with one tool:

- `get_current_time(timezone="UTC")`: the current date and time in an IANA timezone (for example `Asia/Jerusalem`), as ISO 8601.

It uses the official Python SDK (`mcp` 2.x) over **Streamable HTTP** at `/mcp`, in stateless JSON mode, so any instance can answer any request.

## Run locally

```bash
uv run python server.py          # http://127.0.0.1:8000/mcp
```

Try it with the MCP Inspector (a browser UI for MCP servers):

```bash
npx @modelcontextprotocol/inspector   # connect to http://127.0.0.1:8000/mcp, transport "Streamable HTTP"
```

## Docker

```bash
docker build -t cloud-mcp .
docker run --rm -p 8000:8080 -e PORT=8080 cloud-mcp
```

## Concepts

- **Tool:** a function the AI model can call. The docstring and type hints become the description and input schema the model reads.
- **Expected errors:** raise `ToolError` so the model sees the message and can retry. Any other exception reaches it only as "Error executing tool".
- **Host check:** bound to `127.0.0.1`, the SDK rejects requests with a foreign `Host` header (DNS-rebinding protection). In Docker it binds `0.0.0.0`, so access must be controlled elsewhere (Cloud Run IAM).

## Deploy

Merging to `main` runs [.github/workflows/deploy.yml](.github/workflows/deploy.yml). It logs in to Google with Workload Identity Federation and deploys the `cloud-mcp` Cloud Run service. The service is **private**: only the `cloud-agent` backend's account has `roles/run.invoker` on it, and the backend sends a Google ID token with each call.
