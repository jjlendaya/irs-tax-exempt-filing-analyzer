"""IRS Form 990 XML parsing strategy."""

import logging
from typing import Any

from lxml import etree

from organizations.parsers.strategies.general import XMLParserStrategy

from .errors import StrategyCannotHandleXMLContentError

logger = logging.getLogger(__name__)


class IRS990PFStrategy(XMLParserStrategy):
    """Strategy for parsing IRS Form 990PF XML files."""

    IRS_NAMESPACE = "http://www.irs.gov/efile"

    def can_handle(self) -> bool:
        """Check if this is an IRS Form 990PF XML file."""
        try:
            root = etree.fromstring(self.xml_content)
            self._validate_has_irs_namespace(root)
            self._validate_has_irs_990_pf_root_elements(root)
            self._validate_has_correct_return_type(root)
            return True
        except StrategyCannotHandleXMLContentError:
            return False

    def _validate_has_irs_namespace(self, root: etree.Element) -> None:
        """Check if the XML content has the IRS namespace."""
        if root.nsmap:
            namespaces = root.nsmap.values()
            if any(self.IRS_NAMESPACE in ns for ns in namespaces):
                return
        self._raise_cannot_handle_error()

    def _validate_has_irs_990_pf_root_elements(self, root: etree.Element) -> None:
        """Check if the XML content has the IRS 990PF root elements."""
        root_tag = root.tag.lower()
        if "return" in root_tag or "irs990pf" in root_tag:
            return
        self._raise_cannot_handle_error()

    def _validate_has_correct_return_type(self, root: etree.Element) -> None:
        """Check if the XML content has the correct return type."""
        return_type = root.find(".//irs:ReturnHeader/irs:ReturnTypeCd", namespaces={"irs": self.IRS_NAMESPACE})
        if return_type is None or return_type.text.lower() != "990pf":
            self._raise_cannot_handle_error()

    def parse(self) -> dict[str, Any]:
        """
        Parse an IRS Form 990PF XML file and extract organization and return information.

        Args:
            xml_content: The XML file content as bytes

        Returns:
            Dictionary with keys:
            - organization: dict with name, website_url, mission_description
            - return_info: dict with filed_on, tax_period_start_date, tax_period_end_date,
              employee_count, total_revenue, total_expenses, total_assets
        """
        # Parse XML with namespace support
        root = etree.fromstring(self.xml_content)

        # IRS Form 990PF XML typically uses this namespace
        ns = {"irs": self.IRS_NAMESPACE}

        # Try to find namespace from root element if present
        if root.nsmap:
            # Use the default namespace or first namespace found
            default_ns = root.nsmap.get(None) or list(root.nsmap.values())[0]
            ns = {"irs": default_ns}

        # Extract organization information
        organization_data = self._extract_organization_data(root, ns)

        # Extract return information
        return_data = self._extract_return_data(root, ns)

        return {
            "organization": organization_data,
            "return_info": return_data,
        }

    def _extract_organization_data(self, root: etree.Element, ns: dict[str, str]) -> dict[str, Any]:
        """Extract organization data from XML root."""
        org_data = {
            "name": None,
            "website_url": None,
            "mission_description": None,
        }

        # Try various XPath patterns for organization name
        name_elem = root.xpath(".//irs:Filer/irs:BusinessName/irs:BusinessNameLine1Txt", namespaces=ns)
        if name_elem and name_elem[0].text:
            org_data["name"] = name_elem[0].text.strip()

        # Try to find website URL
        website_elem = root.xpath(".//irs:WebsiteAddressTxt", namespaces=ns)
        if website_elem and website_elem[0].text:
            # We don't ensure the URL is valid here because we want to stay faithful to the original data.
            # The URL is prepended with "https://" in the serializer class.
            url = website_elem[0].text.strip()
            org_data["website_url"] = url

        # Try to find mission description
        mission_elem = root.xpath(".//irs:ActivityOrMissionDesc", namespaces=ns)
        if mission_elem and mission_elem[0].text:
            org_data["mission_description"] = mission_elem[0].text.strip().capitalize()

        return org_data

    def _extract_return_data(self, root: etree.Element, ns: dict[str, str]) -> dict[str, Any]:
        """Extract return information from XML root."""
        return_data = {
            "filed_on": None,
            "tax_period_start_date": None,
            "tax_period_end_date": None,
            "employee_count": None,
            "total_revenue": None,
            "total_expenses": None,
            "total_assets_eoy": None,
            "total_assets_boy": None,
            "total_liabilities_eoy": None,
            "total_liabilities_boy": None,
        }

        # Extract tax period dates
        tax_period_start_elem = root.xpath(".//irs:ReturnHeader/irs:TaxPeriodBeginDt", namespaces=ns)
        if tax_period_start_elem and tax_period_start_elem[0].text:
            try:
                return_data["tax_period_start_date"] = self._parse_datetime(tax_period_start_elem[0].text)
            except (ValueError, TypeError):
                logger.debug(f"Error parsing tax period start date: {tax_period_start_elem[0].text}", exc_info=True)
                pass

        tax_period_end_elem = root.xpath(".//irs:ReturnHeader/irs:TaxPeriodEndDt", namespaces=ns)
        if tax_period_end_elem and tax_period_end_elem[0].text:
            try:
                return_data["tax_period_end_date"] = self._parse_datetime(tax_period_end_elem[0].text)
            except (ValueError, TypeError):
                logger.debug(f"Error parsing tax period end date: {tax_period_end_elem[0].text}", exc_info=True)
                pass

        # Extract filed date
        filed_date_elem = root.xpath(".//irs:ReturnHeader/irs:ReturnTs", namespaces=ns)
        if filed_date_elem and filed_date_elem[0].text:
            try:
                return_data["filed_on"] = self._parse_datetime(filed_date_elem[0].text)
            except (ValueError, TypeError):
                logger.debug(f"Error parsing filed date: {filed_date_elem[0].text}", exc_info=True)
                pass

        # 990 PF doesn't seem to have an overall employee count.
        return_data["employee_count"] = None

        # Extract total revenue
        revenue_elem = root.xpath(".//irs:TotalRevAndExpnssAmt", namespaces=ns)
        if revenue_elem and revenue_elem[0].text:
            try:
                return_data["total_revenue"] = self._parse_decimal(revenue_elem[0].text)
            except (ValueError, TypeError):
                logger.debug(f"Error parsing total revenue: {revenue_elem[0].text}", exc_info=True)
                pass

        # Extract total expenses
        expense_elem = root.xpath(".//irs:TotalExpensesRevAndExpnssAmt", namespaces=ns)
        if expense_elem and expense_elem[0].text:
            try:
                return_data["total_expenses"] = self._parse_decimal(expense_elem[0].text)
            except (ValueError, TypeError):
                logger.debug(f"Error parsing total expenses: {expense_elem[0].text}", exc_info=True)
                pass

        # Extract total assets EOY
        asset_elem = root.xpath(".//irs:TotalAssetsEOYAmt", namespaces=ns)
        if asset_elem and asset_elem[0].text:
            try:
                return_data["total_assets_eoy"] = self._parse_decimal(asset_elem[0].text)
            except (ValueError, TypeError):
                logger.debug(f"Error parsing total assets EOY: {asset_elem[0].text}", exc_info=True)
                pass

        # Extract total assets BOY
        asset_boy_elem = root.xpath(".//irs:TotalAssetsBOYAmt", namespaces=ns)
        if asset_boy_elem and asset_boy_elem[0].text:
            try:
                return_data["total_assets_boy"] = self._parse_decimal(asset_boy_elem[0].text)
            except (ValueError, TypeError):
                logger.debug(f"Error parsing total assets BOY: {asset_boy_elem[0].text}", exc_info=True)
                pass

        # Extract total liabilities EOY
        liability_eoy_elem = root.xpath(".//irs:TotalLiabilitiesEOYAmt", namespaces=ns)
        if liability_eoy_elem and liability_eoy_elem[0].text:
            try:
                return_data["total_liabilities_eoy"] = self._parse_decimal(liability_eoy_elem[0].text)
            except (ValueError, TypeError):
                logger.debug(f"Error parsing total liabilities EOY: {liability_eoy_elem[0].text}", exc_info=True)
                pass

        # Extract total liabilities BOY
        liability_boy_elem = root.xpath(".//irs:TotalLiabilitiesBOYAmt", namespaces=ns)
        if liability_boy_elem and liability_boy_elem[0].text:
            try:
                return_data["total_liabilities_boy"] = self._parse_decimal(liability_boy_elem[0].text)
            except (ValueError, TypeError):
                logger.debug(f"Error parsing total liabilities BOY: {liability_boy_elem[0].text}", exc_info=True)
                pass

        return return_data
