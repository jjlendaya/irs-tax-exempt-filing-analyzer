"""Celery tasks for processing dataset ZIP files."""

from pathlib import Path
import shutil
import tempfile
from uuid import UUID
import zipfile

from celery import shared_task
import requests

from organizations.datasets import process_dataset
from organizations.models import DatasetJob


@shared_task(bind=True, max_retries=3, time_limit=3600, soft_time_limit=3300)
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

        orgs_created, returns_created = process_dataset(zip_path.as_posix(), temp_dir.as_posix(), job)

        # Update job with results
        job.status = DatasetJob.Status.COMPLETED
        job.organizations_created = orgs_created
        job.returns_created = returns_created
        job.progress = 100
        job.save(update_fields=["status", "organizations_created", "returns_created", "progress"])

        return True
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
