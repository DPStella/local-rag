import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.agents.knowledge_agent import KnowledgeAgent
from src.llm.ollama_client import OllamaClient
from src.llm.embeddings import OllamaEmbeddingProvider
from src.retrieval.retrievers import Retriever

app = FastAPI(title="Enterprise RAG Agent Platform")
agent = KnowledgeAgent()


class QueryRequest(BaseModel):
    question: str = Field(min_length=1)


class QueryResponse(BaseModel):
    answer: str


def configure_agent() -> None:
    index_path = Path(os.getenv("INDEX_PATH", "data/indexes/documents.faiss"))
    metadata_path = Path(os.getenv("METADATA_PATH", "data/indexes/documents.json"))
    if not index_path.exists() or not metadata_path.exists():
        return

    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    embedding_model = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
    chat_model = os.getenv("CHAT_MODEL", "qwen2.5:14b")
    embedder = OllamaEmbeddingProvider(ollama_url, embedding_model)
    agent.retriever = Retriever(str(index_path), str(metadata_path), embedder)
    agent.llm = OllamaClient(ollama_url, chat_model)


configure_agent()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
def ready() -> dict[str, str]:
    if agent.retriever is None or agent.llm is None:
        raise HTTPException(status_code=503, detail="Index or Ollama configuration is unavailable")
    return {"status": "ready"}


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest) -> QueryResponse:
    try:
        return QueryResponse(answer=agent.run(request.question))
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
