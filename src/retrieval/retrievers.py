class Retriever:
    """Retrieval interface used by agents and API handlers."""

    def retrieve(self, query: str, top_k: int = 5) -> list:
        raise NotImplementedError
