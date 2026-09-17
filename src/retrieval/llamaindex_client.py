class LlamaIndexClient:
    """Adapter boundary for the LlamaIndex query engine."""

    def query(self, question: str) -> str:
        raise NotImplementedError("Configure the LlamaIndex query engine first")
