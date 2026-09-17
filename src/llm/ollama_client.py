class OllamaClient:
    """Small integration boundary for a local Ollama server."""

    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
