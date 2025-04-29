# MCP-DEMO: My Learning Journey with Model Context Protocol

## Introduction

This repository documents my learning journey with the Model Context Protocol (MCP). As I explore and understand this new technology, I'm implementing various examples and documenting my findings. MCP is a fascinating protocol that enables seamless interaction between Large Language Models (LLMs) and local tools/services.

## What is MCP?

The Model Context Protocol (MCP) is a protocol designed to facilitate communication between language models and local tools/services. It provides:
- Standardized way to expose local tools to LLMs
- Multiple transport layers (stdio and Server-Sent Events)
- Integration with various LLMs (like OpenAI and Groq)
- Tool discovery and registration mechanisms
- Async support for better performance

## Learning Path Structure

My learning journey is organized into several key areas:

### 1. Simple Examples (`learning/simple/`)
Start here to understand the basics:
- [`server_stdio.py`](learning/simple/server_stdio.py): Basic MCP server using stdio transport
- [`client_stdio.py`](learning/simple/client_stdio.py): Corresponding stdio client
- [`server_sse.py`](learning/simple/server_sse.py): MCP server using SSE transport
- [`client_sse.py`](learning/simple/client_sse.py): SSE client implementation
- [README](learning/simple/README.md): More details about the Simple Examples

### 2. Groq Integration (`learning/groq/`)
Exploring MCP with Groq's LLM:
- Server implementation for knowledge base access
- Various client implementations (async, SSE, simple)
- Example of tool usage and LLM interactions
- [README](learning/groq/README.md): More details about the Groq Integration

### 3. Servers (`learning/Servers/`)
Different server implementations:
- PostgreSQL database server
- Web search server using Tavily
- File system server
- Async implementations
- [README](learning/Servers/README.md): More details about the Server Implementations

### 4. Clients (`learning/Clients/`)
Advanced client implementations:
- Multi-server client
- Agent implementations
- Async patterns
- [README](learning/Clients/README.md): More details about the Client Implementations

### 5. Asynchronous Python (`learning/asyncoronus python/`)
Learning async programming with Python:
- Basic async concepts
- Task management
- Event loops
- Real-world async patterns

## Project Setup

### Prerequisites
- Python 3.12 or higher
- uv package manager
- PostgreSQL (for database examples)
- API keys for Groq and Tavily

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mcp-demo.git
cd mcp-demo
```

2. Create a virtual environment and install dependencies using uv:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

## Learning Guide

1. **Start with Basics**:
   - Read through `learning/simple/` examples
   - Run the stdio examples first (simpler setup)
   - Understand the basic client-server interaction

2. **Progress to SSE Transport**:
   - Move to SSE examples for web-based communication
   - Learn about real-time updates and streaming

3. **Explore LLM Integration**:
   - Study the Groq examples
   - Understand tool registration and discovery
   - Learn about prompt engineering with tools

4. **Advanced Topics**:
   - Multi-server architectures
   - Async patterns and best practices
   - Complex tool implementations

## Project Structure

```
mcp-demo/
├── learning/
│   ├── simple/           # Basic examples
│   ├── groq/            # Groq LLM integration
│   ├── Servers/         # Various server implementations
│   ├── Clients/         # Client implementations
│   └── asyncoronus python/  # Async programming examples
├── main.py              # Project entry point
├── requirements.txt     # Project dependencies
└── README.md           # This file
```

## Dependencies

Key dependencies include:
- `mcp[cli]`: Core MCP functionality
- `groq`: Groq LLM API client
- `asyncpg`: Async PostgreSQL driver
- `httpx`: Async HTTP client
- `python-dotenv`: Environment management
- `tavily-python`: Web search API client

## Contributing

Feel free to:
- Open issues for questions
- Submit PRs for improvements
- Share your own learning experiences
- Add more examples

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Resources

- [MCP Documentation](https://mcp.readthedocs.io/)
- [Groq Documentation](https://docs.groq.com/)
- [AsyncIO Documentation](https://docs.python.org/3/library/asyncio.html)