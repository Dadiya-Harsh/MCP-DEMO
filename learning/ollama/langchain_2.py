from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

llm = ChatOllama(model = "gemma3", base_url="http://localhost:11434/")

response = llm.invoke("Hi")


print(f"Response: {response.content}")