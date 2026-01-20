"""XML Parser Handler using Strategy pattern."""

import logging
from typing import Any

from lxml import etree

from organizations.parsers.errors import NoStrategyFoundError
from organizations.parsers.strategies.general import XMLParserStrategy
from organizations.parsers.strategies.irs_990 import IRS990Strategy
from organizations.parsers.strategies.irs_990_ez import IRS990EZStrategy
from organizations.parsers.strategies.irs_990_pf import IRS990PFStrategy

logger = logging.getLogger(__name__)


class XMLParser:
    """Main handler for XML parsing using strategy pattern."""

    STRATEGY_CLASSES = {
        "IRS Form 990": IRS990Strategy,
        "IRS Form 990PF": IRS990PFStrategy,
        "IRS Form 990EZ": IRS990EZStrategy,
    }

    def __init__(self, xml_content: bytes):
        self.xml_content = xml_content
        self.strategy_instances = {
            strategy_name: strategy_class(self.xml_content)
            for strategy_name, strategy_class in self.STRATEGY_CLASSES.items()
        }

    def _select_strategy(self) -> tuple[str, XMLParserStrategy]:
        xml_content_str = (
            self.xml_content.decode("utf-8")[:50] + "..."
            if len(self.xml_content) > 50
            else self.xml_content.decode("utf-8")
        )
        logger.debug(f"Selecting strategy for XML content: {xml_content_str}...")
        for strategy_name, strategy in self.strategy_instances.items():
            logger.debug(f"Checking if {strategy_name} can handle XML content...")
            if strategy.can_handle():
                logger.debug(f"Selected {strategy_name} strategy.")
                return strategy_name, strategy
        raise NoStrategyFoundError(self.xml_content, available_strategies=list(self.strategy_instances.keys()))

    def _validate_xml(self) -> None:
        """
        Check if the XML content is valid and well-formed.

        Args:
            xml_content: Raw XML bytes

        Raises:
            etree.XMLSyntaxError: If the XML content is not valid XML or not well-formed.
        """
        etree.fromstring(self.xml_content)

    def parse(self) -> dict[str, Any]:
        """
        Parse XML content using appropriate handler.

        Args:
            None

        Returns:
            Dictionary with strategy_name used and data parsed from the XML content.

        Raises:
            NoStrategyFoundError: If no suitable handler is found for the given XML content.
            etree.XMLSyntaxError: If the XML content is not valid XML or not well-formed.
        """
        self._validate_xml()
        strategy_name, strategy = self._select_strategy()
        logger.debug(f"Using {strategy_name} handler to parse XML content.")
        return {
            "strategy_name": strategy_name,
            "data": strategy.parse(),
        }
