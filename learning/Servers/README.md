# Servers Examples: Model Context Protocol (MCP) Implementations

This directory contains example scripts demonstrating server implementations using the **Model Context Protocol (MCP)** — a framework for integrating AI models with tools and resources. Each server exposes tools for specific functionalities such as PostgreSQL interaction, file system operations, or web search using the Tavily API.

> These scripts are designed for learning and run in an interactive browser-based playground when executed (e.g., via `mcp dev`), similar to LangGraph's development environment.

---

## 📘 Overview

The **Model Context Protocol (MCP)** enables AI-driven applications by providing a modular client-server architecture, where servers expose tools that clients (powered by AI) can invoke via **Server-Sent Events (SSE)**.

### Example Server Capabilities

- **Database Integration:** Async/sync PostgreSQL querying and management
- **File System Operations:** File reading/writing inside a safe folder scope
- **Web Search:** Real-time search via the Tavily API

These examples are focused, educational, and ideal for understanding how AI integrates securely with tools using MCP.

---

## 📂 Scripts in This Directory

### [`async_postgres_server.py`](async_postgres_server.py)
An async PostgreSQL server using `asyncpg`.

**Tools:**
- `connect_database`: Connects to a PostgreSQL database
- `execute_query`: Executes SQL queries
- `list_tables`: Lists tables in the database
- `describe_table`: Describes table schema
- `close_connection`: Closes DB connection

### `folder_server.py`
Performs file operations securely inside a base folder.

**Tools:**
- `file_read`: Reads file content
- `file_write`: Writes to a file
- `file_delete`: Deletes a file
- `folder_analysis`: Analyzes folder contents
- `folder_content`: Exposes folder as a resource

### [`postgres_server.py`](postgres_server.py)
Synchronous PostgreSQL server using `psycopg2`.

**Same tools as** `async_postgres_server.py`, but blocking I/O.

### [`web_search_using_tavily.py`](web_search_using_tavily.py)
Performs web searches using the **Tavily API**.

**Tool:**
- `web_search`: Returns structured search results from the web

---

## 🧪 Playground Integration

When run via `mcp dev`, the README is rendered in-browser alongside the interactive code environment. You can explore tools, inspect outputs, and even edit code live.

---

## 🛠 Requirements

- Python 3.7+
- Required packages:
```bash
pip install mcp asyncpg psycopg2-binary tavily-python python-dotenv
```

* PostgreSQL database setup
* Tavily API Key

### `.env` Example

```env
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=your_default_db
DATABASE_URI=postgresql://your_user:your_password@localhost:5432
TAVILY_API_KEY=your_tavily_key
ALLOWED_BASE_PATH=/path/to/allowed/directory
```

---

## 🚀 How to Use

### Start a Server

Example:
```
#in `server.py`
mcp.run(transport = "sse")
```

```bash
python async_postgres_server.py
```

Check console for:

```
Starting MCP PostgreSQL server on http://localhost:8002/sse
```

### Example: Create a Client

```python
from mcp.client.sse import sse_client
from mcp import ClientSession
import asyncio

async def main():
    async with sse_client("http://localhost:8002/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tools = await session.list_tools()
            print("Available tools:", [tool.name for tool in tools.tools])

asyncio.run(main())
```

### Tool Invocation Examples

**PostgreSQL:**

```python
result = await session.call_tool("connect_database", arguments={"db_name": "mydb"})
result = await session.call_tool("execute_query", arguments={"query": "SELECT * FROM users", "params": []})
print(result.content[0].text)
```

**Folder Server:**

```python
result = await session.call_tool("file_read", arguments={"path": "test.txt"})
print(result.content[0].text)
```

**Web Search:**

```python
result = await session.call_tool("web_search", arguments={"query": "AI news"})
print(result.content[0].text)
```

---

## 🧠 Example Workflow

### Scenario: Query PostgreSQL and Save to File

```python
# Step 1: Query users from database
async with sse_client("http://localhost:8002/sse") as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        result = await session.call_tool("execute_query", arguments={"query": "SELECT * FROM users", "params": []})
        data = json.loads(result.content[0].text)["results"]

# Step 2: Save query results to file
async with sse_client("http://localhost:8003/sse") as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        await session.call_tool("file_write", arguments={"path": "users.json", "content": json.dumps(data)})
```

---

## ✅ Expected Outputs

**PostgreSQL Example:**

```json
{"status": "success", "results": [{"id": 1, "name": "Alice"}, ...]}
```

**Folder Server Example:**

```json
{"status": "success", "path": "test.txt", "content": "Hello, world!"}
```

**Web Search Example:**

```json
{"status": "success", "query": "AI news", "results": [{"title": "...", "url": "..."}]}
```

---

## 🧑‍💻 Learning with the Playground

* **Interactive Docs:** This README is rendered in-browser
* **Live Editing:** Modify and run code live
* **Guided Learning:** Learn MCP architecture by example

Run:

```bash
mcp dev
```

---

## 🧰 Troubleshooting

| Issue                     | Solution                            |
| ------------------------- | ----------------------------------- |
| PostgreSQL not connecting | Ensure DB is running, check `.env`  |
| Tavily API not working    | Check `.env` for valid key          |
| Folder errors             | Ensure `ALLOWED_BASE_PATH` is valid |
| SSE not connecting        | Check ports, firewall, server logs  |
| Playground not launching  | Refer to repo root README or docs   |

---

## 🪪 License

MIT License. See `LICENSE` file in repo root.

