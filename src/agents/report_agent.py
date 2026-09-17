from .base_agent import BaseAgent


class ReportAgent(BaseAgent):
    """Reserved for structured report generation."""

    def run(self, prompt: str) -> str:
        raise NotImplementedError
