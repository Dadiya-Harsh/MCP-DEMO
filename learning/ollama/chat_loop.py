from ollama import chat

model = "gemma3"

# Initialize with an empty conversation history
messages = []

async def chat_loop() -> None:
    """
    Function to implement AI chatbot in CLI with dynamic message history.
    """
    print(f"\nStarting chat with {model}. Type 'quit' to exit.")

    while True:
        try:
            # Get user input
            query = input("\nQuery: ").strip()

            # Check if user wants to quit
            if query.lower() == 'quit':
                print("Exiting chat...")
                break

            # Add user message to conversation history
            messages.append({
                'role': "user",
                'content': query
            })

            # Get response from the model
            response = chat(model=model, messages=messages)
            
            # Extract the assistant's message
            assistant_message = response["message"]["content"]
            
            # Add assistant response to conversation history
            messages.append({
                'role': "assistant",
                'content': assistant_message
            })

            # Print the response
            print(f"\nResponse: {assistant_message}")

        except Exception as e:
            print(f"Exception {e} has occurred...")

# To run the chat loop
if __name__ == "__main__":
    import asyncio
    asyncio.run(chat_loop())