
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
    mcp.run()