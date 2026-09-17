from dataclasses import dataclass

from src.agents.knowledge_agent import KnowledgeAgent


@dataclass
class Result:
    chunk_id: str
    text: str
    source: str


class FakeRetriever:
    def retrieve(self, query: str, top_k: int):
        return [Result("notes:0", "The project uses FAISS for vector search.", "notes.txt")]


class FakeLlm:
    def generate(self, prompt: str) -> str:
        assert "FAISS" in prompt
        assert "citation markers" in prompt
        return "FAISS is used for vector search. [1]"


def test_knowledge_agent_grounds_prompt():
    answer = KnowledgeAgent(FakeRetriever(), FakeLlm()).run("What is used for search?")
    assert answer == (
        "FAISS is used for vector search. [1]\n\n"
        "Sources:\n"
        "[1]: [notes.txt](notes.txt) (chunk notes:0)"
    )
