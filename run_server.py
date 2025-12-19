import subprocess
import sys

# Run FastMCP with HTTP transport on port 3001
subprocess.run([
    sys.executable, 
    "-m", 
    "mcp.server.fastmcp",
    "randomNO:mcp",
    "--transport", "http",
    "--host", "127.0.0.1", 
    "--port", "3001"
])
