from dataclasses import dataclass

from src.agents.knowledge_agent import KnowledgeAgent


@dataclass
class Result:
    chunk_id: str
    text: str


class FakeRetriever:
    def retrieve(self, query: str, top_k: int):
        return [Result("notes:0", "The project uses FAISS for vector search.")]


class FakeLlm:
    def generate(self, prompt: str) -> str:
        assert "FAISS" in prompt
        return "FAISS is used for vector search."


def test_knowledge_agent_grounds_prompt():
    answer = KnowledgeAgent(FakeRetriever(), FakeLlm()).run("What is used for search?")
    assert answer == "FAISS is used for vector search."
