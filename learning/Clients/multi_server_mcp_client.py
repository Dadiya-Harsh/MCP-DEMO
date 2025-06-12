import json
from typing import Any, Dict, List, Optional, Mapping
from contextlib import AsyncExitStack
import asyncio
import logging
from groq import Groq
import os
from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.sse import sse_client  # Use SSE transport

load_dotenv()

# Configure logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ServerConnection:
    """Class representing a connection to a single MCP server"""

    def __init__(self, server_id: str, url: str):
        """
        Initialize a server connection.

        Args:
            server_id: Unique identifier for this server
            url: URL of the MCP server's SSE endpoint
        """
        self.server_id = server_id
        self.url = url
        self.session: Optional[ClientSession] = None
        self.read_stream: Optional[Any] = None
        self.write_stream: Optional[Any] = None
        self.tools: List[Dict[str, Any]] = []
        self.tool_names: List[str] = []

    def __str__(self):
        return f"Server({self.server_id}, {self.url}, connected={self.session is not None})"

class MultiServerMCPClient:
    """Client for interacting with multiple MCP servers using Groq models over SSE transport."""

    def __init__(self):
        """Initialize the client."""
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.exit_stack = AsyncExitStack()
        self.servers: Dict[str, ServerConnection] = {}
        self.tool_to_server_map: Dict[str, str] = {}  # Maps tool names to server IDs

    async def connect_to_server(self, server_id: str, server_url: str):
        """
        Connect to an MCP server using SSE transport.

        Args:
            server_id: Unique identifier for this server
            server_url: URL of the MCP server's SSE endpoint
        """
        logger.info(f"Connecting to MCP server {server_id} at {server_url}")

        # Create a new server connection
        server = ServerConnection(server_id, server_url)
        self.servers[server_id] = server

        try:
            # Use sse_client from mcp.client.sse
            sse_transport = await self.exit_stack.enter_async_context(
                sse_client(
                    url=server_url,
                    headers={"Accept": "text/event-stream"},
                    timeout=5.0,  # HTTP timeout for initial connection
                    sse_read_timeout=300.0,  # 5 minutes for SSE read timeout
                )
            )
            server.read_stream, server.write_stream = sse_transport

            # Initialize ClientSession with SSE streams
            server.session = await self.exit_stack.enter_async_context(
                ClientSession(server.read_stream, server.write_stream)
            )
            await server.session.initialize()

            # List available tools
            response = await server.session.list_tools()

            # Store tool names and update tool-to-server mapping
            server.tool_names = [tool.name for tool in response.tools]
            for tool_name in server.tool_names:
                self.tool_to_server_map[tool_name] = server_id

            # Convert tools to Groq format
            server.tools = [
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema,
                    },
                }
                for tool in response.tools
            ]

            logger.info(f"Connected to server {server_id} with tools: {server.tool_names}")
            print(f"\nConnected to server {server_id} with tools: {server.tool_names}")

            return True
        except Exception as e:
            logger.error(f"Failed to connect to server {server_id}: {str(e)}")
            if server_id in self.servers:
                del self.servers[server_id]
            return False

    async def get_all_tools(self) -> List[Dict[str, Any]]:
        """
        Get all available tools from all connected MCP servers in Groq format.

        Returns:
            A list of all tools in Groq format.
        """
        all_tools = []
        for server in self.servers.values():
            all_tools.extend(server.tools)
        return all_tools

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a tool on the appropriate server.

        Args:
            tool_name: Name of the tool to call
            arguments: Arguments for the tool

        Returns:
            The result of the tool call
        """
        server_id = self.tool_to_server_map.get(tool_name)
        if not server_id:
            error_msg = f"Unknown tool: {tool_name}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}

        server = self.servers.get(server_id)
        if not server or not server.session:
            error_msg = f"Server {server_id} is not connected"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}

        try:
            result = await server.session.call_tool(tool_name, arguments=arguments)
            return {"status": "success", "content": result.content[0].text}
        except Exception as e:
            error_msg = f"Error calling tool {tool_name} on server {server_id}: {str(e)}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}

    async def process_query(self, query: str) -> str:
        """
        Process a query using Groq and available MCP tools.

        Args:
            query: The user query.

        Returns:
            The response from Groq.
        """
        if not self.servers:
            raise ValueError("No servers connected")

        # Get all available tools from all servers
        all_tools = await self.get_all_tools()
        if not all_tools:
            logger.warning("No tools available across all servers")

        # Initial Groq API call
        response = self.groq_client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": query}],
            tools=all_tools,
            tool_choice="auto",
        )

        # Get assistant's response
        assistant_message = response.choices[0].message

        # Initialize conversation with user query and assistant response
        messages = [
            {"role": "user", "content": query},
            {
                "role": assistant_message.role,
                "content": assistant_message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    } for tc in (assistant_message.tool_calls or [])
                ] if hasattr(assistant_message, 'tool_calls') and assistant_message.tool_calls else []
            }
        ]

        # Handle tool calls if present
        if hasattr(assistant_message, 'tool_calls') and assistant_message.tool_calls:
            # Process each tool call
            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                logger.info(f"Calling tool: {tool_name}")

                try:
                    # Parse arguments
                    arguments = json.loads(tool_call.function.arguments)

                    # Call the tool on the appropriate server
                    result = await self.call_tool(tool_name, arguments)

                    if result["status"] == "success":
                        content = result["content"]
                    else:
                        content = json.dumps(result)

                    # Add tool response to conversation
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": content,
                        }
                    )
                except Exception as e:
                    logger.error(f"Error processing tool call {tool_name}: {str(e)}")
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps({"status": "error", "message": str(e)}),
                        }
                    )

            # Get final response from Groq with tool results
            final_response = self.groq_client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=all_tools,  # Include tools again in case followup tool calls are needed
                tool_choice="auto",  # Allow more tool calls for multi-step reasoning
            )

            # Check if there are more tool calls
            final_message = final_response.choices[0].message
            if hasattr(final_message, 'tool_calls') and final_message.tool_calls:
                # Add the assistant's follow-up response to messages
                messages.append({
                    "role": final_message.role,
                    "content": final_message.content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        } for tc in final_message.tool_calls
                    ]
                })

                # Process the additional tool calls
                for tool_call in final_message.tool_calls:
                    tool_name = tool_call.function.name
                    logger.info(f"Calling follow-up tool: {tool_name}")

                    try:
                        arguments = json.loads(tool_call.function.arguments)
                        result = await self.call_tool(tool_name, arguments)

                        if result["status"] == "success":
                            content = result["content"]
                        else:
                            content = json.dumps(result)

                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": content,
                        })
                    except Exception as e:
                        logger.error(f"Error processing follow-up tool call {tool_name}: {str(e)}")
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps({"status": "error", "message": str(e)}),
                        })

                # Final response after second round of tool calls
                final_final_response = self.groq_client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=all_tools,
                    tool_choice="none",  # Don't allow more tool calls in this final round
                )

                return final_final_response.choices[0].message.content

            return final_message.content

        # No tool calls, just return the direct response
        return assistant_message.content

    async def chat_loop(self):
        """
        Run an interactive chat loop.
        """
        print("\nMulti-Server MCP Client Started!")
        print("Type your queries or 'quit' to exit.")
        print("Type 'servers' to list connected servers.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == 'quit':
                    break

                if query.lower() == 'servers':
                    print("\nConnected servers:")
                    for server_id, server in self.servers.items():
                        print(f" - {server_id} ({server.url}): {', '.join(server.tool_names)}")
                    continue

                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                logger.error(f"Error processing query: {str(e)}")
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        """
        Clean up resources.
        """
        await self.exit_stack.aclose()


async def main():
    # Default server configurations
    default_servers = {
        "postgres": "http://localhost:8001/sse",
        "web_search": "http://localhost:8002/sse",
        "file_manager": "http://localhost:8004/sse"
    }

    # Check for command line arguments or use defaults
    import sys

    # Parse any server overrides from command line
    # Format: "server_id=url"
    servers_to_connect = default_servers.copy()
    for arg in sys.argv[1:]:
        if "=" in arg:
            server_id, url = arg.split("=", 1)
            servers_to_connect[server_id] = url

    client = MultiServerMCPClient()

    # Connect to all configured servers
    connected_any = False
    for server_id, url in servers_to_connect.items():
        print(f"Connecting to {server_id} server at {url}...")
        success = await client.connect_to_server(server_id, url)
        if success:
            connected_any = True

    if not connected_any:
        print("Failed to connect to any servers. Exiting.")
        return

    try:
        await client.chat_loop()
    except Exception as e:
        logger.error(f"Main loop error: {str(e)}")
        print(f"Error: {str(e)}")
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())