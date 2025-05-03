# Ollama Integration Examples
This directory contains example scripts demonstrating the integration of Ollama, a tool for running large language models (LLMs) locally, with Python applications. These examples focus on direct interaction with Ollama models and integration with LangChain, a framework for building AI-driven applications. While the Model Context Protocol (MCP) is a framework for integrating AI models with tools and resources in a client-server architecture, these scripts do not use MCP servers, instead showcasing standalone Ollama and LangChain usage. The scripts are designed for learning, with this README rendered in an interactive browser-based playground when a script is run (e.g., via mcp dev), similar to LangGraph's development environment.

## Overview
Ollama enables local execution of LLMs, providing a lightweight alternative to cloud-based models. These examples demonstrate:

- Basic interaction with an Ollama model using the ollama library.
- Building an interactive command-line interface (CLI) for continuous chat with conversation history.
- Integrating Ollama with LangChain for structured AI interactions.

The scripts are simple, focusing on core Ollama and LangChain functionalities, making them ideal for learning how to leverage local LLMs in Python applications. Unlike other directories in the repository that use MCP for client-server tool integration, these examples are standalone, directly interfacing with the Ollama model running locally.

## Scripts in This Directory

### [first.py](first.py)
A basic script demonstrating how to send a single query to an Ollama model (gemma3) using the ollama library and print the response.

#### Function: chat (from ollama)
```python
from ollama import chat

response = chat(
    model="gemma3",
    messages=[{"role": "user", "content": "Hi, how are you?"}]
)
````

**Purpose:** Sends a chat message to an Ollama model and retrieves the response.
**Parameters:**

* `model` (str): Name of the Ollama model (e.g., gemma3).
* `messages` (list): List of message dictionaries with role and content.

**Returns:** Dictionary containing the response, with the assistant’s message in `response["message"]["content"]`.

**Usage Example:**

```python
response = chat(model="gemma3", messages=[{"role": "user", "content": "Hi, how are you?"}])
print(response["message"]["content"])  # Output: "I'm doing great, thanks for asking!"
```

#### Main Block

```python
print(f"response type: {type(response)}")
print(f"Response : {response['message']['content']}")
```

**Purpose:** Prints the response type and content for the query “Hi, how are you?”.
**Output Example:**

```
response type: <class 'dict'>
Response: I'm doing great, thanks for asking!
```

---

### [chat\_loop.py](chat_loop.py)

An asynchronous CLI chat interface with conversation history.

#### Function: chat\_loop

```python
async def chat_loop() -> None:
    """Function to implement AI chatbot in CLI with dynamic message history."""
```

**Purpose:** Runs an interactive chat loop, maintaining conversation history for context-aware responses.
**Behavior:**

* Prompts the user for input.
* Appends user and assistant messages to messages.
* Uses ollama.chat to get responses.
* Exits on “quit” input.

**Usage Example:**

```python
import asyncio
asyncio.run(chat_loop())
```

#### Main Block

```python
if __name__ == "__main__":
    import asyncio
    asyncio.run(chat_loop())
```

**Purpose:** Starts the chat loop with the gemma3 model.
**Output Example:**

```
Starting chat with gemma3. Type 'quit' to exit.
Query: Hello, what's the weather like?
Response: I don't have access to real-time weather data, but I can suggest checking a weather app! What's the next topic you'd like to explore?
Query: quit
Exiting chat...
```

---

### [langchain\_ollama\_chat.py](langchain_ollama_chat.py)

A class-based asynchronous CLI chat interface using LangChain.

#### Class: OllamaClient

```python
class OllamaClient:
    """A class to manage interactions with an Ollama model via LangChain."""
```

**Purpose:** Encapsulates a LangChain ChatOllama instance for chat interactions.
**Attributes:**

* `llm`: ChatOllama instance for the gemma3 model.
* `messages`: List to store conversation history.

#### Methods

##### **init**

```python
def __init__(self):
    """Initialize the Ollama client with a LangChain ChatOllama instance."""
```

**Purpose:** Sets up the ChatOllama LLM with the gemma3 model and a base URL.
**Usage Example:**

```python
client = OllamaClient()
print(client.llm.model)  # Output: gemma3
```

##### chat\_loop

```python
async def chat_loop(self) -> None:
    """Demonstrate the chat interface in CLI."""
```

**Purpose:** Runs an asynchronous CLI chat loop, appending user and assistant messages to history.
**Behavior:**

* Prompts for user input.
* Uses llm.ainvoke for responses.
* Exits on “quit” input.

**Usage Example:**

```python
await client.chat_loop()
```

#### Main Block

```python
if __name__ == "__main__":
    import asyncio
    cl = OllamaClient()
    asyncio.run(cl.chat_loop())
```

**Purpose:** Initializes and runs the chat loop.
**Output Example:**

```
LLM invoked with: gemma3
Starting chat with gemma3. Type 'quit' to exit.
Query: Hi, how are you?
Response: I'm doing great, thanks for asking! How about you?
Query: quit
```

---

## Expected Output

**For first.py:**

```
response type: <class 'dict'>
Response: I'm doing great, thanks for asking!
```

**For chat\_loop.py (interactive):**

```
Starting chat with gemma3. Type 'quit' to exit.
Query: What's the capital of France?
Response: The capital of France is Paris.
Query: quit
Exiting chat...
```

**For langchain\_ollama\_chat.py (interactive):**

```
LLM invoked with: gemma3
Starting chat with gemma3. Type 'quit' to exit.
Query: Tell me a joke.
Response: Why did the scarecrow become a motivational speaker? Because he was outstanding in his field!
Query: quit
```

---

## Learning with the Playground

The interactive playground enhances learning by:

* Rendering This README: Provides context and detailed documentation.
* Interactive Exploration: May allow running scripts, viewing outputs, or editing code in the browser.
* Guided Learning: Demonstrates direct Ollama and LangChain usage, serving as a foundation for extending to MCP-based applications.

To explore, run a script using the repository’s custom command (e.g., mcp dev). The playground will display this README and potentially offer interactive features.

---

## Troubleshooting

* **Ollama Not Running:** Ensure Ollama is installed and running locally (ollama run gemma3). Check the base URL ([http://localhost:11434](http://localhost:11434)) in langchain\_ollama\_chat.py.
* **Model Not Found:** Verify the gemma3 model is pulled (ollama pull gemma3).
* **LangChain Errors:** Ensure langchain-ollama is installed and compatible with your Python version.
* **Playground Not Loading:** Consult the repository’s main documentation for the correct mcp dev command.
* **Conversation History Issues:** For chat\_loop.py and langchain\_ollama\_chat.py, ensure inputs are processed correctly; clear messages if context becomes inconsistent.

---

## License

This project is licensed under the MIT License. See the LICENSE file in the repository root for details.
