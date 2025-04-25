from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="folder_server",
    host="localhost",
    port=8002,
)

@mcp.resource(name="folder_server", description="Provides access to a folder on the server.", uri="/path/to/folder")
def folder_server():
    """
    This resource provides access to a folder on the server.

    Returns:
        dict: Information about the folder server resource
    """
    return {"status": "ready", "message": "Folder server resource is ready"}


@mcp.tool(name="file_read", description="Perform file reading operations in the folder server.")
def file_read():
    """
    Perform file reading operations in the folder server.

    Returns:
        str: Information about the file operations
    """
    return "Performing file operations in the folder server."


@mcp.tool(name="file_write", description="Perform file writing operations in the folder server.")
def file_write():
    """
    Perform file writing operations in the folder server.

    Returns:
        str: Information about the file operations
    """
    return "Performing file operations in the folder server."

@mcp.tool(name="file_delete", description="Perform file deletion operations in the folder server.")
def file_delete():
    """
    Perform file deletion operations in the folder server.

    Returns:
        str: Information about the file operations
    """
    return "Performing file operations in the folder server."

@mcp.tool(name="folder_analysis", description="Does short analysis of the folder to provide context to ai agents.")
def folder_analysis():
    """
    Perform folder analysis operations in the folder server.

    Returns:
        str: Information about the folder analysis
    """
    return "Performing folder analysis in the folder server."

@mcp.prompt(
    name="folder_server_prompt",
    description="Prompt for performing operations in the folder server."
)
def folder_server_prompt():
    """
    Provides guidance and context for performing operations in the folder server.

    Returns:
        list: A list of chat messages for the AI to consider
    """
    return [
        {
            "role": "user",
            "content": "I need to perform operations in the folder server. Please help me with the following:"
        }
    ]

if __name__ == "__main__":
    mcp.run(transport="stdio")