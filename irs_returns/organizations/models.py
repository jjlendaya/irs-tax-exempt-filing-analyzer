from django.db import models

from core.models import TimestampedAbstractModel, UUIDAbstractModel


class Organization(UUIDAbstractModel, TimestampedAbstractModel):
    name = models.CharField(max_length=255)
    website_url = models.URLField(max_length=255)
    mission_description = models.TextField()


class OrganizationReturnInformation(UUIDAbstractModel, TimestampedAbstractModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    filed_on = models.DateField()
    tax_period_start_date = models.DateField()
    tax_period_end_date = models.DateField()
    employee_count = models.IntegerField(null=True, blank=True)
    total_revenue = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    total_expenses = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    total_assets = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
