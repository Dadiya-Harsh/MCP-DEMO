# MCP-DEMO: My Learning Journey with Model Context Protocol

## Introduction

This repository documents my learning journey with the Model Context Protocol (MCP). As I explore and understand this innovative technology, I’m implementing various examples and documenting my findings. MCP is a fascinating protocol that enables seamless interaction between Large Language Models (LLMs) and local tools/services.

## What is MCP?

The Model Context Protocol (MCP) is a protocol designed to facilitate communication between language models and local tools/services. It provides:
- A standardized way to expose local tools to LLMs.
- Multiple transport layers (stdio and Server-Sent Events).
- Integration with various LLMs (e.g., OpenAI and Groq).
- Tool discovery and registration mechanisms.
- Asynchronous support for enhanced performance.

## Learning Path Structure

My learning journey is organized into several key areas:

### 1. Simple Examples (`learning/simple/`)
Start here to understand the basics:
- [`server_stdio.py`](learning/simple/server_stdio.py): Basic MCP server using stdio transport.
- [`client_stdio.py`](learning/simple/client_stdio.py): Corresponding stdio client.
- [`server_sse.py`](learning/simple/server_sse.py): MCP server using SSE transport.
- [`client_sse.py`](learning/simple/client_sse.py): SSE client implementation.
- [README](learning/simple/README.md): More details about the Simple Examples.

### 2. Groq Integration (`learning/groq/`)
Exploring MCP with Groq's LLM:
- Server implementation for knowledge base access.
- Various client implementations (async, SSE, simple).
- Example of tool usage and LLM interactions.
- [README](learning/groq/README.md): More details about the Groq Integration.

### 3. Servers (`learning/Servers/`)
Different server implementations:
- PostgreSQL database server.
- Web search server using Tavily.
- File system server.
- Asynchronous implementations.
- [README](learning/Servers/README.md): More details about the Server Implementations.

### 4. Clients (`learning/Clients/`)
Advanced client implementations:
- Multi-server client.
- Agent implementations.
- Asynchronous patterns.
- [README](learning/Clients/README.md): More details about the Client Implementations.

### 5. Asynchronous Python (`learning/asynchronous python/`)
Learning async programming with Python:
- Basic async concepts.
- Task management.
- Event loops.
- Real-world async patterns.
- [README](learning/asynchronous python/README.md): More details about Asynchronous Python.

## Project Setup

### Prerequisites
- Python 3.12 or higher.
- `uv` package manager.
- PostgreSQL (for database examples).
- API keys for Groq and Tavily (optional, depending on examples).

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mcp-demo.git
   cd mcp-demo
   ```

2. Create a virtual environment and install dependencies using `uv`:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys (e.g., GROQ_API_KEY, TAVILY_API_KEY) and configuration
   ```

## Learning Guide

1. **Start with Basics**:
   - Read through `learning/simple/` examples.
   - Run the stdio examples first (simpler setup).
   - Understand the basic client-server interaction.

2. **Progress to SSE Transport**:
   - Move to SSE examples for web-based communication.
   - Learn about real-time updates and streaming.

3. **Explore LLM Integration**:
   - Study the Groq examples.
   - Understand tool registration and discovery.
   - Learn about prompt engineering with tools.

4. **Advanced Topics**:
   - Explore multi-server architectures.
   - Study async patterns and best practices.
   - Implement complex tool examples.

## Project Structure

```
mcp-demo/
├── learning/
│   ├── simple/              # Basic examples
│   ├── groq/                # Groq LLM integration
│   ├── Servers/             # Various server implementations
│   ├── Clients/             # Client implementations
│   └── asynchronous python/ # Async programming examples
├── main.py                  # Project entry point (CLI interface)
├── browser_documentation.py # Web-based interface
├── requirements.txt         # Project dependencies
├── templates/               # HTML templates for web interface
├── .env                     # Environment variables
└── README.md                # This file
```

## Using the Project

### Console-Based Interface
Run `python main.py` to explore the MCP learning journey via a command-line interface. Features include:
- Interactive menu to view full module documentation (`README.md` files).
- Listing and running Python scripts in each module.
- Console-based navigation for quick access.

### Web-Based Interface
Run `python browser_documentation.py` to launch a browser-based documentation site at `http://localhost:5000`. Features include:
- Full rendering of module documentation as HTML.
- Sidebar navigation for modules (`simple`, `groq`, `Servers`, etc.).
- Interactive script execution with outputs displayed via "Run" buttons on module pages (e.g., `/module/groq`).
- View script source code directly in the browser via links in `README.md` (e.g., `/learning/groq/simple_async_groq_client.py`) or module pages (e.g., `/module/groq/script/simple_async_groq_client.py`).
- Environment variable configuration at `/env` to set keys like `GROQ_API_KEY`, `DATABASE_URL`, etc.
- Responsive design with Tailwind CSS.

*Note*: Links in `README.md` (e.g., `learning/groq/simple_async_groq_client.py`) are intended to display script content in the web interface. If links redirect incorrectly (e.g., adding `/module/`), ensure the latest `browser_documentation.py` is used, or see the Troubleshooting section.

## Dependencies

Key dependencies include:
- `mcp[cli]`: Core MCP functionality.
- `groq`: Groq LLM API client.
- `asyncpg`: Asynchronous PostgreSQL driver.
- `httpx`: Asynchronous HTTP client.
- `python-dotenv`: Environment management.
- `tavily-python`: Web search API client.
- `flask`: Web framework for the browser interface.
- `markdown`: Markdown processing for documentation.

## Contributing

Feel free to:
- Open issues for questions or bugs.
- Submit pull requests (PRs) for improvements.
- Share your own learning experiences.
- Add more examples or modules.

## Troubleshooting

- **Link Redirection Issues**: If clicking a link (e.g., `learning/groq/simple_async_groq_client.py`) redirects to an incorrect URL (e.g., `/module/learning/groq/simple_async_groq_client.py` and shows a 404 error), update `browser_documentation.py` with the latest version from the repository or this documentation’s history. The file includes a fix to rewrite links to `/learning/<module>/<file>`.
- **Script Not Found**: Ensure the script file exists in the corresponding `learning/<module>/` directory and matches the name in `README.md`.
- **Environment Errors**: Verify `.env` contains all required variables (e.g., `GROQ_API_KEY`) and that the virtual environment is activated.
- **Web Interface Not Loading**: Check that `templates/` contains the required HTML files (`base.html`, `index.html`, `module.html`, `error.html`, `env.html`) and that `python browser_documentation.py` runs without errors.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Resources

- [MCP Documentation](https://mcp.readthedocs.io/)
- [Groq Documentation](https://docs.groq.com/)
- [AsyncIO Documentation](https://docs.python.org/3/library/asyncio.html)
- [Flask Documentation](https://flask.palletsprojects.com/)