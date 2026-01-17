from rest_framework import serializers

from organizations.models import OrganizationReturnInformation


class OrganizationReturnInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationReturnInformation
        fields = [
            "id",
            "organization",
            "filed_on",
            "tax_period_start_date",
            "tax_period_end_date",
            "employee_count",
            "total_revenue",
            "total_expenses",
            "total_assets",
        ]
