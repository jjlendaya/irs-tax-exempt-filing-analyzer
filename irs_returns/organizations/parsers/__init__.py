"""XML Parser package using Strategy pattern."""

from organizations.parsers.handler import XMLParserHandler

__all__ = ["XMLParserHandler", "parse_irs_990_xml"]


def parse_irs_990_xml(xml_content: bytes) -> dict:
    """
    Legacy interface for parsing XML.
    
    Maintained for backward compatibility with existing code.
    
    Args:
        xml_content: Raw XML bytes
        
    Returns:
        Dictionary with organization and return_info keys
    """
    handler = XMLParserHandler()
    return handler.parse(xml_content)
