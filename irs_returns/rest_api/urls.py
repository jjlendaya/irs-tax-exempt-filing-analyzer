from rest_framework.routers import DefaultRouter

from rest_api.viewsets.organizations.companies import CompanyViewSet

app_name = "rest_api"

router = DefaultRouter()
router.register(r"companies", CompanyViewSet, basename="company")

urlpatterns = router.urls
