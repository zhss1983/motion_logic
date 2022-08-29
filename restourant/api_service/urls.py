from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ObjectTypeViewSet, OrganisationViewSet, OwnerViewSet, PhoneViewSet

api_router_v1 = DefaultRouter()
api_router_v1.register("organisation", OrganisationViewSet, basename="organisation")
api_router_v1.register("type", ObjectTypeViewSet, basename="object_type")
api_router_v1.register("phone", PhoneViewSet, basename="phone")
api_router_v1.register("owner", OwnerViewSet, basename="phone")

urlpatterns = [
    path("v1/", include(api_router_v1.urls)),
]
