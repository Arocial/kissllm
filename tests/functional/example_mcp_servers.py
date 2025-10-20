import argparse
import os
import sys

# Determine the absolute path to this script file
# This is needed so the aggregator can correctly configure its backends
# to call this same script.
SCRIPT_PATH = os.path.abspath(__file__)


# --- Simple MCP Server Definition ---
def create_simple_mcp_server():
    """Creates and returns a simple FastMCP server instance."""
    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP("Test Server")

    @mcp.tool()
    def add(a: int, b: int) -> int:
        """Add two numbers"""
        return a + b

    @mcp.tool()
    def multiply(a: int, b: int) -> int:
        """Multiply two numbers"""
        return a * b

    return mcp


# --- Main Execution Logic ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Example MCP Servers for Testing")
    parser.add_argument(
        "mode",
        choices=["stdio", "streamable-http"],
        help="Transport mode (stdio or streamable http)",
    )
    parser.add_argument(
        "--port", type=int, help="Port number for streamable http mode", default=None
    )
    parser.add_argument(
        "--host", type=str, help="Host for streamable http mode", default="localhost"
    )

    args = parser.parse_args()

    server = None
    server = create_simple_mcp_server()
    print(f"Starting Simple MCP Server in {args.mode} mode...")

    if server:
        if args.mode == "streamable-http" and args.port is not None:
            server.settings.port = args.port
            server.settings.host = args.host

        server.run(args.mode)
    else:
        print(f"Error: Unknown server type '{args.server_type}'", file=sys.stderr)
        sys.exit(1)
