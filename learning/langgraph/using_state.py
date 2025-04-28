from typing import TypedDict
from langgraph.graph import StateGraph, START, END

"""
This example demonstrates how to use the StateGraph class to create a stateful graph.
The graph consists of three nodes, each representing a function that processes the state in some way.
The state is represented as a dictionary, and each node can read from and write to the state.
The graph is compiled and invoked with an initial state, and the final output is printed.   


State can have multiple Schemas, and the graph can be used to transform the state from one schema to another.
Nodes does the computation and can read from and write to the state.

"""

class InputState(TypedDict):
    user_input: str

class OutputState(TypedDict):
    graph_output: str

class OverallState(TypedDict):
    foo: str
    user_input: str
    graph_output: str

class PrivateState(TypedDict):
    bar: str

def node_1(state: InputState) -> OverallState:
    # Write to OverallState
    return {"foo": state["user_input"] + " name"}

def node_2(state: OverallState) -> PrivateState:
    # Read from OverallState, write to PrivateState
    return {"bar": state["foo"] + " is"}

def node_3(state: PrivateState) -> OutputState:
    # Read from PrivateState, write to OutputState
    return {"graph_output": state["bar"] + " Lance"}

builder = StateGraph(OverallState,input=InputState,output=OutputState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_2", "node_3")
builder.add_edge("node_3", END)

graph = builder.compile()
graph.invoke({"user_input":"My"})
{'graph_output': 'My name is Lance'}

graph.invoke({"user_input":"Hello"})
{'graph_output': 'Hello name is Lance'}
