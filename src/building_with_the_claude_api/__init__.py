from anthropic import Anthropic
from dotenv import load_dotenv

from .utils import Effort, add_user_message, add_assistant_message, chat

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
