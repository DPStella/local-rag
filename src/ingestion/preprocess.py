from dataclasses import dataclass


@dataclass(frozen=True)
class TextChunk:
    """A stable unit of text and the metadata needed for citations."""

    chunk_id: str
    text: str
    source: str
    chunk_index: int


def preprocess_text(text: str) -> str:
    """Normalize whitespace before indexing."""
    return " ".join(text.split())


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 120) -> list[str]:
    """Split normalized text into deterministic word-based chunks."""
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("chunk_size must be positive and overlap must be smaller")

    words = preprocess_text(text).split()
    chunks: list[str] = []
    step = chunk_size - overlap
    for start in range(0, len(words), step):
        chunk = " ".join(words[start : start + chunk_size])
        if chunk:
            chunks.append(chunk)
        if start + chunk_size >= len(words):
            break
    return chunks
