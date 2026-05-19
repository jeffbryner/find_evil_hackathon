# /// script
# dependencies = [
#   "mcp[cli]",
# ]
# ///

import os
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("filesystem")


@mcp.tool()
def list_directory(path: str = ".") -> list[str]:
    """
    List all files and directories at the given path.
    Unlike some other tools, this will show ALL files, including binary ones.
    """
    try:
        # Resolve path relative to current working directory
        target_path = os.path.abspath(os.path.join(os.getcwd(), path))

        # Verify it exists and is a directory
        if not os.path.exists(target_path):
            return [f"Error: Path '{path}' does not exist."]
        if not os.path.isdir(target_path):
            return [f"Error: Path '{path}' is not a directory."]

        return os.listdir(target_path)
    except Exception as e:
        return [f"Error listing directory: {str(e)}"]


@mcp.tool()
def create_directory(path: str) -> str:
    """
    Create a new directory (and any parent directories) if it doesn't already exist.
    """
    try:
        # Resolve path relative to current working directory
        target_path = os.path.abspath(os.path.join(os.getcwd(), path))

        os.makedirs(target_path, exist_ok=True)
        return f"Successfully created directory: {path}"
    except Exception as e:
        return f"Error creating directory: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
