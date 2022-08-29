from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api_service.urls")),
    path("api/", include("parser.urls")),
]
