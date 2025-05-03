from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()


class OllamaClient:
    """
    It is just class which 
    """
    def __init__(self):
        self.llm = ChatOllama(
            model =  "gemma3",
            base_url="http://localhost:11434/",
            temperature = 1
        ) 
        print(f"LLM invoked with: {self.llm.model}")
        self.messages = []

    async def chat_loop(self) -> None:
        """
        It is just function to demonstrtae the chat interface in cli..
        Args:
            llm: it is an object chatollama class, provides an interface for ollama models.
        """ 
        print(f"\nStarting chat with {self.llm.model}. Type 'quit' to exit.")

        while True:
            user_input = input("\nQuery: ")
            if user_input.lower() == 'quit':
                break
            self.messages.append(
                [f"{user_input}"]
            )

            response = await self.llm.ainvoke(user_input)
            

            print(f"\nResponse: {response.content}")

            self.messages.append(
                [f"{response.content}"]
            )

# async def main():
#     cl = OllamaClient()
#     await cl.chat_loop()

if __name__ == '__main__':
    import asyncio
    cl = OllamaClient()

    asyncio.run(cl.chat_loop())








