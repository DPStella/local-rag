from pathlib import Path

from src.ingestion.build_index import build_index
from src.retrieval.retrievers import Retriever


class FakeEmbedder:
    def embed(self, text: str) -> list[float]:
        return [float(len(text)), float(text.count("alpha")), 1.0]


def test_retriever_returns_source_metadata(tmp_path: Path):
    raw = tmp_path / "raw"
    output = tmp_path / "indexes"
    raw.mkdir()
    (raw / "notes.txt").write_text("alpha beta gamma", encoding="utf-8")
    build_index(str(raw), str(output), FakeEmbedder(), chunk_size=10, overlap=2)

    results = Retriever(
        str(output / "documents.faiss"),
        str(output / "documents.json"),
        FakeEmbedder(),
    ).retrieve("alpha")

    assert len(results) == 1
    assert results[0].source.endswith("notes.txt")
    assert "alpha" in results[0].text
