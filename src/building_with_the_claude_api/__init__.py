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
    NONE = "none"

def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

def chat(messages, client, system_prompt=None, effort=Effort.LOW, stop_sequences=None, json_schema=None, model="claude-sonnet-5"):
    request = {
        "model": model,
        "max_tokens": 1024,
        "messages": messages,
        "output_config": {},
    }

    if effort not in (None, Effort.NONE):
        request["output_config"]["effort"] = effort.value

    if json_schema is not None:
        request["output_config"]["format"] = {"type": "json_schema", "schema": json_schema}

    if system_prompt is not None:
        request["system"] = system_prompt

    if stop_sequences is not None:
        request["stop_sequences"] = stop_sequences

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

