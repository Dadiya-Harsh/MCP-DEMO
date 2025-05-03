# Ollama Integration Examples

This directory contains examples demonstrating the integration of MCP servers with Ollama, a tool for running large language models locally. These examples showcase how to expose Ollama models as tools within an MCP server, allowing clients to interact with them through the MCP framework.

## Contents

-   **[first.py](first.py)**: A basic example of using the Ollama library to interact with a language model. This script demonstrates how to send a simple query to an Ollama model and print the response.

-   **[chat_loop.py](chat_loop.py)**: An implementation of an interactive chat loop using Ollama. This example shows how to maintain conversation history and create an interactive CLI chat interface.

-   **[langchain_2.py](langchain_2.py)**: Demonstrates integration between LangChain and Ollama. Shows how to use the ChatOllama class for simple one-shot interactions.

-   **[langchain_ollama_chat.py](langchain_ollama_chat.py)**: A more sophisticated example combining LangChain with Ollama in an object-oriented approach. Implements a chat interface with message history management.

## Requirements

-   Python 3.7+
-   `ollama` library (install via `pip install ollama`)
-   Ollama installed and running with a model available (e.g., `gemma3`).

## Code Overview

### [first.py](learning/ollama/first.py)
This script provides a basic example of interacting with an Ollama language model. It sends a simple "Hi, how are you?" message to the `gemma3` model and prints the response. This example demonstrates the fundamental usage of the `ollama.chat` function.

### [chat_loop.py](learning/ollama/chat_loop.py)
An asynchronous implementation of a chat interface using Ollama directly. It maintains a conversation history and provides a command-line interface for interactive chat sessions with the model.

### [langchain_2.py](learning/ollama/langchain_2.py)
Demonstrates how to use LangChain's ChatOllama class for simple interactions with Ollama models. This script shows the basic setup and usage of LangChain with Ollama integration.

### [langchain_ollama_chat.py](learning/ollama/langchain_ollama_chat.py)
A comprehensive example that combines LangChain and Ollama in a class-based structure. Features:
- Asynchronous chat loop implementation
- Message history management
- Temperature control for response generation
- Command-line interface for interactive sessions

## Usage Examples

### Basic Usage
```python
from ollama import chat

response = chat(
    model="gemma3",
    messages=[{"role": "user", "content": "Hi, how are you?"}]
)
```

### LangChain Integration
```python
from langchain_ollama import ChatOllama

llm = ChatOllama(model="gemma3", base_url="http://localhost:11434/")
response = llm.invoke("Hi")
```

### Interactive Chat
```python
from langchain_ollama_chat import OllamaClient

client = OllamaClient()
asyncio.run(client.chat_loop())