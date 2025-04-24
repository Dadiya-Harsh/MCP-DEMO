import psycopg2
from psycopg2.extras import RealDictCursor
import json
import os
from mcp.server.fastmcp import FastMCP
import nest_asyncio
from dotenv import load_dotenv

load_dotenv()

nest_asyncio.apply()

mcp = FastMCP(name = "LLM-Server", host = "0.0.0.0", port = 8050)


@mcp.tool()
def knowledge_base() -> str:
    """Retrieve the entire knowledge base as a formatted string.

    Returns:
        A formatted string containing all Q&A pairs from the knowledge base.
    """
    try:
        kb_path = os.path.join(os.path.dirname(__file__), "data", "kb.json")
        with open(kb_path, "r") as f:
            kb_data = json.load(f)

        # Format the knowledge base as a string
        kb_text = "Here is the retrieved knowledge base:\n\n"

        if isinstance(kb_data, list):
            for i, item in enumerate(kb_data, 1):
                if isinstance(item, dict):
                    question = item.get("question", "Unknown question")
                    answer = item.get("answer", "Unknown answer")
                else:
                    question = f"Item {i}"
                    answer = str(item)

                kb_text += f"Q{i}: {question}\n"
                kb_text += f"A{i}: {answer}\n\n"
        else:
            kb_text += f"Knowledge base content: {json.dumps(kb_data, indent=2)}\n\n"

        return kb_text
    except FileNotFoundError:
        return "Error: Knowledge base file not found"
    except json.JSONDecodeError:
        return "Error: Invalid JSON in knowledge base file"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def database_connection(database_url: str = os.getenv("DATABASE_URL")) -> str:
    """ Sets up the database connection and retrieve answer from the database.
    Args:
        database_url: it is connection string which helps us to connect with the database..
    """
    try:
        conn = psycopg2.connect(database_url,cursor_factory = RealDictCursor)
        print("Connected to the database...")
        cursor = conn.cursor()
        cursor.close()
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return "Error connecting to the database"
    return "Toll is used.."

if __name__ == "__main__":
    if os.getenv("TRANSPORT") == "stdio":
        print("Running server with stdio transport")
        mcp.run(transport="stdio")
    elif os.getenv("TRANSPORT") == "sse":
        print("Running server with sse transport")
        mcp.run(transport="sse")
    # mcp.run(transport="stdio")
    # mcp.run(transport="sse")