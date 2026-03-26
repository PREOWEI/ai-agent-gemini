from abc import ABC, abstractmethod

# this is like a template for all tools
class BaseTool(ABC):

    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description

    # what the tool will actually do
    @abstractmethod
    def execute(self, args: dict) -> str:
        pass

    # this tells the AI how to use the tool
    @abstractmethod
    def get_declaration(self) -> dict:
        pass
