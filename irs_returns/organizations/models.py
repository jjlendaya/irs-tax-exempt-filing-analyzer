from django.db import models

from core.models import TimestampedAbstractModel, UUIDAbstractModel


class Organization(UUIDAbstractModel, TimestampedAbstractModel):
    name = models.CharField(max_length=255)
    website_url = models.URLField(max_length=255)
    mission_description = models.TextField()


class OrganizationReturnInformation(UUIDAbstractModel, TimestampedAbstractModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="returns")
    original_file_name = models.CharField(max_length=512, blank=True)
    return_type = models.CharField(max_length=255, blank=True)
    filed_on = models.DateField()
    tax_period_start_date = models.DateField()
    tax_period_end_date = models.DateField()
    employee_count = models.IntegerField(null=True, blank=True)
    py_employee_count = models.IntegerField(null=True, blank=True)
    total_revenue = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
    )
    py_total_revenue = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
    )
    total_expenses = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
    )
    py_total_expenses = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
    )
    total_assets_eoy = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
    )
    total_assets_boy = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
    )
    total_liabilities_eoy = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
    )
    total_liabilities_boy = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
    )


class DatasetJob(UUIDAbstractModel, TimestampedAbstractModel):
    """Track the status of dataset processing jobs."""

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        DOWNLOADING = "DOWNLOADING", "Downloading"
        PROCESSING = "PROCESSING", "Processing"
        COMPLETED = "COMPLETED", "Completed"
        FAILED = "FAILED", "Failed"

    zip_url = models.URLField(max_length=2048)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    progress = models.IntegerField(default=0)  # 0-100
    total_files = models.IntegerField(null=True, blank=True)
    processed_files = models.IntegerField(default=0)
    organizations_created = models.IntegerField(default=0)
    returns_created = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]
