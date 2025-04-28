from langchain_groq import ChatGroq
from dotenv import load_dotenv  
import os
from langgraph.graph import StateGraph, START, END
from typing import Annotated, TypedDict, List, Dict, Any
import asyncio
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
from langchain_core.messages import AIMessage, HumanMessage
from mcp.client.sse import sse_client
from mcp.types import Tool



# Load environment variables
load_dotenv()

# Initialize LLM with async capabilities
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.0, groq_api_key=os.getenv("GROQ_API_KEY"))

async def get_mcp_tools():
    """Get available tools from the MCP server."""

    # using stdio_client to connect to the server
    # server_params = StdioServerParameters(
    #     command="python",
    #     args=["server.py"]
    # )
    
    # # The stdio_client yields a tuple of (read_stream, write_stream)
    # # We need to create a ClientSession with these streams
    # async with stdio_client(server_params) as streams:
    #     read_stream, write_stream = streams
    #     session = ClientSession(read_stream, write_stream)
    #     await session.initialize()
    #     tools_result = await session.list_tools()
    #     return tools_result.tools


    # Using sse_client to connect to the server
    async with sse_client("http://localhost:8050/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()
            
            # List available tools
            tools_result = await session.list_tools()
            return tools_result.tools

class ChatState(TypedDict):
    messages: List[Any]  # Store conversation history
    available_tools: List[Tool] # Store tool descriptions
    current_tool: Tool  # Store current tool being used
    tool_result: str  # Store tool execution result

async def start_node(state: ChatState) -> ChatState:
    """Start node function to initialize the chat state."""
    tools = await get_mcp_tools()
    
    return {
        "messages": state["messages"],
        "available_tools": tools,
        "current_tool": None,
        "tool_result": ""
    }

async def react_agent_plan(state: ChatState) -> dict:
    """React agent function to process user input and generate a response."""
    # Format the prompt with tools information
    tools_description = "\n".join([f"- {tool.name}: {tool.description}" 
                                  for tool in state["available_tools"]])
    
    # Add system instruction to guide ReAct format
    system_prompt = (
        "You are an assistant that follows the ReAct framework (Reasoning and Acting). "
        f"You have access to these tools:\n{tools_description}\n\n"
        "Format your response as follows:\n"
        "Thought: <your reasoning>\n"
        "Action: <tool_name or 'Final Answer'>\n"
        "Action Input: <tool input or final response>"
    )
    
    # Use the LLM to generate a response 
    response = await llm.ainvoke([
        HumanMessage(content=system_prompt),
        *state["messages"]
    ])
    
    # Extract the action from the response
    response_text = response.content
    if "Action:" in response_text and "Action Input:" in response_text:
        # Extract the action and action input
        action_part = response_text.split("Action:")[1].split("Action Input:")[0].strip()
        action_input = response_text.split("Action Input:")[1].strip()
        
        # Determine if this is a final answer or tool use
        if action_part.lower() == "final answer":
            return {
                "messages": state["messages"] + [AIMessage(content=action_input)],
                "available_tools": state["available_tools"],
                "current_tool": None,
                "tool_result": "",
                "next": "react_agent_end"  # Go to end
            }
        else:
            # Look up the tool by name
            matching_tools = [t for t in state["available_tools"] if t["name"].lower() == action_part.lower()]
            if matching_tools:
                return {
                    "messages": state["messages"] + [AIMessage(content=response_text)],
                    "available_tools": state["available_tools"],
                    "current_tool": matching_tools[0],
                    "tool_result": "",
                    "next": "react_agent_tool"  # Go to tool execution
                }
    
    # If we can't extract a valid action, just respond directly
    return {
        "messages": state["messages"] + [AIMessage(content=response_text)],
        "available_tools": state["available_tools"],
        "current_tool": None,
        "tool_result": "",
        "next": "react_agent_end"  # Go to end
    }

async def react_agent_tool(state: ChatState) -> ChatState:
    """Tool function to execute the selected tool."""
    tool = state["current_tool"]
    
    # Extract tool input from the last message
    last_message = state["messages"][-1].content
    tool_input = last_message.split("Action Input:")[1].strip() if "Action Input:" in last_message else ""
    
    # Execute the tool
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )
    tool_result = "Tool execution placeholder"  # Default value
    
    try:
        async with stdio_client(server_params) as session:
            await session.initialize()
            # Call the tool with the input
            tool_response = await session.call_tool(
                tool_name=tool["name"],
                tool_input=tool_input
            )
            tool_result = tool_response.tool_result
    except Exception as e:
        tool_result = f"Error executing tool: {str(e)}"
    
    # Add the observation to the state
    observation = f"Observation: {tool_result}"
    
    return {
        "messages": state["messages"] + [HumanMessage(content=observation)],
        "available_tools": state["available_tools"],
        "current_tool": None,
        "tool_result": tool_result,
        "next": "react_agent_plan"  # Go back to planning
    }

async def react_agent_end(state: ChatState) -> ChatState:
    """End node function to finalize the chat state."""
    return state

# Create async state graph
async_graph = StateGraph(ChatState)
async_graph.add_node("start", start_node)
async_graph.add_node("react_agent_plan", react_agent_plan)    
async_graph.add_node("react_agent_tool", react_agent_tool)
async_graph.add_node("react_agent_end", react_agent_end)

# Add edges
async_graph.add_edge(START, "start")
async_graph.add_edge("start", "react_agent_plan")

# Add conditional edges based on the "next" field in the state
async_graph.add_conditional_edges(
    "react_agent_plan",
    lambda state: state["next"]
)

async_graph.add_edge("react_agent_tool", "react_agent_plan")
async_graph.add_edge("react_agent_end", END)

# Compile the async graph
async_app = async_graph.compile()

# Run the async graph
async def main():
    result = await async_app.ainvoke({
        "messages": [HumanMessage(content="Write an example of a recursive function in Python")]
    })
    
    # Print the final conversation
    for message in result["messages"]:
        if isinstance(message, HumanMessage):
            print(f"Human: {message.content}")
        else:
            print(f"AI: {message.content}")

# # Run the async main function
if __name__ == "__main__":
    asyncio.run(main())