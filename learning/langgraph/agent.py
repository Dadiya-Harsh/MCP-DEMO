from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from typing import Dict, Any, Annotated
from langgraph.prebuilt import create_react_agent

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
print(groq_api_key)

llm = ChatGroq(
    api_key=groq_api_key,
    model="llama-3.3-70b-versatile",
    temperature=0.0
)
class InputState(TypedDict):
    user_input: Annotated[str, "The input from the user."]

class IntermediateState(TypedDict):
    user_input: Annotated[str, "The input from the user."]
    intermediate_output: Annotated[str, "The intermediate output."]

class OutputState(TypedDict):
    user_input: Annotated[str, "The input from the user."]
    agent_response: Annotated[str, "The response from the agent."]
    graph_output: Annotated[str, "The final output."]

def input_node(state: InputState) -> IntermediateState:
    # This node does not modify the state, but it can be used to read from it if needed.
    print(f"Input node received state: {state['user_input']}")

    return{
        "user_input": state["user_input"],
        "intermediate_output": f"Processing: {state['user_input']}"
    }

def process_node(state: IntermediateState) -> OutputState:
    # This node processes the input state and modifies it.
    user_input = state["user_input"]

    response = llm.invoke(user_input)
    agent_response = response.content

    return {
        "user_input": user_input,
        "agent_response": agent_response,
        "graph_output": f"Final output: {agent_response}"
    }

def output_node(state: OutputState) -> OutputState:
    # This node generates the output state based on the input state.
    final_output = f"Final Response: state['graph_output']"

    return {
        "user_input": state["user_input"],
        "agent_response": state["agent_response"],
        "graph_output": final_output
    }


graph = StateGraph(InputState, output=OutputState)
graph.add_node("input_node", input_node)
graph.add_node("process_node", process_node)
graph.add_node("output_node", output_node)
graph.add_edge(START, "input_node")
graph.add_edge("input_node", "process_node")
graph.add_edge("process_node", "output_node")
graph.add_edge("output_node", END)

compile = graph.compile()
compile.invoke({"user_input": "Hello, world!"})

