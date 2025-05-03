# Servers Examples

This directory contains several server examples demonstrating different capabilities and integrations of the MCP (Modular Component Platform) library.

## Contents

-   **[async_postgres_server.py](async_postgres_server.py)**: An MCP server example that integrates with a PostgreSQL database using asynchronous operations. This server demonstrates how to expose database interactions as MCP tools, allowing clients to query and manipulate data.
-   **[enhanced_folder_server.py](enhanced_folder_server.py)**: An enhanced version of the `folder_server.py`, this server exposes tools that allow clients to interact with the file system, such as listing files and reading file contents. It likely includes additional features or security measures compared to the basic `folder_server.py`.
-   **[folder_server.py](folder_server.py)**: An MCP server that exposes tools for interacting with the file system. Clients can use these tools to list files in a directory, read file contents, and potentially perform other file-related operations.
-   **[postgres_server.py](postgres_server.py)**: An MCP server example that integrates with a PostgreSQL database. This server demonstrates how to expose database interactions as MCP tools, allowing clients to query and manipulate data.
-   **[web_search_using_tavily.py](web_search_using_tavily.py)**: An MCP server that provides web search functionality using the Tavily API. Clients can use this server to perform web searches and retrieve relevant information.

## Requirements

-   Python 3.7+
-   `mcp` library (install via `pip install mcp`)
-   `nest_asyncio` library (install via `pip install nest_asyncio`)
-   `psycopg2-binary` library (for PostgreSQL integration, install via `pip install psycopg2-binary`)
-   `tavily-python` (for web search integration, install via `pip install tavily-python`)
-   Appropriate database setup and credentials for the PostgreSQL servers.
-   Tavily API key for the web search server.

## Code Overview

### [async_postgres_server.py](async_postgres_server.py)

This script demonstrates an MCP server that asynchronously interacts with a PostgreSQL database. It likely uses libraries like `asyncpg` to handle asynchronous database connections and queries.  The exposed tools would allow clients to perform operations like querying data, inserting new records, or updating existing entries in the database.

### [enhanced_folder_server.py](enhanced_folder_server.py)

This server builds upon the basic `folder_server.py` by adding enhancements such as improved error handling, more sophisticated file filtering, or security features to restrict access to certain files or directories. It exposes tools for interacting with the file system.

### [folder_server.py](folder_server.py)

This script implements a basic MCP server that allows clients to interact with the file system. It exposes tools to list files in a directory, read file contents, and potentially perform other file-related operations.  This server provides a foundation for building more complex file management applications using MCP.

### [postgres_server.py](postgres_server.py)

This script showcases an MCP server integrated with a PostgreSQL database. It exposes database interactions as MCP tools, enabling clients to query and manipulate data stored in the database.  The server uses a library like `psycopg2` to connect to the database and execute SQL queries.

### [web_search_using_tavily.py](web_search_using_tavily.py)

This script implements an MCP server that provides web search functionality using the Tavily API. Clients can send search queries to the server, which then uses the Tavily API to retrieve search results and return them to the client.  This server requires a Tavily API key to authenticate with the Tavily service.