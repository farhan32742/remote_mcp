from mcp.server.fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("Math Wizard")

@mcp.tool()
async def add(x: float, y: float) -> str:
    """Add two numbers together."""
    result = x + y
    return f"The sum of {x} and {y} is {result}"

@mcp.tool()
async def subtract(x: float, y: float) -> str:
    """Subtract y from x."""
    result = x - y
    return f"The difference between {x} and {y} is {result}"

@mcp.tool()
async def multiply(x: float, y: float) -> str:
    """Multiply two numbers."""
    result = x * y
    return f"The product of {x} and {y} is {result}"

@mcp.tool()
async def divide(x: float, y: float) -> str:
    """Divide x by y. Handles division by zero errors."""
    if y == 0:
        return "Error: Cannot divide by zero."
    result = x / y
    return f"The result of dividing {x} by {y} is {result}"

if __name__ == "__main__":
    # The run() method handles the event loop for the async tools
    mcp.run()