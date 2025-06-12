# This code snippet demonstrates how to use the Ollama client to interact with a model.
# It initializes a chat loop that allows users to send messages and receive responses from the model.
# Import necessary modules
import os
import asyncio
from dotenv import load_dotenv
from openai import OpenAI
import httpx  # Move this import to the top

# Load environment variables from .env file
load_dotenv()

# Correct way to instantiate OpenAI client:
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", "your_openai_api_key_here"),
    base_url=os.getenv("OPENAI_BASE_URL", "http://localhost:11434/v1")
)

model = os.getenv("OLLAMA_MODEL", "deepseek-r1:1.5b")
# Initialize with an empty conversation history
messages = []

async def chat_loop() -> None:
    """
    Function to implement AI chatbot in CLI with dynamic message history.
    """
    print(f"\nStarting chat with {model}. Type 'quit' to exit.")

    while True:
        try:
            # Get user input
            query = input("\nQuery: ").strip()

            # Check if user wants to quit
            if query.lower() == 'quit':
                print("Exiting chat...")
                break

            # Add user message to conversation history
            messages.append({
                'role': "user",
                'content': query
            })

            # Get response from the model
            response = client.chat.completions.create(
                model=model,
                messages=messages,
            )
            
            # Extract the assistant's message
            assistant_message = response.choices[0].message.content
            
            # Add assistant response to conversation history
            messages.append({
                'role': "assistant",
                'content': assistant_message
            })

            # Print the response
            print(f"\nResponse: {assistant_message}")

        except Exception as e:
            print(f"Exception {e} has occurred...")

async def discover_sse_servers(port_range=(8000, 8100), host="localhost"):
    """
    Scan localhost for running MCP servers with SSE endpoints.

    Returns:
        Dict[str, str]: Mapping of discovered server names to their SSE URLs.
    """
    discovered = {}
    for port in range(port_range[0], port_range[1] + 1):
        url = f"http://{host}:{port}/sse"
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                resp = await client.get(url, headers={"Accept": "text/event-stream"})
                # Check for MCP-specific headers or content
                if resp.status_code == 200 and "text/event-stream" in resp.headers.get("content-type", ""):
                    # Optionally, parse the first event for a server name or type
                    server_name = f"server_{port}"
                    discovered[server_name] = url
        except Exception:
            continue
    return discovered


async def interact_with_sse_server(sse_url):
    """
    Connect to an SSE server and print incoming events. (Basic demo)
    """
    print(f"\nConnecting to SSE server at {sse_url} (Ctrl+C to stop)...")
    try:
        async with httpx.AsyncClient(timeout=None) as client:
            with client.stream("GET", sse_url, headers={"Accept": "text/event-stream"}) as response:
                async for line in response.aiter_lines():
                    if line.strip():
                        print(f"[SSE] {line}")
    except Exception as e:
        print(f"Error connecting to SSE server: {e}")

async def chatgpt_style_chat():
    """
    Unified chat interface: normal messages go to Ollama, `/tool <number>` uses an MCP SSE tool.
    """
    print(f"\nChatGPT-style chat started with model '{model}'.")
    print("Type your message and press Enter.\nType '/tools' to list MCP SSE tools.\nType '/tool <number>' to connect to a tool.\nType 'quit' to exit.")
    servers = None
    while True:
        try:
            query = input("\nYou: ").strip()
            if query.lower() == 'quit':
                print("Exiting chat...")
                break
            if query == '/tools':
                print("\nDiscovering MCP SSE servers...")
                servers = await discover_sse_servers()
                if not servers:
                    print("No SSE servers found.")
                else:
                    print("Discovered servers:")
                    for idx, (name, url) in enumerate(servers.items(), 1):
                        print(f"{idx}. {name} ({url})")
                continue
            if query.startswith('/tool'):
                if not servers:
                    print("No tools discovered yet. Use /tools first.")
                    continue
                try:
                    sel_idx = int(query.split()[1]) - 1
                    sse_url = list(servers.values())[sel_idx]
                    print(f"Connecting to tool {sel_idx+1} ({sse_url})... Press Ctrl+C to stop.")
                    await interact_with_sse_server(sse_url)
                except (IndexError, ValueError):
                    print("Invalid tool number.")
                continue
            # Default: send to Ollama
            messages.append({'role': "user", 'content': query})
            response = client.chat.completions.create(
                model=model,
                messages=messages,
            )
            assistant_message = response.choices[0].message.content
            messages.append({'role': "assistant", 'content': assistant_message})
            print(f"\nOllama: {assistant_message}")
        except Exception as e:
            print(f"Exception {e} has occurred...")

if __name__ == "__main__":
    asyncio.run(chatgpt_style_chat())