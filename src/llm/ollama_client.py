import httpx


class OllamaClient:
    """Small integration boundary for a local Ollama server."""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "qwen2.5:14b"):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def generate(self, prompt: str) -> str:
        response = httpx.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
            },
            timeout=120.0,
        )
        response.raise_for_status()
        content = response.json().get("message", {}).get("content", "").strip()
        if not content:
            raise RuntimeError("Ollama returned an empty response")
        return content
