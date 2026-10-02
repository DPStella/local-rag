# Local Open RAG Platform (LORP)
_Local‑first multi‑agent RAG platform built with Ollama, LangChain, LlamaIndex, and FAISS_

---

## Overview

Local Open RAG Platform (LORP) is a fully local, open‑source AI system designed to demonstrate modern enterprise AI platform engineering practices. It combines:

- Ollama for local LLM serving
- LlamaIndex for ingestion, chunking, embeddings, and retrieval
- FAISS for high‑performance vector search
- LangChain for agent orchestration and tool execution
- FastAPI for serving a clean API layer
- Open WebUI for a ChatGPT‑style interface

LORP is built as a realistic, production‑aligned starter project for hands‑on work with RAG, agents, and AI platform engineering.

---

## Goals

LORP helps you learn and demonstrate:

- Local LLM serving and model abstraction
- Document ingestion and semantic chunking
- Embedding generation and vector indexing
- Retrieval‑augmented generation (RAG)
- Agent orchestration and tool use
- API design for AI systems
- Containerization and deployment patterns
- Monitoring and evaluation foundations
- Multi‑agent architecture design

---

## Architecture

### Runtime Flow

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

For the complete API, agent, retrieval, model, and CLI flow, see the [detailed runtime view](docs/lorp_runtime_flow.md).

### LlamaIndex – Retrieval Layer

- Document loaders (PDF, DOCX, HTML, Markdown)
- Preprocessing and semantic chunking
- Embeddings (Ollama or SentenceTransformers)
- FAISS vector store
- Query engine with reranking
- RAG evaluation (RAGAS / LlamaIndex eval suite)

### LangChain – Orchestration Layer

- Agents
- Tools (retrieval, web search, SQL, filesystem)
- Multi‑step workflows
- Routing between models
- FastAPI service layer

### Ollama – Local LLM Server

- Model inference
- Embeddings
- OpenAI‑compatible API
- GPU acceleration

### Open WebUI – User Interface

- Chat interface
- File upload
- Model switching
- Custom RAG plugin

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
### 1. Install Ollama
Download from:
https://ollama.com/download

Pull recommended models:

```bash
ollama pull qwen2.5:14b
ollama pull llama3.1:8b
ollama pull gemma2:9b
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Build your FAISS index
```bash
python src/ingestion/build_index.py
```
The standard build indexes documents from `data/raw` and the project `README.md`.

### 4. Start the API server
```bash
uvicorn src.api.server:app --reload
```

### 5. (Optional) Start Open WebUI
Point Open WebUI to the API endpoint you just started.

---

## Agents
### Knowledge Agent (current)
- RAG‑powered question answering
- Source citation
- Document summarization
- Context‑aware responses

### Future Agents
- Research Agent – multi‑step research workflows
- Report Agent – structured report generation
- Orchestrator Agent – routes tasks between agents


## Retrieval
- LORP uses LlamaIndex + FAISS for retrieval:
- Semantic chunking
- Metadata‑rich document nodes
- GPU‑accelerated vector search
- Optional hybrid search and reranking


## Evaluation
- RAG quality can be measured using:
- RAGAS
- LlamaIndex eval suite
- DeepEval

Metrics include:
- Faithfulness
- Context relevance
- Answer correctness
- Citation accuracy


## Deployment
LORP includes Dockerfiles for:
- Ollama
- API server
- Open WebUI
And a `docker-compose.yml` for local orchestration.


## Monitoring (Optional)
You can integrate:
- Prometheus
- Grafana
- NVIDIA DCGM exporter

To track:
- GPU utilization
- Token/sec
- Latency
- Memory usage
- Vector DB performance


## Data & Security
This repo intentionally excludes:

- Raw documents
- FAISS indexes
- Models
- Secrets

See .gitignore for details.


## Roadmap
- Add Research Agent
- Add Report Agent
- Add Orchestrator Agent
- Add hybrid search (BM25 + FAISS)
- Add RAG evaluation suite
- Add monitoring stack
- Add CI/CD (GitHub Actions)
- Add cloud deployment option (Kubernetes)

---

License
GNU V3 License
