from rest_framework import serializers

from organizations.models import Organization, OrganizationReturnInformation
from rest_api.formatters.common import to_paragraph_case


class OrganizationReturnInformationNestedSerializer(serializers.ModelSerializer):
    """Nested serializer for OrganizationReturnInformation (excludes organization field)."""

    filed_on = serializers.SerializerMethodField()
    tax_period_start_date = serializers.SerializerMethodField()
    tax_period_end_date = serializers.SerializerMethodField()

    class Meta:
        model = OrganizationReturnInformation
        fields = [
            "filed_on",
            "tax_period_start_date",
            "tax_period_end_date",
            "employee_count",
            "py_employee_count",
            "total_revenue",
            "py_total_revenue",
            "total_expenses",
            "py_total_expenses",
            "total_assets_eoy",
            "total_assets_boy",
            "total_liabilities_eoy",
            "total_liabilities_boy",
        ]

    def get_filed_on(self, obj: OrganizationReturnInformation) -> str | None:
        if not obj.filed_on:
            return None

        return obj.filed_on.isoformat()

    def get_tax_period_start_date(self, obj: OrganizationReturnInformation) -> str | None:
        if not obj.tax_period_start_date:
            return None

        return obj.tax_period_start_date.isoformat()

    def get_tax_period_end_date(self, obj: OrganizationReturnInformation) -> str | None:
        if not obj.tax_period_end_date:
            return None

        return obj.tax_period_end_date.isoformat()


class CompanySerializer(serializers.ModelSerializer):
    """Serializer for Organization with nested related OrganizationReturnInformation."""

    name = serializers.SerializerMethodField()
    website_url = serializers.SerializerMethodField()
    mission_description = serializers.SerializerMethodField()
    returns = OrganizationReturnInformationNestedSerializer(
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

    def get_name(self, obj: Organization) -> str | None:
        if not obj.name:
            return None

        return obj.name.title()

    def get_website_url(self, obj: Organization) -> str | None:
        if not obj.website_url:
            return None

        if not obj.website_url.startswith(("http://", "https://")):
            return f"https://{obj.website_url.lower().strip()}"

        return obj.website_url

    def get_mission_description(self, obj: Organization) -> str | None:
        if not obj.mission_description:
            return None

        return to_paragraph_case(obj.mission_description)
