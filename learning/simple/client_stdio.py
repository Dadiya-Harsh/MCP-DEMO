import sys
import asyncio
import nest_asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

nest_asyncio.apply()
async def main():
    # Get the directory where client_stdio.py is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    server_path = os.path.join(current_dir, "server_stdio.py")
    
    server_params = StdioServerParameters(
        command="python",
        args=[server_path]
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream,write_stream) as session:
            await session.initialize()


            tools_result = await session.list_tools()
            print("Available Tools: ")
            for tool in tools_result.tools:
                print(f" -{tool.name}: {tool.description}")

            result = await session.call_tool("add", arguments = {"num_1": 2, "num_2":7})
            print("Result of add tool: ", result.content[0].text)

if __name__ == "__main__":
    asyncio.run(main())