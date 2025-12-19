import os
import random
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP
mcp = FastMCP("RandomNumber")

@mcp.tool()
async def generate_random(min_value: int, max_value: int) -> int:
    """Generate a random number between min_value and max_value (inclusive)."""
    # Type consistency: always return an int or raise an error
    if min_value > max_value:
        raise ValueError("min_value must be less than or equal to max_value")
    return random.randint(min_value, max_value)

if __name__ == "__main__":
    # Cloud environments ke liye dynamic port aur host
    port = int(os.getenv("PORT", 8000))
    host = "0.0.0.0"

    print(f"Starting MCP server on {host}:{port}")
    mcp.run(transport="sse", host=host, port=port)



import os
import random
from mcp.server.fastmcp import FastMCP

# 1. Server instance create karein
mcp = FastMCP("RandomNumber")

@mcp.tool()
async def generate_random(min_value: int, max_value: int) -> int:
    """Generate a random number between min_value and max_value (inclusive)."""
    if min_value > max_value:
        raise ValueError("min_value must be less than or equal to max_value")
    return random.randint(min_value, max_value)

# 2. Yeh block sirf tab chalta hai jab aap file local computer par chalate hain
# FastMCP Cloud is block ko ignore karega aur conflict nahi hoga
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    # Local testing ke liye
    mcp.run(transport="sse", host="0.0.0.0", port=port)