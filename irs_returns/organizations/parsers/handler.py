"""XML Parser Handler using Strategy pattern."""

from typing import Any

from organizations.parsers.strategies.general import select_strategy


class XMLParserHandler:
    """Main handler for XML parsing using strategy pattern."""

    def parse(self, xml_content: bytes) -> dict[str, Any]:
        """
        Parse XML content using appropriate strategy.

        Args:
            xml_content: Raw XML bytes

        Returns:
            Dictionary with organization and return_info keys

        Raises:
            ValueError: If no suitable strategy found for XML
        """
        strategy = select_strategy(xml_content)
        return strategy.parse(xml_content)
