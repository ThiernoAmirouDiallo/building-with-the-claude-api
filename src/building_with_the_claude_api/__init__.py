import os
from anthropic import Anthropic
from dotenv import load_dotenv

def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

def chat(messages, client):
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=messages
    )
    return message.content[0].text

def main() -> None:
    load_dotenv()
    # print("Hello from building-with-the-claude-api!")

    client = Anthropic()
    # client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    messages = []
    add_user_message(messages=messages, text="what is ML vs AI engineering. Only one sentence")
    response = chat(messages=messages, client=client)
    add_assistant_message(messages=messages, text=response)
    print(response)

    add_user_message(messages=messages, text="which one has a higher bar to braking into the field. Only one sentence")
    response = chat(messages=messages, client=client)
    add_assistant_message(messages=messages, text=response)
    print(response)
    
