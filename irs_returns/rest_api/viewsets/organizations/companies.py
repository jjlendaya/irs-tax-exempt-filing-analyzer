from rest_framework import viewsets

from organizations.models import Organization
from rest_api.serializers.organizations.companies import CompanySerializer


class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for companies endpoint combining Organization with related returns."""

    queryset = Organization.objects.prefetch_related("returns").all()
    serializer_class = CompanySerializer
