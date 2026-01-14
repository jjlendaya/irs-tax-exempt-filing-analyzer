from rest_framework import serializers
from organizations.models import Organization, OrganizationReturnInformation


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "website_url",
            "mission_description",
        ]


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
