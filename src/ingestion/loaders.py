from pathlib import Path


def load_documents(directory: str = "data/raw") -> list[Path]:
    """Return supported documents found below *directory*."""
    root = Path(directory)
    extensions = {".pdf", ".docx", ".html", ".htm", ".md", ".txt"}
    return [path for path in root.rglob("*") if path.is_file() and path.suffix.lower() in extensions]
