# Simple Examples

This directory contains simple examples demonstrating the usage of the MCP (Modular Component Platform) library. It includes both client and server implementations using different transport mechanisms: `stdio` and `sse`.

## MCP Example: Client-Server Communication with SSE and Stdio

This directory contains example scripts demonstrating the Modular Component Platform (MCP) library for building client-server applications using two transport mechanisms: Server-Sent Events (SSE) and Standard Input/Output (stdio). The scripts provide a hands-on introduction to MCP's core functionality, making them ideal for learning how to create and interact with modular tools.

## Overview

The MCP library enables modular, component-based applications where clients can invoke tools (functions) exposed by a server. These examples illustrate:

- **Server Implementation**: A server that exposes an `add` tool for adding two integers, supporting either SSE or stdio transport.
- **Client Implementation**: A client that connects to the server, lists available tools, and invokes the `add` tool with specific arguments.

The scripts are intentionally simple to focus on MCP's key concepts. When you run a script in this directory via the repository's custom command (e.g., `mcp dev`), an interactive playground opens in a browser, rendering this README and offering features to explore the code interactively.

## Scripts in This Directory

- **[client_sse.py](client_sse.py)**: A client that connects to an MCP server via SSE, lists available tools, and calls the `add` tool with arguments `num_1=2`, `num_2=3`.
- **[client_stdio.py](client_stdio.py)**: A client that launches an MCP server as a subprocess, connects via stdio, lists tools, and calls the `add` tool with arguments `num_1=2`, `num_2=7`.
- **[server_sse.py](server_sse.py)**: A server that exposes the `add` tool and listens for SSE connections on port 8050.
- **[server_stdio.py](server_Stdio.py)**: A server that exposes the `add` tool and communicates via stdio.
- **README.md**: This documentation, displayed in the playground to guide learning.

## Playground Integration

This directory is part of a larger repository with multiple subdirectories, each containing MCP examples. Running a script (e.g., via `mcp dev`) launches a browser-based playground that displays this README and allows users to run the scripts, view outputs, or modify code interactively. The playground aims to provide an engaging learning experience, similar to LangGraph's `langgraph dev` command, by combining documentation with hands-on exploration.

## MCP Library Overview

The Modular Component Platform (MCP) library provides a framework for building distributed applications with a client-server architecture. The key components used in these examples are:

- **FastMCP**: A server class for registering tools and handling client connections.
- **ClientSession**: A client class for initializing sessions, listing tools, and invoking tools on the server.
- **StdioServerParameters**: A configuration class for launching a server as a subprocess in stdio mode.
- **sse_client**: A context manager for establishing SSE connections.
- **stdio_client**: A context manager for launching a server and establishing stdio connections.

These examples demonstrate how to use these components to create a simple client-server system where the server exposes an `add` tool, and the client interacts with it using different transport mechanisms.

## Code Documentation

This section provides detailed documentation for the classes and functions in the scripts, following Python's PEP 8 and PEP 257 guidelines. Each entry includes a description, parameters, return values, and usage examples to help you understand the code's functionality.

### Server Scripts: server_sse.py and server_stdio.py

The server scripts implement an MCP server that exposes an `add` tool for adding two integers. They use the `FastMCP` class and differ only in their default transport mechanism: `sse` for `server_sse.py` and `stdio` for `server_stdio.py`.

#### Class: FastMCP

```python
class FastMCP:
    """Creates and manages an MCP server for handling client requests and tools.

    Args:
        name (str): The server instance name (e.g., "MCP-Demo").
        host (str): The host address to bind to (e.g., "0.0.0.0" for all interfaces).
        port (int): The port for SSE communication (e.g., 8050, ignored for stdio).

    Attributes:
        name (str): The server identifier.
        host (str): The network interface for the server.
        port (int): The port for SSE connections.

    Methods:
        tool: Registers a function as an MCP tool.
        run: Starts the server with the specified transport mechanism.
    """
```

**Purpose**: Initializes an MCP server to manage tools and client communications.

**Usage Example**:
```python
mcp = FastMCP(name="MCP-Demo", host="0.0.0.0", port=8050)
```

#### Method: FastMCP.tool

```python
def tool(self):
    """Decorator to register a function as an MCP tool.

    Returns:
        callable: A decorator that adds the function to the server's tool registry.

    Example:
        @mcp.tool()
        def multiply(x: int, y: int) -> int:
            return x * y
    """
```

**Purpose**: Marks a function as an MCP tool, making it available for clients to invoke.

**Usage Example**:
```python
@mcp.tool()
def add(num_1: int, num_2: int) -> int:
    return num_1 + num_2
```

#### Method: FastMCP.run

```python
def run(self, transport: str) -> None:
    """Starts the MCP server with the specified transport mechanism.

    Args:
        transport (str): The communication protocol, either "stdio" or "sse".

    Raises:
        ValueError: If the transport is not "stdio" or "sse".
    """
```

**Purpose**: Launches the server to accept client connections via the specified transport.

**Usage Example**:
```python
mcp.run(transport="sse")
```

#### Function: add

```python
@mcp.tool()
def add(num_1: int, num_2: int) -> int:
    """Adds two integers.

    Args:
        num_1 (int): The first integer to add.
        num_2 (int): The second integer to add.

    Returns:
        int: The sum of num_1 and num_2.
    """
    return num_1 + num_2
```

**Purpose**: A tool that computes the sum of two integers, exposed for client invocation.

**Usage Example (from client)**:
```python
result = await session.call_tool("add", arguments={"num_1": 2, "num_2": 3})
print(result.content[0].text)  # Output: "5"
```

#### Main Block

```python
if __name__ == '__main__':
    transport: str = "sse"  # or "stdio"
    if transport == "stdio":
        print("Running server with stdio transport")
        mcp.run(transport="stdio")
    elif transport == "sse":
        print("Running server with sse transport")
        mcp.run(transport="sse")
    else:
        raise ValueError("Invalid transport type. Use 'stdio' or 'sse'.")
```

**Purpose**: Configures the transport mechanism and starts the server.

**Behavior**: Prints the transport type and calls `mcp.run` to launch the server.

### Client Scripts: client_sse.py and client_stdio.py

The client scripts implement an MCP client that connects to a server, lists available tools, and invokes the `add` tool. They differ in their transport mechanism: `sse` for `client_sse.py` and `stdio` for `client_stdio.py`.

#### Class: ClientSession

```python
class ClientSession:
    """Manages an MCP client session for interacting with a server.

    Args:
        read_stream: Stream for receiving server responses.
        write_stream: Stream for sending requests to the server.

    Methods:
        initialize: Initializes the client-server connection.
        list_tools: Queries the server for available tools.
        call_tool: Invokes a tool on the server with specified arguments.
    """
```

**Purpose**: Handles client operations, including session setup, tool discovery, and tool invocation.

**Usage Example**:
```python
async with ClientSession(read_stream, write_stream) as session:
    await session.initialize()
```

#### Method: ClientSession.initialize

```python
async def initialize(self) -> None:
    """Initializes the client session for server communication.

    Returns:
        None
    """
```

**Purpose**: Establishes the client-server connection, preparing for further operations.

#### Method: ClientSession.list_tools

```python
async def list_tools(self) -> ToolsResult:
    """Retrieves the list of tools available on the server.

    Returns:
        ToolsResult: An object containing a list of tools with names and descriptions.
    """
```

**Purpose**: Queries the server for registered tools and returns their details.

**Usage Example**:
```python
tools_result = await session.list_tools()
for tool in tools_result.tools:
    print(f"  - {tool.name}: {tool.description}")
# Output: "  - add: Adds two numbers."
```

#### Method: ClientSession.call_tool

```python
async def call_tool(self, tool_name: str, arguments: dict) -> ToolResult:
    """Invokes a tool on the server with the specified arguments.

    Args:
        tool_name (str): The name of the tool to call (e.g., "add").
        arguments (dict): A dictionary of argument names and values.

    Returns:
        ToolResult: An object containing the tool's execution result.
    """
```

**Purpose**: Sends a request to execute a tool and retrieves the result.

**Usage Example**:
```python
result = await session.call_tool("add", arguments={"num_1": 2, "num_2": 3})
print(result.content[0].text)  # Output: "5"
```

#### Class: StdioServerParameters (in client_stdio.py)

```python
class StdioServerParameters:
    """Configures a server subprocess for stdio communication.

    Args:
        command (str): The command to run the server (e.g., "python").
        args (list[str]): Arguments for the command (e.g., ["server_stdio.py"]).
    """
```

**Purpose**: Specifies how to launch the server as a subprocess for stdio transport.

**Usage Example**:
```python
server_params = StdioServerParameters(command="python", args=["server_stdio.py"])
```

#### Function: sse_client (in client_sse.py)

```python
async def sse_client(url: str) -> tuple:
    """Establishes a Server-Sent Events connection to an MCP server.

    Args:
        url (str): The server endpoint (e.g., "http://localhost:8050/sse").

    Returns:
        tuple: A tuple of (read_stream, write_stream) for client-server communication.

    Yields:
        The streams within an async context manager.
    """
```

**Purpose**: Sets up an SSE connection, providing streams for communication.

**Usage Example**:
```python
async with sse_client("http://localhost:8050/sse") as (read_stream, write_stream):
    # Use streams with ClientSession
```

#### Function: stdio_client (in client_stdio.py)

```python
async def stdio_client(server_params: StdioServerParameters) -> tuple:
    """Launches a server subprocess and establishes a stdio connection.

    Args:
        server_params (StdioServerParameters): Configuration for the server subprocess.

    Returns:
        tuple: A tuple of (read_stream, write_stream) for client-server communication.

    Yields:
        The streams within an async context manager.
    """
```

**Purpose**: Starts the server and sets up stdio streams for communication.

**Usage Example**:
```python
server_params = StdioServerParameters(command="python", args=["server_stdio.py"])
async with stdio_client(server_params) as (read_stream, write_stream):
    # Use streams with ClientSession
```

#### Function: main (in both client scripts)

```python
async def main() -> None:
    """Demonstrates MCP client operations by connecting to a server and invoking a tool.

    Connects to an MCP server, lists available tools, and calls the 'add' tool.

    Returns:
        None
    """
```

**Purpose**: Orchestrates client operations, including connection, tool listing, and tool invocation.

**Behavior**:
- In `client_sse.py`: Connects to `http://localhost:8050/sse` and calls `add` with `num_1=2`, `num_2=3`.
- In `client_stdio.py`: Launches the server via `StdioServerParameters` and calls `add` with `num_1=2`, `num_2=7`.

**Usage Example**:
```python
asyncio.run(main())
```

#### Main Block (in both client scripts)

```python
if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
```

**Purpose**: Applies `nest_asyncio` to support nested event loops and runs the main coroutine.

**Note**: `nest_asyncio.apply()` ensures compatibility with environments like Jupyter or playgrounds that may have existing event loops.

## Expected Output

When viewed in the playground, the scripts produce the following outputs:

For `client_sse.py`:
```
Available tools:
  - add: Adds two numbers.
2 + 3 = 5
```

For `client_stdio.py`:
```
Available Tools:
 - add: Adds two numbers.
Result of add tool: 9
```

These outputs show the client listing the `add` tool and invoking it with different arguments.

## Learning with the Playground

The interactive playground enhances learning by:

- **Rendering This README**: Provides detailed documentation and context for the scripts.
- **Interactive Exploration**: Allows running the scripts, viewing outputs, or editing code in the browser.
- **Guided Learning**: Demonstrates MCP's client-server architecture with a simple `add` tool, making it easy to understand key concepts.

To explore, run a script in this directory using the repository's custom command (e.g., `mcp dev`). The playground will open in your browser, displaying this documentation and offering interactive features.

## Troubleshooting

- **SSE Connection Issues**: Ensure `server_sse.py` is running and accessible at `http://localhost:8050/sse`. Check for port conflicts and update the port in both `server_sse.py` and `client_sse.py` if necessary.
- **Stdio Server Not Starting**: Verify that `server_stdio.py` is in the same directory as `client_stdio.py` and that the `python` command is available.
- **Playground Not Loading**: If the browser does not open or the README is not displayed, consult the repository's main documentation for the correct command to launch the playground.
- **Incorrect Output**: Ensure the client and server use the same transport mechanism (e.g., `client_sse.py` with `server_sse.py`).

## License

This project is licensed under the MIT License. See the LICENSE file in the repository root for details.