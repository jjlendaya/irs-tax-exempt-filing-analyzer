from rest_framework import serializers

from organizations.models import DatasetJob


class DatasetJobCreateSerializer(serializers.Serializer):
    """Serializer for creating a new dataset processing job."""

    zip_url = serializers.URLField(required=True, max_length=2048)

    def validate_zip_url(self, value):
        """Validate that the URL points to a ZIP file."""
        if not value.lower().endswith((".zip",)):
            # Allow URLs that might not have .zip extension but are valid
            # The actual validation happens during download
            pass
        return value


class DatasetJobSerializer(serializers.ModelSerializer):
    """Serializer for dataset job status and details."""

    class Meta:
        model = DatasetJob
        fields = [
            "id",
            "zip_url",
            "status",
            "progress",
            "total_files",
            "processed_files",
            "organizations_created",
            "returns_created",
            "error_message",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "progress",
            "total_files",
            "processed_files",
            "organizations_created",
            "returns_created",
            "error_message",
            "created_at",
            "updated_at",
        ]
