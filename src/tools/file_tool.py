class FileTool:
    """Safe filesystem tool boundary."""

    def read(self, path: str) -> str:
        raise NotImplementedError
