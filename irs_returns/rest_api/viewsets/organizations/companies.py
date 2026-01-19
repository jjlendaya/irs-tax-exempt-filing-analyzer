from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from organizations.models import Organization
from rest_api.serializers.organizations.companies import CompanySerializer


class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for companies endpoint combining Organization with related returns."""

    permission_classes = [AllowAny]
    queryset = Organization.objects.prefetch_related("returns").all().order_by("name")
    serializer_class = CompanySerializer
