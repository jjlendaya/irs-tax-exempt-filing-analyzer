"""Strategy selector and base class for XML parsers."""

from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal
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

    def _parse_datetime(self, date_str: str | None) -> datetime | None:
        """Parse date string in various formats to datetime object."""
        if not date_str:
            return None

        date_str = date_str.strip()

        # Try common date formats
        date_formats = [
            "%Y-%m-%d",
            "%m/%d/%Y",
            "%d/%m/%Y",
            "%Y%m%d",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S%z",
        ]

        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue

        return None

    def _parse_decimal(self, value: str | None) -> Decimal | None:
        """Parse decimal string to Decimal object."""
        if not value:
            return None

        try:
            # Remove commas and whitespace
            cleaned = value.replace(",", "").strip()
            return Decimal(cleaned)
        except (ValueError, TypeError):
            return None
