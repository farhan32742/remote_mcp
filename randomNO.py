import random
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
    # FastMCP mein SSE ke liye sirf transport define karna kafi hota hai
    # Default port 8000 hota hai.
    mcp.run(transport="sse")