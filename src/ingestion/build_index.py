from pathlib import Path

from src.ingestion.loaders import load_documents


def build_index(input_dir: str = "data/raw", output_dir: str = "data/indexes") -> None:
    """Scaffold entry point for building the vector index."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    documents = load_documents(input_dir)
    print(f"Found {len(documents)} documents; connect LlamaIndex and FAISS here.")


if __name__ == "__main__":
    build_index()
