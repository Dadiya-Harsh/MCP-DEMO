# Ollama Integration Examples

This directory contains examples demonstrating the integration of MCP servers with Ollama, a tool for running large language models locally. These examples showcase how to expose Ollama models as tools within an MCP server, allowing clients to interact with them through the MCP framework.

## Contents

-   **[first.py](learning/ollama/first.py)**: A basic example of using the Ollama library to interact with a language model. This script demonstrates how to send a simple query to an Ollama model and print the response.

## Requirements

-   Python 3.7+
-   `ollama` library (install via `pip install ollama`)
-   Ollama installed and running with a model available (e.g., `gemma3`).

## Code Overview

### [first.py](learning/ollama/first.py)

This script provides a basic example of interacting with an Ollama language model. It sends a simple "Hi, how are you?" message to the `gemma3` model and prints the response. This example demonstrates the fundamental usage of the `ollama.chat` function.