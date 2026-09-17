from dataclasses import dataclass

import httpx


@dataclass(frozen=True)
class GenerationResult:
    content: str
    prompt_tokens: int
    completion_tokens: int
    total_duration_ms: float
    generation_duration_ms: float
    tokens_per_second: float


class OllamaClient:
    """Small integration boundary for a local Ollama server."""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "qwen3.5:4b"):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def generate(self, prompt: str) -> str:
        return self.generate_with_metrics(prompt).content

    def generate_with_metrics(self, prompt: str) -> GenerationResult:
        response = httpx.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "think": False,
            },
            timeout=120.0,
        )
        response.raise_for_status()
        payload = response.json()
        content = payload.get("message", {}).get("content", "").strip()
        if not content:
            raise RuntimeError("Ollama returned an empty response")

        completion_tokens = int(payload.get("eval_count", 0))
        generation_duration_ns = int(payload.get("eval_duration", 0))
        generation_duration_seconds = generation_duration_ns / 1_000_000_000
        tokens_per_second = (
            completion_tokens / generation_duration_seconds
            if generation_duration_seconds > 0
            else 0.0
        )
        return GenerationResult(
            content=content,
            prompt_tokens=int(payload.get("prompt_eval_count", 0)),
            completion_tokens=completion_tokens,
            total_duration_ms=int(payload.get("total_duration", 0)) / 1_000_000,
            generation_duration_ms=generation_duration_ns / 1_000_000,
            tokens_per_second=tokens_per_second,
        )
