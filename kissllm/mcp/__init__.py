from dataclasses import dataclass, field
from typing import Dict, List, Literal, Optional, Union

from mcp import StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client


@dataclass
class StdioMCPConfig:
    """Configuration for an MCP server connected via stdio."""

    name: str
    command: str
    args: List[str] = field(default_factory=list)
    env: Optional[Dict[str, str]] = None
    type: Literal["stdio"] = "stdio"

    def create_transport(self):
        """Create stdio transport for this configuration."""
        server_params = StdioServerParameters(
            command=self.command, args=self.args, env=self.env
        )
        transport = stdio_client(server_params)
        return transport


@dataclass
class SSEMCPConfig:
    """Configuration for an MCP server connected via SSE."""

    name: str
    url: str
    type: Literal["sse"] = "sse"

    def create_transport(self):
        """Create SSE transport for this configuration."""
        transport = sse_client(self.url)
        return transport


MCPConfig = Union[StdioMCPConfig, SSEMCPConfig]


# Example mcp_servers.json structure:
"""
{
  "servers": [
    {
      "name": "My Stdio Server",
      "type": "stdio",
      "command": "python",
      "args": ["/path/to/my_mcp_server.py", "stdio"],
      "env": {"MY_VAR": "value"}
    },
    {
      "name": "My SSE Server",
      "type": "sse",
      "url": "http://localhost:8080/sse"
    },
    {
       // Minimal stdio config
      "command": "another_server_cmd"
    }
  ]
}
"""
