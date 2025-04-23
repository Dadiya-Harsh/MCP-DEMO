from mcp.server.fastmcp import FastMCP

#create server
mcp = FastMCP(name = "MCP-Demo", host = "0.0.0.0", port = 8050)


@mcp.tool()
def add(num_1: int, num_2: int) -> int:
    """
    Adds two numbers..

    Args:
        num_1 and num_2 are both integers..
    """
    return num_1 + num_2

if __name__ == '__main__':
    transport: str = "stdio"
    if transport == "stdio":
        print("Running server with stdio transport")
        mcp.run(transport = "stdio")
    
    elif transport == "sse":
        print("Running server with sse transport")
        mcp.run(transport = "sse")

    else:
        raise ValueError("Invalid transport type. Use 'stdio' or 'sse'.")   