from ollama import chat, Tool


response = chat(
    model = "gemma3",
    messages = [
        {
            'role': "user",
            'content': "Hi, how are you?"
        }
    ]
)

print(f"response type: {type(response)}")

print(f"Response : {response['message']['content']}")