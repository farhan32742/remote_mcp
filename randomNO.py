import os
import random
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("RandomNumber")

@mcp.tool()
async def generate_random(min_value: int, max_value: int) -> int:
    if min_value > max_value:
        return {"error": "min_value must be less than or equal to max_value"}
    return random.randint(min_value, max_value)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    mcp.run(transport="sse", host="0.0.0.0", port=port)