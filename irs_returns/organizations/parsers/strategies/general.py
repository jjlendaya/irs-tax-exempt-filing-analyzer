"""Strategy selector and base class for XML parsers."""

from abc import ABC, abstractmethod
from typing import Any


class XMLParserStrategy(ABC):
    """Abstract base class for XML parsing strategies."""

    @abstractmethod
    def can_handle(self, xml_content: bytes) -> bool:
        """
        Check if this strategy can handle the given XML.

        Args:
            xml_content: Raw XML bytes

        Returns:
            True if this strategy can parse the XML, False otherwise
        """
        pass

    @abstractmethod
    def parse(self, xml_content: bytes) -> dict[str, Any]:
        """
        Parse the XML content.

        Args:
            xml_content: Raw XML bytes

        Returns:
            Dictionary with organization and return_info keys
        """
        pass


def select_strategy(xml_content: bytes) -> XMLParserStrategy:
    """
    Select appropriate parsing strategy based on XML content.

    Args:
        xml_content: Raw XML bytes

    Returns:
        Strategy instance that can handle the XML

    Raises:
        ValueError: If no strategy can handle the XML
    """
    # Import here to avoid circular imports
    from organizations.parsers.strategies.irs_990 import IRS990Strategy

    # Registry of available strategies
    strategies = [
        IRS990Strategy(),
    ]

    for strategy in strategies:
        if strategy.can_handle(xml_content):
            return strategy

    raise ValueError("No suitable parsing strategy found for the given XML")
