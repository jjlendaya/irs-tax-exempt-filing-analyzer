class StrategyCannotHandleXMLContentError(Exception):
    """Exception raised when a strategy cannot handle the given XML content."""

    def __init__(self, strategy_name: str):
        super().__init__(f"Strategy {strategy_name} cannot handle the given XML content.")
