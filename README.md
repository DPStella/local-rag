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

This diagram lists every tracked project file, excluding Git's internal metadata. Entries marked `planned` are placeholders or stubs, not active implementations.

```mermaid
---
config:
  treeView:
    rowIndent: 24
    paddingX: 8
    paddingY: 6
    lineThickness: 1.5
    showIcons: false
  themeVariables:
    treeView:
      labelFontSize: '16px'
      labelColor: '#1f2937'
      lineColor: '#64748b'
      descriptionColor: '#475569'
---
treeView-beta
└── 📦 local-rag/
    ├── .gitignore
    ├── _config.yml
    ├── LICENSE
    ├── 📝 README.md
    ├── requirements.txt
    ├── _layouts/
    │   └── default.html
    ├── ⚙️ config/
    │   ├── agents.yaml
    │   ├── models.yaml
    │   └── settings.yaml
    ├── 💾 data/
    │   ├── indexed/
    │   │   ├── .gitkeep
    │   │   └── FAISS.txt
    │   ├── indexes/ ## planned: generated FAISS indexes are created here
    │   │   └── .gitkeep
    │   ├── processed/
    │   │   ├── .gitkeep
    │   │   └── test.csv
    │   └── raw/
    │       ├── .gitkeep
    │       └── test.txt
    ├── 🐳 docker/
    │   ├── api.Dockerfile
    │   ├── docker-compose.yaml
    │   ├── docker-compose.yml
    │   ├── ollama.Dockerfile
    │   └── webui.Dockerfile
    ├── docs/
    │   └── lorp_runtime_flow.md
    ├── src/
    │   ├── __init__.py
    │   ├── prompt_flow.py
    │   ├── 🤖 agents/
    │   │   ├── __init__.py
    │   │   ├── base_agent.py
    │   │   ├── knowledge_agent.py
    │   │   ├── report_agent.py ## planned: structured report agent
    │   │   └── research_agent.py ## planned: multi-step research agent
    │   ├── api/
    │   │   ├── __init__.py
    │   │   └── server.py
    │   ├── eval/
    │   │   ├── __init__.py
    │   │   └── rag_eval.py ## planned: evaluation integration is a placeholder
    │   ├── ingestion/
    │   │   ├── __init__.py
    │   │   ├── build_index.py
    │   │   ├── loaders.py
    │   │   └── preprocess.py
    │   ├── llm/
    │   │   ├── __init__.py
    │   │   ├── embeddings.py
    │   │   └── ollama_client.py
    │   ├── retrieval/
    │   │   ├── __init__.py
    │   │   ├── llamaindex_client.py
    │   │   └── retrievers.py
    │   ├── 🧰 tools/ ## planned: tool implementations are currently stubs
    │   │   ├── __init__.py
    │   │   ├── file_tool.py
    │   │   ├── retrieval_tool.py
    │   │   ├── sql_tool.py
    │   │   └── web_search_tool.py
    │   └── 🖥️ ui/
    │       ├── .gitkeep
    │       └── webui_integration.md ## planned: UI integration has notes only
    └── 🧪 tests/
        ├── test_agent.py
        ├── test_api.py
        ├── test_ingestion.py
        ├── test_prompt_flow.py
        └── test_retrieval.py
```

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
