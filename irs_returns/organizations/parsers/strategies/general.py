"""Strategy selector and base class for XML parsers."""

from abc import ABC, abstractmethod
from typing import Any

from .errors import StrategyCannotHandleXMLContentError


class XMLParserStrategy(ABC):
    """Abstract base class for XML parsing strategies."""

    def __init__(self, xml_content: bytes):
        self.xml_content = xml_content

    @abstractmethod
    def can_handle(self) -> bool:
        """
        Check if this strategy can handle the given XML.

        Args:
            None

        Returns:
            True if this strategy can handle the XML content, False otherwise
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def parse(self) -> dict[str, Any]:
        """
        Parse the XML content.

        Args:
            None

        Returns:
            Dictionary with data parsed from the XML content
        """
        raise NotImplementedError("Subclasses must implement this method")

    def _raise_cannot_handle_error(self) -> None:
        """Raise a cannot handle error."""
        raise StrategyCannotHandleXMLContentError(strategy_name=self.__class__.__name__)
