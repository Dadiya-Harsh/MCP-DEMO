# Groq Examples: MCP Integration with Groq API

This directory contains example scripts demonstrating the integration of the **Groq API** with the **Modular Component Platform (MCP)** library. These examples showcase how to build client-server applications that leverage Groq's fast language models for:

- Querying a knowledge base
- Using tools for real-time data retrieval
- Supporting interactive communication via Server-Sent Events (SSE) and Standard Input/Output (stdio) transports

The scripts are designed for learning, with this README rendered in an interactive browser-based playground when a script is run (e.g., via `mcp dev`), similar to LangGraph's development environment.

---

## 🧠 Overview

The **Groq API**, powered by the **Language Processing Unit (LPU)**, provides ultra-low latency inference for large language models (LLMs), making it ideal for real-time applications.

These examples integrate Groq with MCP to create a **client-server architecture** where:

- Servers expose tools (e.g., querying a knowledge base)
- Clients connect to servers, list available tools, and use Groq’s LLMs to process queries, optionally calling server tools for enhanced responses

These scripts focus on MCP’s core concepts and Groq’s capabilities, making them ideal for learning how to combine fast LLMs with modular tools.

---

## 📜 Scripts in This Directory

- [`server.py`](server.py): An MCP server that exposes a `knowledge_base` tool to retrieve Q&A pairs from `data/kb.json`. Supports SSE and stdio transports via the `TRANSPORT` environment variable.
- [`simple_async_groq_client.py`](simple_async_groq_client.py): Asynchronous MCP client using stdio transport. Uses Groq’s LLM to process queries and invoke tools.
- [`simple_groq_client.py`](simple_groq_client.py): Synchronous stdio-based client with interactive chat loop.
- `simple_sse_client.py`: SSE-based client with interactive chat loop and real-time communication.
- [`tool_usage_example.py`](tool_usage_example.py): Demonstrates Groq’s tool-calling capabilities using mock weather and calculation tools.
- [`data/kb.json`](data/kb.json): JSON file containing Q&A pairs used by the `knowledge_base` tool.

---

## 🌐 Playground Integration

This directory is part of a larger repository with multiple MCP example subdirectories. Running a script (e.g., via `mcp dev`) launches a **browser-based playground** that:

- Displays this README
- May allow executing scripts, viewing outputs, or editing code
- Enhances learning via hands-on exploration (similar to `langgraph dev`)

---

## 🛠 Requirements

- Python 3.7+
- [`mcp`](https://pypi.org/project/mcp) (`pip install mcp`)
- [`groq`](https://pypi.org/project/groq) (`pip install groq`)
- `python-dotenv` (`pip install python-dotenv`)
- Groq API key set as `GROQ_API_KEY` (obtain from [Groq Console](https://console.groq.com))
- `.env` file with:
```env
  GROQ_API_KEY=your_api_key
  GROQ_MODEL=llama-3.3-70b-versatile  # Optional
```

---

## 🧩 MCP and Groq Integration Overview

### Key Components

* **FastMCP**: Server class for registering tools and handling client connections
* **ClientSession**: Initializes client sessions, lists tools, and invokes them
* **StdioServerParameters**: For stdio communication
* **sse\_client / stdio\_client**: Context managers for SSE or stdio
* **Groq / AsyncGroq**: Synchronous and asynchronous Groq API clients

---

## 📂 Code Documentation

### `server.py`

#### Class: `FastMCP`

```python
class FastMCP:
    """Creates and manages an MCP server for handling client requests and tools."""
```

* **Args**:

  * `name`: Server name (e.g., "LLM-Server")
  * `host`: Host address
  * `port`: Port for SSE (ignored for stdio)
* **Methods**:

  * `tool`: Registers a tool
  * `run`: Starts the server

#### Example:

```python
mcp = FastMCP(name="LLM-Server", host="0.0.0.0", port=8050)

@mcp.tool()
def knowledge_base() -> str:
    return "Knowledge base content"

mcp.run(transport="sse")
```

---

### Tool: `knowledge_base`

```python
@mcp.tool()
def knowledge_base() -> str:
    """Retrieve the entire knowledge base as a formatted string."""
```

* **Returns**: Formatted Q\&A string from `kb.json`

---

### `__main__` Block

```python
if __name__ == "__main__":
    if os.getenv("TRANSPORT") == "stdio":
        mcp.run(transport="stdio")
    elif os.getenv("TRANSPORT") == "sse":
        mcp.run(transport="sse")
```

---

## 👤 Client Scripts

### `simple_async_groq_client.py`

#### Class: `MCPGroqClient`

* `connect_to_server(server_script_path: str)`
* `get_mcp_tools() -> List[Dict[str, Any]]`
* `process_query(query: str) -> str`
* `cleanup()`

---

### `simple_groq_client.py` / `simple_sse_client.py`

#### Class: `SimpleGroqClient`

Includes all methods from `MCPGroqClient` plus:

* `chat_loop()`: Runs an interactive prompt

---

### Tool Call Example

```python
response = await client.process_query("What is our vacation policy?")
print(response)
```

---

## ⚙️ Tool Usage Example (`tool_usage_example.py`)

```python
def calculate(expression: str) -> str
def get_temperature(location: str) -> str
def get_weather_condition(location: str) -> str
```

### Example Output

```
The weather in New York is sunny and the temperature is 22°C.
The result of 10 * 4 + 5 is 45.
```

---

## 📁 `data/kb.json`

Contains a list of dictionaries:

```json
[
  {
    "question": "What is our vacation policy?",
    "answer": "20 days annually"
  }
]
```

Used by the `knowledge_base` tool to return structured content.

---

## ✅ Expected Output

### From `simple_async_groq_client.py`:

```
Connected to server with tools:
  - knowledge_base: Retrieve the entire knowledge base as a formatted string.
Query: What is our company's vacation policy?
Response: [Formatted knowledge base content or Groq's response]
```

### From `simple_sse_client.py`:

```
Connected to server with tools: ['knowledge_base']
MCP Client Started! Type your queries or 'quit' to exit.
Query: What is our vacation policy?
[Groq or tool-based response]
```

---

## 🧪 Learning with the Playground

* 📝 **README Rendering**: Context + Documentation
* 🧭 **Interactive Scripts**: Run + Explore
* 🧑‍🏫 **Hands-On Learning**: Modular + Real-Time LLM Integration

---

## ❗ Troubleshooting

| Issue                     | Resolution                                              |
| ------------------------- | ------------------------------------------------------- |
| Groq API Key Error        | Set `GROQ_API_KEY` in `.env` or environment variables   |
| SSE Not Connecting        | Ensure server is running with `TRANSPORT=sse`           |
| Stdio Server Fails        | Check `server.py` is present, Python available          |
| Invalid JSON in `kb.json` | Ensure it's a list of `{question, answer}` dictionaries |
| Playground Not Loading    | Refer to repo's main documentation for correct usage    |

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for details.

