from pathlib import Path

from src.ingestion.build_index import build_index
from src.ingestion.preprocess import chunk_text


class FakeEmbedder:
    def embed(self, text: str) -> list[float]:
        return [float(len(text)), float(text.count("alpha")), 1.0]


def test_chunk_text_is_deterministic():
    assert chunk_text("one two three four", chunk_size=2, overlap=1) == [
        "one two",
        "two three",
        "three four",
    ]


def test_build_index_writes_faiss_and_metadata(tmp_path: Path):
    raw = tmp_path / "raw"
    output = tmp_path / "indexes"
    raw.mkdir()
    (raw / "notes.txt").write_text("alpha beta gamma", encoding="utf-8")

    index_path = build_index(str(raw), str(output), FakeEmbedder(), chunk_size=10, overlap=2)

    assert index_path.exists()
    assert (output / "documents.json").exists()
