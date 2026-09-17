def preprocess_text(text: str) -> str:
    """Normalize whitespace before indexing."""
    return " ".join(text.split())
