"""Parser for IRS Form 990 XML files."""

from datetime import date
from decimal import Decimal
from typing import Any

from lxml import etree


def parse_irs_990_xml(xml_content: bytes) -> dict[str, Any]:
    """
    Parse an IRS Form 990 XML file and extract organization and return information.

    Args:
        xml_content: The XML file content as bytes

    Returns:
        Dictionary with keys:
        - organization: dict with name, website_url, mission_description
        - return_info: dict with filed_on, tax_period_start_date, tax_period_end_date,
          employee_count, total_revenue, total_expenses, total_assets
    """
    # Parse XML with namespace support
    root = etree.fromstring(xml_content)

    # IRS Form 990 XML typically uses this namespace
    ns = {"irs": "http://www.irs.gov/efile"}

    # Try to find namespace from root element if present
    if root.nsmap:
        # Use the default namespace or first namespace found
        default_ns = root.nsmap.get(None) or list(root.nsmap.values())[0]
        ns = {"irs": default_ns}

    # Extract organization information
    organization_data = _extract_organization_data(root, ns)

    # Extract return information
    return_data = _extract_return_data(root, ns)

    return {
        "organization": organization_data,
        "return_info": return_data,
    }


def _extract_organization_data(root: etree.Element, ns: dict[str, str]) -> dict[str, Any]:
    """Extract organization data from XML root."""
    org_data = {
        "name": None,
        "website_url": None,
        "mission_description": None,
    }

    # Try various XPath patterns for organization name
    name_paths = [
        ".//irs:BusinessName/irs:BusinessNameLine1Txt",
        ".//irs:BusinessNameLine1Txt",
        ".//irs:NameBusiness/BusinessNameLine1Txt",
            ".//irs:OrganizationName/irs:BusinessNameLine1Txt",
    ]
    for path in name_paths:
        name_elem = root.xpath(path, namespaces=ns)
        if name_elem and name_elem[0].text:
            org_data["name"] = name_elem[0].text.strip()
            break

    # If no name found, try alternative patterns
    if not org_data["name"]:
        name_elem = root.xpath(".//irs:BusinessName", namespaces=ns)
        if name_elem and name_elem[0].text:
            org_data["name"] = name_elem[0].text.strip()

    # Try to find website URL
    website_paths = [
        ".//irs:WebsiteAddressTxt",
        ".//irs:WebsiteAddress",
        ".//irs:WebSite",
    ]
    for path in website_paths:
        website_elem = root.xpath(path, namespaces=ns)
        if website_elem and website_elem[0].text:
            url = website_elem[0].text.strip()
            # Ensure URL has protocol
            if url and not url.startswith(("http://", "https://")):
                url = f"https://{url}"
            org_data["website_url"] = url
            break

    # Try to find mission description
    mission_paths = [
        ".//irs:ActivityOrMissionDesc",
        ".//irs:MissionDesc",
        ".//irs:PrimaryExemptPurposeTxt",
    ]
    for path in mission_paths:
        mission_elem = root.xpath(path, namespaces=ns)
        if mission_elem and mission_elem[0].text:
            org_data["mission_description"] = mission_elem[0].text.strip()
            break

    return org_data


def _extract_return_data(root: etree.Element, ns: dict[str, str]) -> dict[str, Any]:
    """Extract return information from XML root."""
    return_data = {
        "filed_on": None,
        "tax_period_start_date": None,
        "tax_period_end_date": None,
        "employee_count": None,
        "total_revenue": None,
        "total_expenses": None,
        "total_assets": None,
    }

    # Extract tax period dates
    tax_period_start_paths = [
        ".//irs:TaxPeriodBeginDt",
        ".//irs:TaxPeriodStartDt",
        ".//irs:TaxYearBeginDt",
    ]
    for path in tax_period_start_paths:
        elem = root.xpath(path, namespaces=ns)
        if elem and elem[0].text:
            return_data["tax_period_start_date"] = _parse_date(elem[0].text)
            break

    tax_period_end_paths = [
        ".//irs:TaxPeriodEndDt",
        ".//irs:TaxYearEndDt",
    ]
    for path in tax_period_end_paths:
        elem = root.xpath(path, namespaces=ns)
        if elem and elem[0].text:
            return_data["tax_period_end_date"] = _parse_date(elem[0].text)
            break

    # Extract filed date
    filed_date_paths = [
        ".//irs:ReturnTs",
        ".//irs:DateOfFiling",
        ".//irs:FilingDate",
    ]
    for path in filed_date_paths:
        elem = root.xpath(path, namespaces=ns)
        if elem and elem[0].text:
            return_data["filed_on"] = _parse_date(elem[0].text)
            break

    # Extract employee count
    employee_paths = [
        ".//irs:TotalEmployeeCnt",
        ".//irs:EmployeeCnt",
        ".//irs:NumEmployees",
    ]
    for path in employee_paths:
        elem = root.xpath(path, namespaces=ns)
        if elem and elem[0].text:
            try:
                return_data["employee_count"] = int(float(elem[0].text))
            except (ValueError, TypeError):
                pass
            break

    # Extract total revenue
    revenue_paths = [
        ".//irs:TotalRevenueColumnA",
        ".//irs:TotalRevenue",
        ".//irs:GrossReceipts",
        ".//irs:TotalGrossReceipts",
    ]
    for path in revenue_paths:
        elem = root.xpath(path, namespaces=ns)
        if elem and elem[0].text:
            try:
                return_data["total_revenue"] = _parse_decimal(elem[0].text)
            except (ValueError, TypeError):
                pass
            break

    # Extract total expenses
    expense_paths = [
        ".//irs:TotalExpensesColumnA",
        ".//irs:TotalExpenses",
        ".//irs:TotalExpensesAmt",
    ]
    for path in expense_paths:
        elem = root.xpath(path, namespaces=ns)
        if elem and elem[0].text:
            try:
                return_data["total_expenses"] = _parse_decimal(elem[0].text)
            except (ValueError, TypeError):
                pass
            break

    # Extract total assets
    asset_paths = [
        ".//irs:TotalAssetsEOYAmt",
        ".//irs:TotalAssets",
        ".//irs:TotalAssetsEndOfYear",
    ]
    for path in asset_paths:
        elem = root.xpath(path, namespaces=ns)
        if elem and elem[0].text:
            try:
                return_data["total_assets"] = _parse_decimal(elem[0].text)
            except (ValueError, TypeError):
                pass
            break

    return return_data


def _parse_date(date_str: str | None) -> date | None:
    """Parse date string in various formats to date object."""
    if not date_str:
        return None

    date_str = date_str.strip()

    # Try common date formats
    date_formats = [
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%d/%m/%Y",
        "%Y%m%d",
    ]

    for fmt in date_formats:
        try:
            from datetime import datetime

            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue

    return None


def _parse_decimal(value: str | None) -> Decimal | None:
    """Parse decimal string to Decimal object."""
    if not value:
        return None

    try:
        # Remove commas and whitespace
        cleaned = value.replace(",", "").strip()
        return Decimal(cleaned)
    except (ValueError, TypeError):
        return None
