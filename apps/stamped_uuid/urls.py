from django.urls import include, path

from rest_framework import routers

from .views import TimeStampedUUIDViewset

router = routers.DefaultRouter()

router.register("", TimeStampedUUIDViewset, basename="time stamped uuid")


app_name = "stamped_uuid_api"

urlpatterns = [
    path("stamped_uuid/", include(router.urls)),
]
