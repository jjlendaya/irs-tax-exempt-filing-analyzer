from rest_framework import serializers, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from organizations.models import DatasetJob
from organizations.tasks import process_dataset_task
from rest_api.serializers.dataset import DatasetJobCreateSerializer, DatasetJobSerializer


class DatasetViewSet(viewsets.ModelViewSet):
    """ViewSet for dataset processing jobs."""

    queryset = DatasetJob.objects.all()
    serializer_class = DatasetJobSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"

    def create(self, request, *args, **kwargs):
        """
        Create a new dataset processing job.

        POST /api/dataset/
        Body: {"zip_url": "https://example.com/data.zip"}
        """
        create_serializer = DatasetJobCreateSerializer(data=request.data)
        try:
            create_serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        # Create the job
        job = DatasetJob.objects.create(
            zip_url=create_serializer.validated_data["zip_url"],
            status=DatasetJob.Status.PENDING,
        )

        # Enqueue the Celery task
        process_dataset_task.delay(str(job.id))

        # Return the job details
        serializer = self.get_serializer(job)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
