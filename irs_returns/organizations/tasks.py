"""Celery tasks for processing dataset ZIP files."""

from pathlib import Path
import shutil
import tempfile
from uuid import UUID
import zipfile

from celery import shared_task
import requests

from organizations.models import DatasetJob, Organization, OrganizationReturnInformation
from organizations.parsers import parse_irs_990_xml


@shared_task(bind=True, max_retries=3)
def process_dataset_task(self, job_id: str):
    """
    Process a dataset ZIP file: download, extract, parse XML files, and load into database.

    Args:
        job_id: UUID of the DatasetJob to process
    """
    job = DatasetJob.objects.get(id=UUID(job_id))
    temp_dir = None

    try:
        # Update status to DOWNLOADING
        job.status = DatasetJob.Status.DOWNLOADING
        job.progress = 10
        job.save(update_fields=["status", "progress"])

        # Download ZIP file
        temp_dir = Path(tempfile.mkdtemp())
        zip_path = temp_dir / "dataset.zip"

        response = requests.get(
            job.zip_url,
            timeout=300,  # 5 minute timeout
            stream=True,
        )
        response.raise_for_status()

        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # Extract ZIP file
        extract_dir = temp_dir / "extracted"
        extract_dir.mkdir()

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)

        # Count XML files
        xml_files = list(extract_dir.rglob("*.xml"))
        total_files = len(xml_files)

        # Update status to PROCESSING
        job.status = DatasetJob.Status.PROCESSING
        job.total_files = total_files
        job.progress = 20
        job.save(update_fields=["status", "total_files", "progress"])

        # Process each XML file
        organizations_created = 0
        returns_created = 0
        processed_count = 0

        for xml_file in xml_files:
            try:
                with open(xml_file, "rb") as f:
                    xml_content = f.read()

                # Parse XML
                parsed_data = parse_irs_990_xml(xml_content)

                # Create or update organization
                org_data = parsed_data["organization"]
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

                    # Create or update return information
                    return_data = parsed_data["return_info"]
                    if return_data.get("tax_period_start_date") and return_data.get("tax_period_end_date"):
                        return_info, return_created = OrganizationReturnInformation.objects.update_or_create(
                            organization=organization,
                            tax_period_start_date=return_data["tax_period_start_date"],
                            tax_period_end_date=return_data["tax_period_end_date"],
                            defaults={
                                "filed_on": return_data.get("filed_on"),
                                "employee_count": return_data.get("employee_count"),
                                "total_revenue": return_data.get("total_revenue"),
                                "total_expenses": return_data.get("total_expenses"),
                                "total_assets": return_data.get("total_assets"),
                            },
                        )

                        if return_created:
                            returns_created += 1

            except Exception as e:
                # Log error but continue processing other files
                # In production, you might want to log this to a proper logging system
                print(f"Error processing {xml_file}: {str(e)}")
                continue

            processed_count += 1

            # Update progress
            if total_files > 0:
                progress = 20 + int((processed_count / total_files) * 70)  # 20-90% range
                job.progress = progress
                job.processed_files = processed_count
                job.save(update_fields=["progress", "processed_files"])

        # Update final status
        job.status = DatasetJob.Status.COMPLETED
        job.progress = 100
        job.organizations_created = organizations_created
        job.returns_created = returns_created
        job.save(
            update_fields=[
                "status",
                "progress",
                "organizations_created",
                "returns_created",
            ],
        )

    except requests.RequestException as e:
        job.status = DatasetJob.Status.FAILED
        job.error_message = f"Failed to download ZIP file: {str(e)}"
        job.save(update_fields=["status", "error_message"])
        raise

    except zipfile.BadZipFile as e:
        job.status = DatasetJob.Status.FAILED
        job.error_message = f"Invalid ZIP file: {str(e)}"
        job.save(update_fields=["status", "error_message"])
        raise

    except Exception as e:
        job.status = DatasetJob.Status.FAILED
        job.error_message = f"Processing error: {str(e)}"
        job.save(update_fields=["status", "error_message"])
        raise

    finally:
        # Cleanup temporary files
        if temp_dir and temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)
