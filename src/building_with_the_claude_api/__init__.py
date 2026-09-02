import os
from enum import Enum
from anthropic import Anthropic
from dotenv import load_dotenv

class Effort(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    XHIGH = "xhigh"
    MAX = "max"

def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

def chat(messages, client, system_prompt=None, effort=Effort.HIGH):
    request = {
        "model": "claude-sonnet-5",
        "max_tokens": 1024,
        "messages": messages,
        "output_config": {"effort": effort.value},
    };

    if system_prompt is not None:
        request["system"] = system_prompt

    message = client.messages.create(**request)

    return next(block.text for block in message.content if block.type == "text")

def main() -> None:
    load_dotenv()
    # print("Hello from building-with-the-claude-api!")

    client = Anthropic()
    # client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    system_prompt = "Explain to a non STEM background person so be non technical."
    messages = []
    add_user_message(messages=messages, text="what is ML vs AI engineering. Only one sentence")
    response = chat(messages=messages, client=client, system_prompt=system_prompt, effort=Effort.LOW)
    add_assistant_message(messages=messages, text=response)
    print(response)
    print("---")

    add_user_message(messages=messages, text="which one has a higher bar to braking into the field. Only one sentence")
    response = chat(messages=messages, client=client, system_prompt=system_prompt, effort=Effort.LOW)
    add_assistant_message(messages=messages, text=response)
    print(response)
    
