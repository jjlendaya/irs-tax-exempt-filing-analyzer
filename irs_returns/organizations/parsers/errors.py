class NoStrategyFoundError(Exception):
    """Exception raised when no handler is found for the given XML content."""

    def __init__(self, xml_content: bytes, available_strategies: list[str]):
        xml_content_str = (
            xml_content.decode("utf-8")[:50] + "..." if len(xml_content) > 50 else xml_content.decode("utf-8")
        )
        super().__init__(
            f"No handler found for the given XML content: {xml_content_str}.\nAvailable handlers: {', '.join(available_strategies)}"
        )
