from time import perf_counter
from .base_agent import BaseAgent
from pathlib import Path


class KnowledgeAgent(BaseAgent):
    """RAG-powered question-answering agent."""

    def __init__(self, retriever=None, llm=None, top_k: int = 5):
        self.retriever = retriever
        self.llm = llm
        self.top_k = top_k

    def run_with_metrics(self, prompt: str) -> tuple[str, list, dict[str, float | int]]:
        if self.retriever is None or self.llm is None:
            raise RuntimeError("Knowledge agent dependencies are not configured")

        workflow_started = perf_counter()
        retrieval_started = perf_counter()
        results = self.retriever.retrieve(prompt, self.top_k)
        retrieval_ms = (perf_counter() - retrieval_started) * 1000
        if not results:
            return (
                "I could not find relevant information in the indexed documents.",
                [],
                {
                    "retrieval_ms": retrieval_ms,
                    "generation_ms": 0.0,
                    "workflow_ms": (perf_counter() - workflow_started) * 1000,
                },
            )

        source_numbers: dict[str, int] = {}
        for result in results:
            source = str(getattr(result, "source", result.chunk_id))
            source_numbers.setdefault(source, len(source_numbers) + 1)

        context = "\n\n".join(
            f"[Source {source_numbers[str(getattr(result, 'source', result.chunk_id))]}] {result.text}"
            for result in results
        )
        prompt_text = (
            "Answer the question using only the context below. "
            "If the context is insufficient, say so. Put each factual statement or "
            "paragraph in its own block, separated by a blank line, and end it with one or more citation markers "
            "such as [1] or [1, 2]. Use only the source numbers provided in context. "
            "Do not place citations in the middle of a sentence.\n\n"
            f"Context:\n{context}\n\nQuestion: {prompt}"
        )
        generation_started = perf_counter()
        if hasattr(self.llm, "generate_with_metrics"):
            generation = self.llm.generate_with_metrics(prompt_text)
            answer = generation.content
            metrics: dict[str, float | int] = {
                "prompt_tokens": generation.prompt_tokens,
                "completion_tokens": generation.completion_tokens,
                "total_tokens": generation.prompt_tokens + generation.completion_tokens,
                "generation_ms": generation.generation_duration_ms,
                "tokens_per_second": generation.tokens_per_second,
            }
        else:
            answer = self.llm.generate(prompt_text)
            metrics = {"generation_ms": (perf_counter() - generation_started) * 1000}
        metrics["retrieval_ms"] = retrieval_ms
        metrics["workflow_ms"] = (perf_counter() - workflow_started) * 1000
        return answer, results, metrics

    def run_with_sources(self, prompt: str) -> tuple[str, list]:
        answer, results, _ = self.run_with_metrics(prompt)
        return answer, results

    def run(self, prompt: str) -> str:
        answer, results = self.run_with_sources(prompt)
        if not results:
            return answer

        sources: list[str] = []
        source_numbers: dict[str, int] = {}
        for result in results:
            source = str(getattr(result, "source", result.chunk_id))
            source_numbers.setdefault(source, len(source_numbers) + 1)
            if source_numbers[source] != len(sources) + 1:
                continue
            display_name = Path(source).name
            link = Path(source).as_posix()
            sources.append(
                f"[{source_numbers[source]}]: [{display_name}]({link}) (chunk {result.chunk_id})"
            )

        return f"{answer.rstrip()}\n\nSources:\n" + "\n".join(sources)
