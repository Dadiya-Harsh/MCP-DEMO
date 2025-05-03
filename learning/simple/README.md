# Simple Examples

This directory contains simple examples demonstrating the usage of the MCP (Modular Component Platform) library. It includes both client and server implementations using different transport mechanisms: `stdio` and `sse`.

## Contents

-   **[client_sse.py](client_sse.py)**: A client example that connects to an MCP server using Server-Sent Events (SSE).
-   **[client_stdio.py](client_stdio.py)**: A client example that connects to an MCP server using standard input/output (stdio).
-   **[server_sse.py](server_sse.py)**: (Not provided) An MCP server example that uses Server-Sent Events (SSE) for communication.
-   **[server_stdio.py](server_stdio.py)**: An MCP server example that uses standard input/output (stdio) for communication.

## Requirements

-   Python 3.7+
-   `mcp` library (install via `pip install mcp`)
-   `nest_asyncio` library (install via `pip install nest_asyncio`)

## Usage

### Running the stdio example

1.  Start the server:

    ```sh
    python server_stdio.py
    ```

2.  In a separate terminal, run the client:

    ```sh
    python client_stdio.py
    ```

### Running the SSE example

1.  Start the server:

    ```sh
    python server_sse.py
    ```

2.  In a separate terminal, run the client:

    ```sh
    python client_sse.py
    ```

**Note:** Ensure that the server is running before starting the client.  For the SSE example, verify the server is listening on the correct port (default is 8050 in [client_sse.py](client_sse.py)).

## Code Overview

### [client_sse.py](client_sse.py)

This script demonstrates how to create an MCP client that communicates with an MCP server using SSE. It initializes a `ClientSession`, lists available tools, and calls the `add` tool.

### [client_stdio.py](client_stdio.py)

This script demonstrates how to create an MCP client that communicates with an MCP server using stdio. It initializes a `ClientSession`, lists available tools, and calls the `add` tool.  It defines `StdioServerParameters` to configure the server execution.

### [server_stdio.py](server_stdio.py)

This script defines a simple MCP server using `FastMCP` that exposes an `add` tool.  The server can be run with either `stdio` or `sse` transport.