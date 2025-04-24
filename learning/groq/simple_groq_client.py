import json

from groq import Groq
import os
from dotenv import load_dotenv
from typing import Optional, Any
from contextlib import AsyncExitStack
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


load_dotenv()

class SimpleGroqClient:
    """Client for interacting with groq models using MCP tools."""

    def __init__(self):
        """
        Initialize the groq client.
        """
        self.stdio = None
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.stdio: Optional[Any] = None
        self.write: Optional[Any] = None

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server

        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    async def process_query(self, query: str) -> str:
        """Process a query using Groq API and available tools"""
        messages = [
            {
                "role": "user",
                "content": query
            }
        ]

        # Initialize Groq client (assuming it's set up in self.groq)
        response = await self.session.list_tools()
        available_tools = [{
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema
            }
        } for tool in response.tools]

        # Initial Groq API call
        response = self.groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=available_tools,
            max_tokens=1000
        )

        # Process response and handle tool calls
        final_text = []
        assistant_message_content = []

        # Groq API returns choices with message content
        message = response.choices[0].message

        if message.content:
            final_text.append(message.content)
            assistant_message_content.append({"type": "text", "text": message.content})

        # Handle tool calls
        if hasattr(message, 'tool_calls') and message.tool_calls:
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                # Execute tool call
                result = await self.session.call_tool(tool_name, tool_args)
                final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")

                assistant_message_content.append({
                    "type": "tool_use",
                    "id": tool_call.id,
                    "name": tool_name,
                    "input": tool_args
                })

                messages.append({
                    "role": "assistant",
                    "content": assistant_message_content
                })
                messages.append({
                    "role": "tool",
                    "content": json.dumps({
                        "tool_call_id": tool_call.id,
                        "result": result.content
                    })
                })

                # Get next response from Groq
                response = self.groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    tools=available_tools,
                    max_tokens=1000
                )

                final_text.append(response.choices[0].message.content)

        return "\n".join(final_text)

    async def chat_loop(self):
        """Run an interactive chat loop"""
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
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()


async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)

    client = SimpleGroqClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    import sys
    asyncio.run(main())