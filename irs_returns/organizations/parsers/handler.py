"""XML Parser Handler using Strategy pattern."""

import logging
from typing import Any

from organizations.parsers.errors import NoStrategyFoundError
from organizations.parsers.strategies.general import XMLParserStrategy
from organizations.parsers.strategies.irs_990 import IRS990Strategy

logger = logging.getLogger(__name__)


class XMLParser:
    """Main handler for XML parsing using strategy pattern."""

    STRATEGY_CLASSES = {
        "IRS Form 990": IRS990Strategy,
        # TODO: Implement other strategies here
        # "IRS990PF": IRS990PFStrategy,
        # "IRS990EZ": IRS990EZStrategy,
    }

    def __init__(self):
        self.strategy_instances = {
            strategy_name: strategy_class() for strategy_name, strategy_class in self.STRATEGY_CLASSES.items()
        }

    def _select_strategy(self, xml_content: bytes) -> tuple[str, XMLParserStrategy]:
        xml_content_str = (
            xml_content.decode("utf-8")[:50] + "..." if len(xml_content) > 50 else xml_content.decode("utf-8")
        )
        logger.debug(f"Selecting strategy for XML content: {xml_content_str}...")
        for strategy_name, strategy in self.strategy_instances.items():
            logger.debug(f"Checking if {strategy_name} can handle XML content...")
            if strategy.can_handle(xml_content):
                logger.debug(f"Selected {strategy_name} strategy.")
                return strategy_name, strategy
        logger.error(f"No strategy found for XML content: {xml_content_str}")
        raise NoStrategyFoundError(xml_content, available_strategies=list(self.strategy_instances.keys()))

    def parse(self, xml_content: bytes) -> dict[str, Any]:
        """
        Parse XML content using appropriate handler.

        Args:
            xml_content: Raw XML bytes

        Returns:
            Dictionary with strategy_name used and data parsed from the XML content.

        Raises:
            NoStrategyFoundError: If no suitable handler is found for the given XML content.
        """
        strategy_name, strategy = self._select_strategy(xml_content)
        logger.info(f"Using {strategy_name} handler to parse XML content.")
        return {
            "strategy_name": strategy_name,
            "data": strategy.parse(xml_content),
        }
