# MCP-DEMO: Learning the Model Context Protocol

## Description

This project serves as a learning resource for the Modular Computation Protocol (MCP). It demonstrates MCP's usage with different transport layers (stdio and SSE) and various LLMs (OpenAI and Groq). The examples are designed to be easy to understand and modify, facilitating a hands-on learning experience.

## Project Structure

- [`main.py`](main.py): Entry point for the application (currently minimal).
- `learning/`: Contains examples and learning resources.
  - `simple/`: Simple examples using stdio and SSE transports.
    - [`server_stdio.py`](learning/simple/server_stdio.py): MCP server example using stdio transport.
    - [`server_sse.py`](learning/simple/server_sse.py): MCP server example using SSE transport.
    - [`client_stdio.py`](learning/simple/client_stdio.py): MCP client example using stdio transport.
    - [`client_sse.py`](learning/simple/client_sse.py): MCP client example using SSE transport.
  - `groq/`: Examples using the Groq LLM.
    - [`server.py`](learning/groq/server.py): MCP server example using Groq (currently empty).
    - [`client.py`](learning/groq/client.py): MCP client example using Groq (imports only).
- [`pyproject.toml`](pyproject.toml): Project configuration file (Poetry).
- `.gitignore`: Specifies intentionally untracked files that Git should ignore.
- [`LICENSE`](LICENSE): License information (MIT License).
- `.python-version`: Specifies the Python version used for the project.

## Dependencies

The project uses the following dependencies, managed by Poetry (see [`pyproject.toml`](pyproject.toml)):

- async
- httpx
- ipykernel
- langchain
- langchain-google-genai
- langchain-groq
- langgraph
- mcp\[cli]
- nest-asyncio
- openai
- psycopg2
- pytest
- python-dotenv
- tavily-python

## Getting Started

1.  Clone the repository.
2.  Install the dependencies using Poetry:

    ```bash
    poetry install
    ```

3.  Explore the examples in the `learning/simple` directory. Start with the stdio examples for a simpler setup.
4.  Modify the examples and experiment with different MCP configurations.
5.  Contribute to the project by adding more examples or improving the existing ones!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
