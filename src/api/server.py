from fastapi import FastAPI
from pydantic import BaseModel

from src.agents.knowledge_agent import KnowledgeAgent

app = FastAPI(title="Enterprise RAG Agent Platform")
agent = KnowledgeAgent()


class QueryRequest(BaseModel):
    question: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/query")
def query(request: QueryRequest) -> dict[str, str]:
    return {"answer": agent.run(request.question)}
