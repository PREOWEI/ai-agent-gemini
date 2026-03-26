class MemoryManager:

    def __init__(self) -> None:
        self.history = []  # store conversation

    # add message to memory
    def add(self, role: str, message: str) -> None:
        self.history.append({
            "role": role,
            "message": message
        })

    # get full history
    def get_history(self) -> list:
        return self.history

    # clear memory if needed
    def clear(self) -> None:
        self.history = []
