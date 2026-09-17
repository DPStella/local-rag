import os
from pathlib import Path

from src.agents.knowledge_agent import KnowledgeAgent
from src.llm.embeddings import OllamaEmbeddingProvider
from src.llm.ollama_client import OllamaClient
from src.retrieval.retrievers import Retriever


def configure_agent(
    index_path: str | Path | None = None,
    metadata_path: str | Path | None = None,
    ollama_url: str | None = None,
    embedding_model: str | None = None,
    chat_model: str | None = None,
    top_k: int = 5,
) -> KnowledgeAgent:
    """Create a configured KnowledgeAgent from the local Ollama + FAISS setup."""
    agent = KnowledgeAgent(top_k=top_k)

    resolved_index = Path(index_path) if index_path is not None else Path(os.getenv("INDEX_PATH", "data/indexes/documents.faiss"))
    resolved_metadata = Path(metadata_path) if metadata_path is not None else Path(os.getenv("METADATA_PATH", "data/indexes/documents.json"))
    resolved_ollama_url = ollama_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    resolved_embedding_model = embedding_model or os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
    resolved_chat_model = chat_model or os.getenv("CHAT_MODEL", "qwen3.5:4b")

    if resolved_index.exists() and resolved_metadata.exists():
        embedder = OllamaEmbeddingProvider(resolved_ollama_url, resolved_embedding_model)
        agent.retriever = Retriever(str(resolved_index), str(resolved_metadata), embedder)
        agent.llm = OllamaClient(resolved_ollama_url, resolved_chat_model)

    return agent


def handle_question(question: str, agent: KnowledgeAgent | None = None) -> str:
    """Ask a question through the configured RAG agent."""
    active_agent = agent or configure_agent()
    if agent is None:
        if getattr(active_agent, "retriever", None) is None or getattr(active_agent, "llm", None) is None:
            raise RuntimeError("Knowledge agent dependencies are not configured")

    print("[LORP] Searching the local index...", flush=True)
    answer = active_agent.run(question)
    print("[LORP] Generating the final answer...", flush=True)
    return answer


def prompt_loop() -> None:
    """Small interactive CLI for the user-facing prompt flow."""
    agent = configure_agent()
    print("=" * 72)
    print("LORP local RAG prompt interface")
    print("Type 'exit' or 'quit' to leave. Press Enter for a new question.")
    print("=" * 72)

    while True:
        question = input("\nAsk a question: ").strip()
        if not question:
            continue
        if question.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break
        try:
            print("\n[LORP] Processing your question...\n")
            answer = handle_question(question, agent)
            print("\n[LORP] Answer:\n")
            print(answer)
        except RuntimeError as error:
            print(f"\n[LORP] Error: {error}")


if __name__ == "__main__":
    prompt_loop()
