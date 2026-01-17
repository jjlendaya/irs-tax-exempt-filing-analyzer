from rest_framework import viewsets

from organizations.models import Organization
from rest_api.serializers.organizations.organizations import OrganizationSerializer


class OrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
