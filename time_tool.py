from tools.base import BaseTool
from datetime import datetime

class TimeTool(BaseTool):

    def __init__(self) -> None:
        super().__init__("time", "get current date and time")

    def execute(self, args: dict) -> str:
        try:
            now = datetime.now()  # get current date and time
            return now.strftime("%A, %d %B %Y - %H:%M")  # format nicely
        except Exception as e:
            return f"time error: {e}"

    def get_declaration(self) -> dict:
        return {
            "name": "time",
            "description": "get current date and time",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
