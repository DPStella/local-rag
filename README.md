# Enterprise RAG Agent Platform (ERAP)
_Local‑first multi‑agent RAG platform built with Ollama, LangChain, LlamaIndex, and FAISS_

---

## Overview

Enterprise RAG Agent Platform (ERAP) is a fully local, open‑source AI system designed to demonstrate modern enterprise AI platform engineering practices. It combines:

- Ollama for local LLM serving
- LlamaIndex for ingestion, chunking, embeddings, and retrieval
- FAISS for high‑performance vector search
- LangChain for agent orchestration and tool execution
- FastAPI for serving a clean API layer
- Open WebUI for a ChatGPT‑style interface

ERAP is built as a realistic, production‑aligned starter project for hands‑on work with RAG, agents, and AI platform engineering.

---

## Goals

ERAP helps you learn and demonstrate:

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

```text
local-enterprise-rag-agent/
├─ docker/
│  ├─ docker-compose.yml
│  ├─ ollama.Dockerfile
│  ├─ api.Dockerfile
│  ├─ webui.Dockerfile
├─ config/
│  ├─ settings.yaml
│  ├─ models.yaml
│  ├─ agents.yaml
├─ data/
│  ├─ raw/          # raw documents (excluded from Git)
│  ├─ processed/    # cleaned text (excluded from Git)
│  ├─ indexes/      # FAISS indexes (excluded from Git)
├─ src/
│  ├─ ingestion/
│  │  ├─ loaders.py
│  │  ├─ preprocess.py
│  │  ├─ build_index.py
│  ├─ retrieval/
│  │  ├─ llamaindex_client.py
│  │  ├─ retrievers.py
│  ├─ llm/
│  │  ├─ ollama_client.py
│  │  ├─ embeddings.py
│  ├─ agents/
│  │  ├─ base_agent.py
│  │  ├─ knowledge_agent.py   # first agent
│  │  ├─ research_agent.py    # future
│  │  ├─ report_agent.py      # future
│  ├─ tools/
│  │  ├─ retrieval_tool.py
│  │  ├─ web_search_tool.py
│  │  ├─ sql_tool.py
│  │  ├─ file_tool.py
│  ├─ api/
│  │  ├─ server.py
│  ├─ ui/
│  │  ├─ webui_integration.md
│  ├─ eval/
│  │  ├─ rag_eval.py
├─ tests/
│  ├─ test_ingestion.py
│  ├─ test_retrieval.py
│  ├─ test_agent.py
├─ .gitignore
├─ README.md
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
- ERAP uses LlamaIndex + FAISS for retrieval:
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
