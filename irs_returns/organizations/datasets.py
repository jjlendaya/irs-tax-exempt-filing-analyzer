import logging
from pathlib import Path
import zipfile

from lxml import etree

from organizations.models import DatasetJob, Organization, OrganizationReturnInformation
from organizations.parsers import XMLParser
from organizations.parsers.errors import NoStrategyFoundError

logger = logging.getLogger(__name__)


def _get_xml_files_from_zip(dataset_zip_path: str, extract_dir: Path):
    """Get all XML files from a ZIP file and extract them to a directory."""
    with zipfile.ZipFile(dataset_zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)

    return list(extract_dir.glob("*.xml"))


def process_dataset(dataset_zip_path: str, extract_dir: str, job: DatasetJob | None = None):
    """Process a dataset ZIP file: extract XML files, parse them, and create or update organizations and returns."""
    logger.info("Starting dataset processing...")
    logger.info("-" * 100)
    logger.info(f"Processing dataset ZIP file: {dataset_zip_path}")
    logger.info(f"Extracting ZIP file to: {extract_dir}")
    xml_files = _get_xml_files_from_zip(dataset_zip_path, Path(extract_dir))
    total_files = len(xml_files)
    logger.info(f"Found {total_files} XML files to process.")
    logger.info("-" * 100)

    # Update job status
    if job:
        job.status = DatasetJob.Status.PROCESSING
        job.total_files = total_files
        job.progress = 20
        job.save(update_fields=["status", "total_files", "progress"])

    # Process XML files
    organizations_created = 0
    returns_created = 0
    processed_count = 0
    skipped_count = 0
    total_attempted = 0

    logger.info(f"Processing {total_files} XML files...")
    for xml_file in xml_files:
        total_attempted += 1
        logger.debug("-" * 60)
        logger.debug(f"Processing XML file: {xml_file}")
        try:
            with open(xml_file, "rb") as f:
                xml_content = f.read()

            # Parse XML file
            parsed_data = XMLParser(xml_content).parse()

            # Create or update organization and return information
            org_data = parsed_data["data"]["organization"]
            if org_data.get("name"):
                organization, org_created = Organization.objects.update_or_create(
                    name=org_data["name"],
                    defaults={
                        "website_url": org_data.get("website_url") or "",
                        "mission_description": org_data.get("mission_description") or "",
                    },
                )

                if org_created:
                    organizations_created += 1

                return_data = parsed_data["data"]["return_info"]
                if return_data.get("tax_period_start_date") and return_data.get("tax_period_end_date"):
                    _, return_created = OrganizationReturnInformation.objects.update_or_create(
                        organization=organization,
                        tax_period_start_date=return_data["tax_period_start_date"],
                        tax_period_end_date=return_data["tax_period_end_date"],
                        defaults={
                            "filed_on": return_data.get("filed_on"),
                            "employee_count": return_data.get("employee_count"),
                            "py_employee_count": return_data.get("py_employee_count"),
                            "total_revenue": return_data.get("total_revenue"),
                            "py_total_revenue": return_data.get("py_total_revenue"),
                            "total_expenses": return_data.get("total_expenses"),
                            "py_total_expenses": return_data.get("py_total_expenses"),
                            "total_assets_eoy": return_data.get("total_assets_eoy"),
                            "total_assets_boy": return_data.get("total_assets_boy"),
                            "total_liabilities_eoy": return_data.get("total_liabilities_eoy"),
                            "total_liabilities_boy": return_data.get("total_liabilities_boy"),
                        },
                    )

                    if return_created:
                        returns_created += 1
            processed_count += 1
        except NoStrategyFoundError:
            logger.debug(f"Skipping XML file because no handler was found for this form type: {xml_file}")
            skipped_count += 1
            continue
        except etree.XMLSyntaxError:
            logger.debug(f"Skipping XML file because it is does not contain valid XML: {xml_file}")
            skipped_count += 1
            continue
        except Exception as e:
            # Log error but continue processing other files
            logger.error(f"Unknown error while processing {xml_file}: {str(e)}")
            skipped_count += 1
            continue

        if total_attempted % 100 == 0 or total_attempted == total_files:
            logger.info(
                f"Attempted {total_attempted} of {total_files} files ({round(total_attempted / total_files * 100, 2)}%) - Skipped {skipped_count} files - Processed {processed_count} files"
            )
            logger.info("-" * 60)

            # Update progress
            if job and total_files > 0:
                progress = 20 + int((total_attempted / total_files) * 70)  # 20 - 90% range
                job.progress = progress
                job.processed_files = total_attempted
                job.save(update_fields=["progress", "processed_files"])

    return organizations_created, returns_created
