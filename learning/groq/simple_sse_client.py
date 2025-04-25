import json
from typing import Any, Dict, List, Optional
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

class SimpleGroqClient:
    """Client for interacting with Groq models using MCP tools over SSE transport."""

    def __init__(self):
        """
        Initialize the Groq client.
        """
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.read_stream: Optional[Any] = None
        self.write_stream: Optional[Any] = None

    async def connect_to_server(self, server_url: str = "http://localhost:8002/sse"):
        """
        Connect to an MCP server using SSE transport.

        Args:
            server_url: URL of the MCP server's SSE endpoint (e.g., "http://localhost:8002/sse")
        """
        logger.info(f"Connecting to MCP server at {server_url}")
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
            self.read_stream, self.write_stream = sse_transport

            # Initialize ClientSession with SSE streams
            self.session = await self.exit_stack.enter_async_context(
                ClientSession(self.read_stream, self.write_stream)
            )
            await self.session.initialize()

            # List available tools
            response = await self.session.list_tools()
            tools = response.tools
            logger.info("Connected to server with tools: %s", [tool.name for tool in tools])
            print("\nConnected to server with tools:", [tool.name for tool in tools])
        except Exception as e:
            logger.error(f"Failed to connect to server: {str(e)}")
            raise

    async def get_mcp_tools(self) -> List[Dict[str, Any]]:
        """
        Get available tools from the MCP server in Groq format.

        Returns:
            A list of tools in Groq format.
        """
        if not self.session:
            raise ValueError("Client is not connected to a server")

        tools_result = await self.session.list_tools()
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema,
                },
            }
            for tool in tools_result.tools
        ]

    async def process_query(self, query: str) -> str:
        """
        Process a query using Groq and available MCP tools.

        Args:
            query: The user query.

        Returns:
            The response from Groq.
        """
        if not self.session:
            raise ValueError("Client is not connected to a server")

        # Get available tools
        tools = await self.get_mcp_tools()

        # Initial Groq API call
        response = self.groq_client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": query}],
            tools=tools,
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
                ]
            }
        ]

        # Handle tool calls if present
        if assistant_message.tool_calls:
            # Process each tool call
            for tool_call in assistant_message.tool_calls:
                logger.info(f"Calling tool: {tool_call.function.name}")
                try:
                    # Execute tool call
                    result = await self.session.call_tool(
                        tool_call.function.name,
                        arguments=json.loads(tool_call.function.arguments),
                    )
                    # Add tool response to conversation
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": result.content[0].text,
                        }
                    )
                except Exception as e:
                    logger.error(f"Error calling tool {tool_call.function.name}: {str(e)}")
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
                tools=tools,
                tool_choice="none",  # Don't allow more tool calls
            )

            return final_response.choices[0].message.content

        # No tool calls, just return the direct response
        return assistant_message.content

    async def chat_loop(self):
        """
        Run an interactive chat loop.
        """
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == 'quit':
                    break

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
    import sys
    if len(sys.argv) < 2:
        server_url = "http://localhost:8002/sse"  # Default URL
        print(f"Using default server URL: {server_url}")
    else:
        server_url = sys.argv[1]
        print(f"Using server URL: {server_url}")

    client = SimpleGroqClient()
    try:
        await client.connect_to_server(server_url)
        await client.chat_loop()
    except Exception as e:
        logger.error(f"Main loop error: {str(e)}")
        print(f"Error: {str(e)}")
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())