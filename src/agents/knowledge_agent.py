from .base_agent import BaseAgent


class KnowledgeAgent(BaseAgent):
    """RAG-powered question-answering agent."""

    def run(self, prompt: str) -> str:
        return f"Knowledge agent is not configured yet: {prompt}"
