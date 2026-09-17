import json
from dataclasses import dataclass
from pathlib import Path

import faiss
import numpy as np


@dataclass(frozen=True)
class RetrievalResult:
    text: str
    source: str
    score: float
    chunk_id: str


class Retriever:
    """FAISS retriever with a companion metadata document store."""

    def __init__(self, index_path: str, metadata_path: str, embedder):
        self.index = faiss.read_index(index_path)
        self.metadata = json.loads(Path(metadata_path).read_text(encoding="utf-8"))
        if self.index.ntotal != len(self.metadata):
            raise ValueError("FAISS index and metadata have different sizes")
        self.embedder = embedder

    def retrieve(self, query: str, top_k: int = 5) -> list[RetrievalResult]:
        if not query.strip():
            return []
        vector = np.asarray([self.embedder.embed(query)], dtype="float32")
        faiss.normalize_L2(vector)
        scores, positions = self.index.search(vector, min(top_k, self.index.ntotal))
        return [
            RetrievalResult(
                text=self.metadata[position]["text"],
                source=self.metadata[position]["source"],
                score=float(score),
                chunk_id=self.metadata[position]["chunk_id"],
            )
            for score, position in zip(scores[0], positions[0])
            if position >= 0
        ]
