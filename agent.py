import os
from google import genai
from google.genai import types # type: ignore

from dotenv import load_dotenv
load_dotenv()
from tool_registry import ToolRegistry
from memory import MemoryManager


class Agent:

    def __init__(self) -> None:
        self.memory = MemoryManager()
        self.registry = ToolRegistry()

        # setup gemini
        api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.5-flash"

        # main function
    def handle_input(self, user_input: str) -> str:
        self.memory.add("user", user_input)

        try:
            formatted_history = self.format_memory()

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=formatted_history,
                config=types.GenerateContentConfig(
                    tools=self.get_tools_schema()
                )
            )

            if hasattr(response, "function_calls") and response.function_calls:
                call = response.function_calls[0]
                name = call.name
                args = dict(call.args)

                result = self.registry.execute_tool(name, args)
                observe_prompt = (
                    formatted_history
                    + "\n\n"
                    + f"Tool used: {name}\n"
                    + f"Tool result: {result}\n\n"
                    + "Use this tool result to answer the user's last message clearly. Keep the answer short and plain. Do not use markdown."
                )

                final_response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=observe_prompt
                )

                final_text = getattr(final_response, "text", None)
                if final_text:
                    self.memory.add("agent", final_text)
                    return final_text

                self.memory.add("agent", result)
                return result

            text = getattr(response, "text", None)
            if text:
                self.memory.add("agent", text)
                return text

            if hasattr(response, "candidates") and response.candidates:
                parts = response.candidates[0].content.parts
                if parts:
                    first = parts[0]
                    if hasattr(first, "text") and first.text:
                        self.memory.add("agent", first.text)
                        return first.text

            return "no valid response"

        except Exception as e:
            return f"error: {e}"

    def format_memory(self) -> str:
        history = self.memory.get_history()
        lines = []

        for item in history:
            role = item["role"]
            message = item["message"]
            if role == "user":
                lines.append(f"{role}: {message}")

        instruction = "Use the conversation below to remember user details and answer questions based on it. Use the available tools whenever a tool matches the user's request, especially for dictionary, calculator, currency, and time questions."
        return instruction + "\n\n" + "\n".join(lines)
        
        
    # collect all tool schemas
    def get_tools_schema(self) -> list:
        declarations = []
        for tool in self.registry.tools.values():
            declarations.append(tool.get_declaration())
        return [types.Tool(function_declarations=declarations)]
