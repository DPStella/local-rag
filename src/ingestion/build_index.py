import json
from pathlib import Path
from typing import Iterable, Protocol

import faiss
import numpy as np

from src.ingestion.loaders import load_documents
from src.ingestion.preprocess import TextChunk, chunk_text


class Embedder(Protocol):
    def embed(self, text: str) -> list[float]: ...


def read_document(path: Path) -> str:
    """Read the initial supported text formats using UTF-8."""
    if path.suffix.lower() not in {".txt", ".md"}:
        raise ValueError(f"Unsupported format for the first pipeline: {path.suffix}")
    return path.read_text(encoding="utf-8")


def build_chunks(
    input_dir: str,
    chunk_size: int,
    overlap: int,
    source_files: Iterable[str | Path] | None = None,
) -> list[TextChunk]:
    chunks: list[TextChunk] = []
    paths = load_documents(input_dir)
    if source_files:
        paths.extend(Path(source) for source in source_files)

    seen_paths: set[Path] = set()
    for path in paths:
        resolved_path = path.resolve()
        if resolved_path in seen_paths:
            continue
        seen_paths.add(resolved_path)
        if path.suffix.lower() not in {".txt", ".md"}:
            continue
        for index, text in enumerate(chunk_text(read_document(path), chunk_size, overlap)):
            chunks.append(TextChunk(f"{path}:{index}", text, str(path), index))
    return chunks


def build_index(
    input_dir: str = "data/raw",
    output_dir: str = "data/indexes",
    embedder: Embedder | None = None,
    chunk_size: int = 800,
    overlap: int = 120,
    source_files: Iterable[str | Path] | None = None,
) -> Path:
    """Build a FAISS index and companion metadata file."""
    if embedder is None:
        from src.llm.embeddings import OllamaEmbeddingProvider

        embedder = OllamaEmbeddingProvider()

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    chunks = build_chunks(input_dir, chunk_size, overlap, source_files)
    if not chunks:
        raise ValueError(f"No supported text documents found in {input_dir}")

    vectors = np.asarray([embedder.embed(chunk.text) for chunk in chunks], dtype="float32")
    faiss.normalize_L2(vectors)
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)

    index_path = Path(output_dir) / "documents.faiss"
    metadata_path = Path(output_dir) / "documents.json"
    faiss.write_index(index, str(index_path))
    metadata_path.write_text(
        json.dumps([chunk.__dict__ for chunk in chunks], indent=2), encoding="utf-8"
    )
    return index_path


if __name__ == "__main__":
    build_index(source_files=("README.md",))
