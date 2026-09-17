import httpx


class EmbeddingProvider:
    """Embedding provider interface for local models."""

    def embed(self, text: str) -> list[float]:
        raise NotImplementedError


class OllamaEmbeddingProvider(EmbeddingProvider):
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "nomic-embed-text"):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def embed(self, text: str) -> list[float]:
        response = httpx.post(
            f"{self.base_url}/api/embed",
            json={"model": self.model, "input": text},
            timeout=60.0,
        )
        response.raise_for_status()
        embeddings = response.json().get("embeddings", [])
        if not embeddings:
            raise RuntimeError("Ollama returned no embedding")
        return embeddings[0]
