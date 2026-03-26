class ToolRegistry:

    def __init__(self) -> None:
        self.tools = {}  # storage for tools, key is tool name, value is tool object

    # add a tool to registry
    def register(self, tool) -> None:
        self.tools[tool.name] = tool

    # get tool by name
    def get_tool(self, name: str):
        return self.tools.get(name)

    # run a tool
    def execute_tool(self, name: str, args: dict) -> str:
        tool = self.get_tool(name)

        if tool is None:
            return "tool could not be found"

        try:
            return tool.execute(args)
        except Exception as e:
            return f"error occurred when executing the tool: {e}"
