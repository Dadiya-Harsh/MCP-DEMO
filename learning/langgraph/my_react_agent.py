from langchain_groq import ChatGroq
from dotenv import load_dotenv  
import os
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, START, END
from typing import Annotated, TypedDict

load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.0, groq_api_key=os.getenv("GROQ_API_KEY"))

class ChatState(TypedDict):
    user_input: Annotated[str, "User input"]
    assistant_output: Annotated[str, "Assistant output"]
    plan: Annotated[str, "Plan"]
    tools: Annotated[str, "Tools"]

def start_node(state: ChatState) -> ChatState:
    """Start node function to initialize the chat state."""
    return ChatState(
        user_input=state["user_input"],
        assistant_output="",
        plan="",
        tools=""
    )


def react_agent_plan(state: ChatState) -> ChatState:
    """React agent function to process user input and generate a response."""
    # Use the LLM to generate a response based on the user input and state
    response = llm.invoke(state["user_input"])
    return ChatState(
        user_input=state["user_input"],
        assistant_output=response,
        plan="",
        tools=""
    )

def react_agent_tool(state: ChatState) -> ChatState:
    """Tool function to process the response and update the state."""
    # Process the response and update the state as needed
    # For example, you might want to extract information from the response or perform actions based on it
    return ChatState(
        user_input=state["user_input"],
        assistant_output=state["assistant_output"],
        plan="",
        tools=""
    )

def react_agent_end(state: ChatState) -> ChatState: 
    """End node function to finalize the chat state."""
    # Perform any final actions or cleanup before ending the chat
    return ChatState(
        user_input=state["user_input"],
        assistant_output=state["assistant_output"],
        plan="",
        tools=""
    )

graph = StateGraph(ChatState)
graph.add_node("start", start_node)
graph.add_node("react_agent_plan", react_agent_plan)    
graph.add_node("react_agent_tool", react_agent_tool)
graph.add_node("react_agent_end", react_agent_end)
graph.add_edge(START, "start")
graph.add_edge("start", "react_agent_plan")
graph.add_edge("react_agent_plan", "react_agent_tool")
graph.add_edge("react_agent_tool", "react_agent_end")
graph.add_edge("react_agent_end", END)
compile = graph.compile()

ans =compile.invoke({
    "user_input": "write an example of recursive function in python"
})
print(ans["assistant_output"].content)

