from .base_agent import BaseAgent


class ResearchAgent(BaseAgent):
    """Reserved for multi-step research workflows."""

    def run(self, prompt: str) -> str:
        raise NotImplementedError
