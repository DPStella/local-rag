class BaseAgent:
    """Base interface for LORP agents."""

    def run(self, prompt: str) -> str:
        raise NotImplementedError
