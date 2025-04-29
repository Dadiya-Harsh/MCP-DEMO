# Clients Examples

This directory contains examples of MCP clients that connect to various MCP servers.

## Contents

-   **[multi_server_mcp_client.py](learning/Clients/multi_server_mcp_client.py)**: An MCP client capable of connecting to multiple MCP servers simultaneously. This example demonstrates how to manage connections to different servers and interact with their respective tools.

## Requirements

-   Python 3.7+
-   `mcp` library (install via `pip install mcp`)

## Code Overview

### [multi_server_mcp_client.py](learning/Clients/multi_server_mcp_client.py)

This script demonstrates how to create an MCP client that can connect to and interact with multiple MCP servers. It showcases how to manage multiple `ClientSession` instances and call tools exposed by different servers. This is useful for building applications that need to access functionality from various MCP services.