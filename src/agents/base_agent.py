class BaseAgent:
    """Base interface for ERAP agents."""

    def run(self, prompt: str) -> str:
        raise NotImplementedError
