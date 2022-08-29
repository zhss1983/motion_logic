from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ObjectTypeViewSet, OrganisationByOwnerViewSet, OrganisationViewSet, OwnerViewSet, PhoneViewSet

api_router_v1 = DefaultRouter()
api_router_v1.register("organisation", OrganisationViewSet)
api_router_v1.register("type", ObjectTypeViewSet)
api_router_v1.register("phone", PhoneViewSet)
api_router_v1.register("owner", OwnerViewSet)
api_router_v1.register("organisation_by_owner", OrganisationByOwnerViewSet)


urlpatterns = [
    path("v1/", include(api_router_v1.urls)),
]
