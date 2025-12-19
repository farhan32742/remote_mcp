import random
import os
from mcp.server.fastmcp import FastMCP

# Create FastMCP server
mcp = FastMCP("RandomNumber")

@mcp.tool()
async def generate_random(min_value: int, max_value: int) -> int:
    """Generate a random number between min_value and max_value (inclusive)."""
    if min_value > max_value:
        return {"error": "min_value must be less than or equal to max_value"}
    return random.randint(min_value, max_value)

if __name__ == "__main__":
    # Environment variables se port aur host uthayein (Production ke liye zaroori)
    port = int(os.getenv("PORT", 8000))
    # Remote access ke liye host hamesha 0.0.0.0 hona chahiye
    host = "0.0.0.0" 
    
    print(f"Starting MCP server on {host}:{port}")
    mcp.run(transport="sse", host=host, port=port)