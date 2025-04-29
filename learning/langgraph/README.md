# LangGraph Examples

This directory contains examples that demonstrate the usage of LangGraph, a library for creating stateful, multi-actor applications. These examples showcase different ways to define agents, manage state, and build complex interaction flows.

## Contents

-   **[agent.py](agent.py)**: A basic example of a LangGraph agent. It defines the agent's state, nodes for processing input, interacting with a language model, and generating output, and then connects these nodes into a graph.
-   **[async_my_react_agent.py](async_my_react_agent.py)**: An asynchronous implementation of a ReAct agent using LangGraph. This example demonstrates how to build a more complex agent that can interact with tools and reason about its actions. The asynchronous nature allows for non-blocking operations, improving performance.
-   **[my_react_agent.py](my_react_agent.py)**: A ReAct agent implemented using LangGraph. ReAct agents are designed to reason about actions to take (Reason) and then perform them (Act). This example showcases how to define the agent's state, tools, and the graph that orchestrates the agent's behavior.
-   **[using_memory.py](using_memory.py)**: This example demonstrates how to incorporate memory into a LangGraph application. Memory allows the agent to retain information from previous interactions, enabling more context-aware and coherent conversations.
-   **[using_state.py](using_state.py)**: This example focuses on managing state within a LangGraph. It shows how to define the state schema and how to update the state as the graph executes.
-   **[react-template/](react-template/)**: A template for building ReAct agents with LangGraph. It includes the necessary files and configurations to get started quickly.
```bash
 langgraph new /your/path --template react-agent-python
```

## Requirements

-   Python 3.7+
-   `langgraph` library (install via `pip install langgraph`)
-   `langchain_groq` library (install via `pip install langchain-groq`)
-   `langchain` library (install via `pip install langchain`)
-   `dotenv` library (install via `pip install python-dotenv`)
-   `typing` library (install via `pip install typing`)
-   A Groq API key for the agent examples.

## Code Overview

### [agent.py](agent.py)

This script defines a simple LangGraph agent that takes user input, processes it with a language model, and generates an output. It showcases the basic structure of a LangGraph, including defining state, creating nodes, and connecting them to form a graph. The agent uses a Groq language model for processing the input.

### [async_my_react_agent.py](async_my_react_agent.py)

This script implements an asynchronous ReAct agent using LangGraph. It demonstrates how to define tools for the agent to use, how to create a graph that orchestrates the agent's reasoning and actions, and how to use asynchronous operations for improved performance.

### [my_react_agent.py](my_react_agent.py)

This script provides a ReAct agent implemented using LangGraph. It showcases how to define the agent's state, tools, and the graph that orchestrates the agent's behavior. ReAct agents are designed to reason about actions to take (Reason) and then perform them (Act).

### [using_memory.py](using_memory.py)

This script demonstrates how to incorporate memory into a LangGraph application. Memory allows the agent to retain information from previous interactions, enabling more context-aware and coherent conversations.

### [using_state.py](using_state.py)

This script focuses on managing state within a LangGraph. It shows how to define the state schema and how to update the state as the graph executes. State management is crucial for building complex, stateful applications with LangGraph.

### [react-template/](react-template/)

This directory provides a template for building ReAct agents with LangGraph. It includes the necessary files and configurations to get started quickly. The template likely includes examples of how to define tools, create a graph, and manage the agent's state.