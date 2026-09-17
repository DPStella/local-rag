class EmbeddingProvider:
    """Embedding provider interface for Ollama or SentenceTransformers."""

    def embed(self, text: str) -> list[float]:
        raise NotImplementedError
