# Groq Examples

This directory contains examples that demonstrate the usage of the Groq API with MCP. These examples showcase how to integrate Groq's language models into MCP servers and clients.

## Contents

-   **[server.py](learning/groq/server.py)**: An MCP server that exposes Groq's language models as tools. Clients can use this server to generate text, translate languages, and perform other language-related tasks using the Groq API.
-   **[simple_async_groq_client.py](learning/groq/simple_async_groq_client.py)**: An asynchronous MCP client that connects to a Groq-powered MCP server. This example demonstrates how to use asynchronous operations to interact with the server and generate text using Groq's language models.
-   **[simple_groq_client.py](learning/groq/simple_groq_client.py)**: A simple MCP client that connects to a Groq-powered MCP server. This example demonstrates how to use the client to generate text using Groq's language models.
-   **[simple_sse_client.py](learning/groq/simple_sse_client.py)**: An MCP client that connects to a Groq-powered MCP server using Server-Sent Events (SSE). This example demonstrates how to use SSE for real-time communication with the server and generate text using Groq's language models.
-   **[tool_usage_example.py](learning/groq/tool_usage_example.py)**: An example that demonstrates how to use the tools exposed by a Groq-powered MCP server. This example showcases how to call different tools and pass parameters to them.
-   **[data/kb.json](learning/groq/data/kb.json)**: A JSON file that likely contains a knowledge base used by one or more of the Groq examples. This file might contain facts, rules, or other information that the Groq language model can use to generate more informed responses.

## Requirements

-   Python 3.7+
-   `mcp` library (install via `pip install mcp`)
-   `langchain_groq` library (install via `pip install langchain-groq`)
-   `langchain` library (install via `pip install langchain`)
-   `dotenv` library (install via `pip install python-dotenv`)
-   A Groq API key for the Groq examples.

## Code Overview

### [server.py](learning/groq/server.py)

This script implements an MCP server that exposes Groq's language models as tools. Clients can connect to this server and use the tools to generate text, translate languages, and perform other language-related tasks. The server uses the Groq API to access the language models.

### [simple_async_groq_client.py](learning/groq/simple_async_groq_client.py)

This script demonstrates how to create an asynchronous MCP client that connects to a Groq-powered MCP server. It showcases how to use asynchronous operations to interact with the server and generate text using Groq's language models.

### [simple_groq_client.py](learning/groq/simple_groq_client.py)

This script provides a simple MCP client that connects to a Groq-powered MCP server. It demonstrates how to use the client to generate text using Groq's language models.

### [simple_sse_client.py](learning/groq/simple_sse_client.py)

This script implements an MCP client that connects to a Groq-powered MCP server using Server-Sent Events (SSE). It showcases how to use SSE for real-time communication with the server and generate text using Groq's language models.

### [tool_usage_example.py](learning/groq/tool_usage_example.py)

This script demonstrates how to use the tools exposed by a Groq-powered MCP server. It showcases how to call different tools and pass parameters to them.

### [data/kb.json](learning/groq/data/kb.json)

This file likely contains a knowledge base used by one or more of the Groq examples. It might contain facts, rules, or other information that the Groq language model can use to generate more informed responses.