from .base_agent import BaseAgent


class KnowledgeAgent(BaseAgent):
    """RAG-powered question-answering agent."""

    def __init__(self, retriever=None, llm=None, top_k: int = 5):
        self.retriever = retriever
        self.llm = llm
        self.top_k = top_k

    def run(self, prompt: str) -> str:
        if self.retriever is None or self.llm is None:
            raise RuntimeError("Knowledge agent dependencies are not configured")

        results = self.retriever.retrieve(prompt, self.top_k)
        if not results:
            return "I could not find relevant information in the indexed documents."

        context = "\n\n".join(
            f"[{result.chunk_id}] {result.text}" for result in results
        )
        prompt_text = (
            "Answer the question using only the context below. "
            "If the context is insufficient, say so. Cite supporting chunk IDs.\n\n"
            f"Context:\n{context}\n\nQuestion: {prompt}"
        )
        return self.llm.generate(prompt_text)
