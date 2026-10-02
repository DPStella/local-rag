# Local Open RAG Platform (LORP)
_Local-first RAG prototype using Ollama, FAISS, and FastAPI_

---

## Overview

LORP is an early-stage local retrieval-augmented generation (RAG) project. The implemented path uses:

- Ollama for local chat-model inference and embeddings
- Word-based chunking and FAISS CPU indexes for retrieval
- A Python knowledge agent for grounded answers and source citations
- FastAPI endpoints and a small browser UI
- Optional Docker Compose services, including Open WebUI

The project is a prototype, not a production-hardened or multi-agent platform. Framework integrations and features that are not implemented are identified as planned below.

---

## Goals

The current implementation demonstrates:

- Local model calls through Ollama
- Basic text ingestion, fixed-size chunking, embedding, and FAISS indexing
- Retrieval-augmented question answering with source citations
- A small FastAPI API and command-line prompt loop

Multi-agent orchestration, richer document ingestion, evaluation, monitoring, and deployment improvements remain planned work.

## Implemented Architecture

```mermaid
flowchart LR
    A[User question] --> B[API]
    B --> C[RAG agent]
    C --> D[Retrieve context]
    D --> E[Local LLM]
    E --> F[Grounded answer]

    classDef input fill:#14314f,stroke:#60a5fa,stroke-width:2px,color:#e0f2fe;
    classDef process fill:#123a2b,stroke:#34d399,stroke-width:2px,color:#d1fae5;
    classDef retrieval fill:#3a2a17,stroke:#fbbf24,stroke-width:2px,color:#fef3c7;
    classDef output fill:#2d1d45,stroke:#a78bfa,stroke-width:2px,color:#f3e8ff;

    class A,B input;
    class C process;
    class D retrieval;
    class E,F output;
```

For the implemented API, agent, retrieval, model, and CLI paths, see the [detailed runtime view](docs/lorp_runtime_flow.md).

### Ingestion and Retrieval

- The index-building path currently reads `.txt` and `.md` files.
- Text is whitespace-normalized and split into fixed-size word chunks with overlap; chunking is not semantic.
- Embeddings are generated through Ollama using `nomic-embed-text` by default.
- Vectors are normalized and stored in a FAISS `IndexFlatIP` index using the CPU FAISS package.
- Retrieval returns the top matching chunks; reranking and hybrid search are not implemented.

The loader can discover PDF, DOCX, and HTML paths, but the index builder skips those formats. They are not yet supported end to end.

### Agent, API, and CLI

- The implemented `KnowledgeAgent` uses retrieved context to answer questions and includes source citations.
- `src.prompt_flow` provides a command-line question loop.
- FastAPI exposes `/health`, `/ready`, `/query`, and `/source` endpoints, plus a basic browser UI at `/`.
- Query responses can include retrieval/generation timing and token metrics when supplied by Ollama.

### Optional Containers

- Docker Compose defines Ollama, the API, and an Open WebUI container.
- Open WebUI is included as a separate service; a project-specific RAG plugin or configured integration is not implemented.
- GPU acceleration depends on the user's Ollama runtime and hardware; the project does not configure GPU FAISS.

### Planned Integrations

- LangChain orchestration, multi-step workflows, and model routing
- LlamaIndex integration, semantic chunking, and reranking
- SentenceTransformers embeddings
- End-to-end PDF, DOCX, and HTML ingestion
- Functional retrieval, web search, SQL, and filesystem tools
- Research, report, and orchestrator agents
- A custom Open WebUI RAG integration

---

## Project Structure

This interactive tree lists every tracked project file, excluding Git's internal metadata. Entries marked <em>planned</em> are placeholders or stubs, not active implementations.

<div class="project-tree">
<details open>
<summary>📦 <code>local-rag/</code></summary>
<div><code>├── .gitignore</code></div>
<div><code>├── _config.yml</code></div>
<div><code>├── LICENSE</code></div>
<div><code>├── README.md</code></div>
<div><code>├── requirements.txt</code></div>
<details>
<summary><code>├── _layouts/</code></summary>
<div><code>│   └── default.html</code></div>
</details>
<details>
<summary><code>├── ⚙️ config/</code></summary>
<div><code>│   ├── agents.yaml</code></div>
<div><code>│   ├── models.yaml</code></div>
<div><code>│   └── settings.yaml</code></div>
</details>
<details>
<summary><code>├── 💾 data/</code></summary>
<details>
<summary><code>│   ├── indexed/</code></summary>
<div><code>│   │   ├── .gitkeep</code></div>
<div><code>│   │   └── FAISS.txt</code></div>
</details>
<details>
<summary><code>│   ├── indexes/</code> — <em>planned: generated FAISS indexes are created here</em></summary>
<div><code>│   │   └── .gitkeep</code></div>
</details>
<details>
<summary><code>│   ├── processed/</code></summary>
<div><code>│   │   ├── .gitkeep</code></div>
<div><code>│   │   └── test.csv</code></div>
</details>
<details>
<summary><code>│   └── raw/</code></summary>
<div><code>│       ├── .gitkeep</code></div>
<div><code>│       └── test.txt</code></div>
</details>
</details>
<details>
<summary><code>├── 🐳 docker/</code></summary>
<div><code>│   ├── api.Dockerfile</code></div>
<div><code>│   ├── docker-compose.yaml</code></div>
<div><code>│   ├── docker-compose.yml</code></div>
<div><code>│   ├── ollama.Dockerfile</code></div>
<div><code>│   └── webui.Dockerfile</code></div>
</details>
<details>
<summary><code>├── docs/</code></summary>
<div><code>│   └── lorp_runtime_flow.md</code></div>
</details>
<details>
<summary><code>├── src/</code></summary>
<div><code>│   ├── __init__.py</code></div>
<div><code>│   ├── prompt_flow.py</code></div>
<details>
<summary><code>│   ├── 🤖 agents/</code></summary>
<div><code>│   │   ├── __init__.py</code></div>
<div><code>│   │   ├── base_agent.py</code></div>
<div><code>│   │   ├── knowledge_agent.py</code></div>
<div><code>│   │   ├── report_agent.py</code> — <em>planned: structured report agent</em></div>
<div><code>│   │   └── research_agent.py</code> — <em>planned: multi-step research agent</em></div>
</details>
<details>
<summary><code>│   ├── api/</code></summary>
<div><code>│   │   ├── __init__.py</code></div>
<div><code>│   │   └── server.py</code></div>
</details>
<details>
<summary><code>│   ├── eval/</code></summary>
<div><code>│   │   ├── __init__.py</code></div>
<div><code>│   │   └── rag_eval.py</code> — <em>planned: evaluation integration is a placeholder</em></div>
</details>
<details>
<summary><code>│   ├── ingestion/</code></summary>
<div><code>│   │   ├── __init__.py</code></div>
<div><code>│   │   ├── build_index.py</code></div>
<div><code>│   │   ├── loaders.py</code></div>
<div><code>│   │   └── preprocess.py</code></div>
</details>
<details>
<summary><code>│   ├── llm/</code></summary>
<div><code>│   │   ├── __init__.py</code></div>
<div><code>│   │   ├── embeddings.py</code></div>
<div><code>│   │   └── ollama_client.py</code></div>
</details>
<details>
<summary><code>│   ├── retrieval/</code></summary>
<div><code>│   │   ├── __init__.py</code></div>
<div><code>│   │   ├── llamaindex_client.py</code></div>
<div><code>│   │   └── retrievers.py</code></div>
</details>
<details>
<summary><code>│   ├── 🧰 tools/</code> — <em>planned: tool implementations are currently stubs</em></summary>
<div><code>│   │   ├── __init__.py</code></div>
<div><code>│   │   ├── file_tool.py</code></div>
<div><code>│   │   ├── retrieval_tool.py</code></div>
<div><code>│   │   ├── sql_tool.py</code></div>
<div><code>│   │   └── web_search_tool.py</code></div>
</details>
<details>
<summary><code>│   └── 🖥️ ui/</code></summary>
<div><code>│       ├── .gitkeep</code></div>
<div><code>│       └── webui_integration.md</code> — <em>planned: UI integration has notes only</em></div>
</details>
</details>
<details>
<summary><code>└── 🧪 tests/</code></summary>
<div><code>    ├── test_agent.py</code></div>
<div><code>    ├── test_api.py</code></div>
<div><code>    ├── test_ingestion.py</code></div>
<div><code>    ├── test_prompt_flow.py</code></div>
<div><code>    └── test_retrieval.py</code></div>
</details>
</details>
</div>

## Getting Started
### 1. Install Ollama and pull models

Install [Ollama](https://ollama.com/download), then pull a chat model and the default embedding model:

```bash
ollama pull qwen3.5:4b
ollama pull nomic-embed-text
```

The direct Python/API defaults use `qwen3.5:4b`. Docker Compose defaults `CHAT_MODEL` to `qwen2.5:14b`; pull that model instead or set `CHAT_MODEL` to another model available in Ollama.

### 2. Install Python dependencies and build an index

```bash
pip install -r requirements.txt
python src/ingestion/build_index.py
```

The index command reads supported `.txt` and `.md` files from `data/raw` and also indexes the project `README.md`. It writes a FAISS index and metadata JSON under `data/indexes/`.

### 3. Start the API server

```bash
uvicorn src.api.server:app --reload
```

The interactive CLI is also available:

```bash
python -m src.prompt_flow
```

### Optional: run with Docker Compose

From the repository root, start the Ollama, API, and Open WebUI containers:

```bash
docker compose -f docker/docker-compose.yml up --build
```

The Compose Ollama service has its own model volume and does not automatically pull models or build an index. Build the index with the direct Python setup first, then stop the host Ollama service before starting Compose because both use port `11434`. Pull the required models into the Compose Ollama container:

```bash
docker compose -f docker/docker-compose.yml exec ollama ollama pull qwen2.5:14b
docker compose -f docker/docker-compose.yml exec ollama ollama pull nomic-embed-text
```

The API container reads the generated index from the mounted project data directory.

### API endpoints

- `GET /health` — process health
- `GET /ready` — reports whether an index and model clients are configured
- `POST /query` — accepts `{"question": "..."}` and returns an answer, sources, and available metrics
- `GET /source?path=...` — serves a source file only when it belongs to the loaded index

---

## Implemented Features

- Knowledge-agent question answering over retrieved context
- Source and chunk citations in agent answers
- FAISS vector indexing and top-k retrieval
- Ollama chat and embedding clients
- FastAPI API and command-line entry points
- Optional Docker Compose services for Ollama, the API, and Open WebUI

The knowledge agent does not provide a separate document-summarization workflow. Open WebUI is included as a container; a project-specific RAG plugin or configured integration is not implemented.

## Not Yet Implemented

- Semantic chunking, hybrid/BM25 search, and reranking
- PDF, DOCX, and HTML indexing (the index builder currently supports `.txt` and `.md`)
- LangChain and LlamaIndex integrations
- SentenceTransformers embeddings
- Functional research/report/orchestrator agents and implementations of the tool wrappers
- A custom Open WebUI RAG integration
- Automated RAG evaluation

The document loader can discover PDF, DOCX, and HTML files, but the index-building pipeline currently skips those formats.

## Evaluation

`src/eval/rag_eval.py` is a placeholder. RAGAS, LlamaIndex evaluation, DeepEval, and quality metrics such as faithfulness or answer correctness are not currently wired up.

## Deployment

Dockerfiles and a Compose definition are provided for Ollama, the API, and Open WebUI. This is a local-development setup, not a production deployment: authentication, a production CORS policy, and a custom WebUI integration are not configured.

## Monitoring

The API can return retrieval/generation timing and Ollama token metrics with query responses. A Prometheus/Grafana stack, GPU/DCGM monitoring, and persistent metrics collection are not implemented.

## Data and Security

- The repository includes small sample files under `data/raw/`, `data/processed/`, and `data/indexed/`.
- `.gitignore` excludes future local raw/processed data, generated index files under `data/indexes/`, GGUF model files, and `.env` secrets; it does not remove sample files already tracked in Git.
- The API currently allows CORS requests from any origin and has no authentication. Do not expose it to untrusted networks without adding appropriate access controls.

## Roadmap

- Implement research, report, and orchestrator agents
- Implement the planned tools and custom WebUI integration
- Add semantic chunking, additional document formats, hybrid search, and reranking
- Add a RAG evaluation suite and monitoring stack
- Add CI/CD and evaluate production/cloud deployment options

---

## License

GNU General Public License v3.0. See [LICENSE](LICENSE).
