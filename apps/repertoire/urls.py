from django.urls import include, path

# from rest_framework import routers
from rest_framework_nested import routers
from .views import FilesViewset, WorksViewset

# router = routers.DefaultRouter()

# router.register("", WorksViewset, basename="files and works")


router = routers.SimpleRouter()
router.register(r"files", FilesViewset)

works_router = routers.NestedSimpleRouter(router, r"files", lookup="files")
works_router.register(r"works", WorksViewset, basename="works")

app_name = "api"

urlpatterns = [
    path("", include(router.urls)),
    path(r"", include(works_router.urls)),
]
