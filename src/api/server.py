import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, Field

from src.agents.knowledge_agent import KnowledgeAgent
from src.llm.ollama_client import OllamaClient
from src.llm.embeddings import OllamaEmbeddingProvider
from src.retrieval.retrievers import Retriever

app = FastAPI(title="Local Open RAG Platform (LORP)")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
agent = KnowledgeAgent()


class QueryRequest(BaseModel):
    question: str = Field(min_length=1)


class QueryResponse(BaseModel):
    answer: str
    sources: list[dict[str, str]] = Field(default_factory=list)
    metrics: dict[str, float | int] = Field(default_factory=dict)


def configure_agent() -> None:
    index_path = Path(os.getenv("INDEX_PATH", "data/indexes/documents.faiss"))
    metadata_path = Path(os.getenv("METADATA_PATH", "data/indexes/documents.json"))
    if not index_path.exists() or not metadata_path.exists():
        return

    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    embedding_model = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
    chat_model = os.getenv("CHAT_MODEL", "qwen3.5:4b")
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
        if hasattr(agent, "run_with_metrics"):
            answer, results, metrics = agent.run_with_metrics(request.question)
        elif hasattr(agent, "run_with_sources"):
            answer, results = agent.run_with_sources(request.question)
            metrics = {}
        else:
            answer, results = agent.run(request.question), []
            metrics = {}
        sources = []
        source_numbers: dict[str, int] = {}
        for result in results:
            source = str(getattr(result, "source", result.chunk_id))
            source_numbers.setdefault(source, len(source_numbers) + 1)
            if source_numbers[source] != len(sources) + 1:
                continue
            sources.append(
                {
                    "number": str(source_numbers[source]),
                    "source": source,
                    "chunk": result.chunk_id,
                }
            )
        return QueryResponse(answer=answer, sources=sources, metrics=metrics)
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error


@app.get("/source")
def source(path: str) -> FileResponse:
    requested_path = Path(path)
    if not requested_path.is_absolute():
        requested_path = Path.cwd() / requested_path
    resolved_path = requested_path.resolve()

    allowed_sources = {
        Path(item["source"]).resolve()
        for item in (agent.retriever.metadata if agent.retriever is not None else [])
    }
    if resolved_path not in allowed_sources or not resolved_path.is_file():
        raise HTTPException(status_code=404, detail="Indexed source not found")
    return FileResponse(resolved_path)


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    return HTMLResponse(
        """
        <html>
            <head>
                <title>LORP Demo</title>
                <style>
                    body { font-family: Arial, sans-serif; max-width: 900px; margin: 48px auto; padding: 0 24px; background: #0f172a; color: #e2e8f0; }
                    textarea { width: 100%; min-height: 120px; margin-top: 12px; border-radius: 10px; padding: 12px; font-size: 16px; }
                    button { background: #22c55e; color: #06210f; border: none; padding: 12px 18px; border-radius: 10px; font-weight: bold; cursor: pointer; }
                    #answer { margin-top: 24px; background: #111827; padding: 18px; border-radius: 12px; line-height: 1.65; }
                    #sources { margin-top: 16px; background: #172033; padding: 14px 18px; border-radius: 10px; }
                    #sources:empty { display: none; }
                    #sources h2 { font-size: 15px; margin: 0 0 8px; }
                    #sources a { color: #93c5fd; }
                    #metrics { margin-top: 12px; color: #94a3b8; font-size: 13px; }
                    .status { color: #93c5fd; margin-bottom: 10px; }
                </style>
            </head>
            <body>
                <h1>LORP Demo</h1>
                <div class="status" id="status">Idle</div>
                <textarea id="question" placeholder="Ask about the project or indexed documents...">What is this project about?</textarea>
                <div><button onclick="ask()">Ask LORP</button></div>
                <div id="answer">Waiting for a question...</div>
                <div id="sources"></div>
                <div id="metrics"></div>
                <script>
                    async function ask() {
                        const question = document.getElementById('question').value.trim();
                        const status = document.getElementById('status');
                        const answer = document.getElementById('answer');
                        const sources = document.getElementById('sources');
                        const metrics = document.getElementById('metrics');
                        if (!question) {
                            answer.textContent = 'Please enter a question.';
                            return;
                        }
                        status.textContent = 'Searching the local index...';
                        answer.textContent = 'Thinking...';
                        sources.replaceChildren();
                        metrics.textContent = '';
                        try {
                            const response = await fetch('/query', {
                                method: 'POST',
                                headers: {'Content-Type': 'application/json'},
                                body: JSON.stringify({ question })
                            });
                            const data = await response.json();
                            if (!response.ok) {
                                throw new Error(data.detail || 'Request failed');
                            }
                            status.textContent = 'Answer ready';
                            renderAnswer(data.answer);
                            renderMetrics(data.metrics);
                            if (data.sources && data.sources.length) {
                                const heading = document.createElement('h2');
                                heading.textContent = 'Sources';
                                sources.appendChild(heading);
                                data.sources.forEach((item) => {
                                    const link = document.createElement('a');
                                    link.href = '/source?path=' + encodeURIComponent(item.source);
                                    link.target = '_blank';
                                    link.rel = 'noreferrer';
                                    link.textContent = '[' + item.number + '] ' + item.source;
                                    sources.appendChild(link);
                                    sources.appendChild(document.createElement('br'));
                                });
                            }
                        } catch (error) {
                            status.textContent = 'Error';
                            answer.textContent = error.message;
                        }
                    }

                    function renderMetrics(data) {
                        if (!data || data.workflow_ms === undefined) {
                            return;
                        }
                        const parts = [
                            'Workflow ' + (data.workflow_ms / 1000).toFixed(2) + 's',
                            'Retrieval ' + Number(data.retrieval_ms || 0).toFixed(0) + 'ms',
                            'Generation ' + Number(data.generation_ms || 0).toFixed(0) + 'ms'
                        ];
                        if (data.total_tokens !== undefined) {
                            parts.push('Tokens ' + data.total_tokens + ' (' + data.prompt_tokens + ' in / ' + data.completion_tokens + ' out)');
                        }
                        if (data.tokens_per_second !== undefined) {
                            parts.push(data.tokens_per_second.toFixed(1) + ' tokens/s');
                        }
                        metrics.textContent = parts.join('  |  ');
                    }

                    function renderAnswer(text) {
                        answer.replaceChildren();
                        const citationPattern = /((?:\[\d+(?:\s*,\s*\d+)*\])+)/g;
                        text.split(/\\r?\\n/).forEach((line, lineIndex, lines) => {
                            line = line.replace(/^\s*[-*]\s+/, '• ');
                            let cursor = 0;
                            let match;
                            while ((match = citationPattern.exec(line)) !== null) {
                                appendInlineText(answer, line.slice(cursor, match.index));
                                match[0].match(/\d+(?:\s*,\s*\d+)*/g).forEach((number) => {
                                    const superscript = document.createElement('sup');
                                    superscript.textContent = number.replace(/\s+/g, '');
                                    answer.appendChild(superscript);
                                });
                                const afterCitation = line.slice(match.index + match[0].length);
                                const punctuation = afterCitation.match(/^[.,!?;:]/);
                                if (punctuation) {
                                    appendInlineText(answer, punctuation[0]);
                                    cursor = match.index + match[0].length + punctuation[0].length;
                                } else {
                                    cursor = match.index + match[0].length;
                                }
                                answer.appendChild(document.createElement('br'));
                                answer.appendChild(document.createElement('br'));
                            }
                            appendInlineText(answer, line.slice(cursor));
                            if (lineIndex < lines.length - 1 && cursor === 0) {
                                answer.appendChild(document.createElement('br'));
                            }
                        });
                    }

                    function appendInlineText(parent, text) {
                        const boldPattern = /\*\*(.+?)\*\*/g;
                        let cursor = 0;
                        let match;
                        while ((match = boldPattern.exec(text)) !== null) {
                            parent.appendChild(document.createTextNode(text.slice(cursor, match.index)));
                            const bold = document.createElement('strong');
                            bold.textContent = match[1];
                            parent.appendChild(bold);
                            cursor = match.index + match[0].length;
                        }
                        parent.appendChild(document.createTextNode(text.slice(cursor)));
                    }
                </script>
            </body>
        </html>
        """
    )
