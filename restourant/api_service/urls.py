from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import PhoneViewSet, ObjectTypeViewSet, OrganisationViewSet

api_router_v1 = DefaultRouter()
api_router_v1.register(
    'phone',
    PhoneViewSet,
    basename='phone'
)
api_router_v1.register(
    'organisation',
    OrganisationViewSet,
    basename='organisation'
)
api_router_v1.register(
    'type',
    ObjectTypeViewSet,
    basename='object_type'
)

urlpatterns = [
    path('v1/', include(api_router_v1.urls)),
]
