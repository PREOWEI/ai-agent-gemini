import os
import time

from agent import Agent
from tools.calculator import CalculatorTool
from tools.time_tool import TimeTool
from dotenv import load_dotenv
from tools.currency_tool import CurrencyTool
from tools.dictionary_tool import DictionaryTool
# simple loading bar
def loading() -> None:
    print("Starting Agent...", end="", flush=True)
    for i in range(5):
        percent = (i + 1) * 20
        print(f"\rStarting Agent... {percent}%", end="", flush=True)
        time.sleep(0.3)
    print(" done")


def main() -> None:
    load_dotenv()  # load .env file

    key = os.getenv("GEMINI_API_KEY")

    # check if key exists
    if key is None:
        print("No API key found. Check your .env file.")
        return
    else:
        print("API key loaded")

    loading()  # show progress

    agent = Agent()

    # register tools
    agent.registry.register(CalculatorTool())
    agent.registry.register(TimeTool())
    agent.registry.register(CurrencyTool())
    agent.registry.register(DictionaryTool())

    print("Agent started (type 'exit' to stop)")

    while True:
        user_input = input("You: ")

        if user_input.strip().lower() == "exit":
            break

        response = agent.handle_input(user_input)
        print("Agent:", response)


if __name__ == "__main__":
    main()
