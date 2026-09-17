class SQLTool:
    """Optional read-only SQL tool boundary."""

    def run(self, query: str) -> list:
        raise NotImplementedError
