from rest_framework import serializers

from organizations.models import Organization, OrganizationReturnInformation


class OrganizationReturnInformationNestedSerializer(serializers.ModelSerializer):
    """Nested serializer for OrganizationReturnInformation (excludes organization field)."""

    class Meta:
        model = OrganizationReturnInformation
        fields = [
            "id",
            "filed_on",
            "tax_period_start_date",
            "tax_period_end_date",
            "employee_count",
            "total_revenue",
            "total_expenses",
            "total_assets",
            "created_at",
            "updated_at",
        ]


class CompanySerializer(serializers.ModelSerializer):
    """Serializer for Organization with nested related OrganizationReturnInformation."""

    returns = OrganizationReturnInformationNestedSerializer(
        source="returns",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "website_url",
            "mission_description",
            "created_at",
            "updated_at",
            "returns",
        ]
