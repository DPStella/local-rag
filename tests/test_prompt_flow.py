from pathlib import Path

from src.prompt_flow import configure_agent, handle_question


def test_handle_question_uses_agent_and_returns_answer(capsys):
    class FakeAgent:
        def run(self, prompt: str) -> str:
            assert prompt == "What is this project about?"
            return "LORP is a local RAG system."

    result = handle_question("What is this project about?", FakeAgent())
    captured = capsys.readouterr()

    assert result == "LORP is a local RAG system."
    assert "Searching the local index" in captured.out
    assert "Generating the final answer" in captured.out


def test_configure_agent_uses_expected_local_paths():
    index_path = Path("data/indexes/documents.faiss")
    metadata_path = Path("data/indexes/documents.json")
    agent = configure_agent(index_path=index_path, metadata_path=metadata_path)

    assert agent.retriever is not None
    assert agent.llm is not None
    assert getattr(agent.llm, "model", None) == "qwen3.5:4b"
