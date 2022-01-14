from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("apps.repertoire.urls", namespace="repertoire_api")),
    path("api/v2/", include("apps.stamped_uuid.urls", namespace="stamped_uuid_api")),
]
