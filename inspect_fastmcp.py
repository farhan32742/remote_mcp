
from mcp.server.fastmcp import FastMCP
import asyncio

mcp = FastMCP("RandomNumber")

print("Attributes of mcp object:")
print(dir(mcp))

# Try to find underlying app or routes
if hasattr(mcp, "_fastapi_app"):
    print("\nFastAPI App detected.")
    for route in mcp._fastapi_app.routes:
        print(f"Route: {route.path} [{route.name}]")

