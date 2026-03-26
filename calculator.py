from tools.base import BaseTool

class CalculatorTool(BaseTool):

    def __init__(self) -> None:
        super().__init__("calculator", "a simple calculator for basic math operations")

    def execute(self, args: dict) -> str:
        try:
            exp = args.get("expression")  # get the math expression
            if exp is None:
                return "expression is not provided"

            answer = eval(exp)  # calculate it
            return str(answer)

        except Exception as e:
            return f"calculation error: {e}"

    def get_declaration(self) -> dict:
        return {
            "name": "calculator",
            "description": "use this to do basic math calculations like addition, subtraction, multiplication, division. just give it a math expression as a string and it will return the answer",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "math input as a string, for example '2 + 2' or '5 * (3 - 1)'"
                    }
                },
                "required": ["expression"]
            }
        }
