"""A minimal MCP server with one tool, served over Streamable HTTP."""

import os
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

mcp = MCPServer("cloud-mcp")


# The docstring and type hints become the tool description and input schema
# that the AI model sees, so they are part of the interface.
@mcp.tool()
def get_current_time(timezone: str = "UTC") -> str:
    """Get the current date and time in an IANA timezone, such as "UTC",
    "Asia/Jerusalem", or "America/New_York". Returns ISO 8601."""
    try:
        tz = ZoneInfo(timezone)
    except (ZoneInfoNotFoundError, ValueError):
        # ToolError sends this message to the model so it can retry with a valid
        # zone. Any other exception reaches it only as "Error executing tool".
        raise ToolError(f"Unknown timezone {timezone[:64]!r}. Use an IANA name like 'Europe/London'.")
    return datetime.now(tz).isoformat(timespec="seconds")


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        # 127.0.0.1 locally keeps the SDK's DNS-rebinding protection on.
        # The Docker image sets HOST=0.0.0.0; Cloud Run IAM guards access there.
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "8000")),
        # No per-client session in memory, so any Cloud Run instance can
        # answer any request, and replies are plain JSON instead of a stream.
        stateless_http=True,
        json_response=True,
    )
