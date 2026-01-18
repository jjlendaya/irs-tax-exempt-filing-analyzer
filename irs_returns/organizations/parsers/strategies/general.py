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
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def parse(self, xml_content: bytes) -> dict[str, Any]:
        """
        Parse the XML content.

        Args:
            xml_content: Raw XML bytes

        Returns:
            Dictionary with organization and return_info keys
        """
        raise NotImplementedError("Subclasses must implement this method")
