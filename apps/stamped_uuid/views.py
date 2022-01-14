from django.shortcuts import render
import json
from rest_framework import status, viewsets

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from apps.services.utils.rest_utils import (
    GoodResponse,
    BadResponse,
    CustomPaginator,
)
from django.shortcuts import get_object_or_404
import os
import uuid
from datetime import datetime
from .models import TimeStampedUUID
from .serializers import TimeStampedUUIDSerializer

from django.contrib.auth import get_user_model
from django.apps import apps
from django.views import View
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponseForbidden
import traceback
import logging


class TimeStampedUUIDViewset(viewsets.ViewSet):
    queryset = TimeStampedUUID.objects.all().order_by("-created")
    serializer_class = TimeStampedUUIDSerializer

    def list(self, request, *args, **kwargs):
        TimeStampedUUID.objects.create()
        current_count_today = self.queryset.filter(
            created__month=datetime.today().month,
            created__day=datetime.today().day,
        ).count()
        daily_limit = TimeStampedUUID.ALLOWED_COUNT_PER_DAY
        serializer = self.serializer_class(self.queryset, many=True)
        results = {
            item: dict(row)[item] for row in serializer.data for item in dict(row)
        }
        response_result = {
            "results": results,
            "current_count_today": current_count_today,
            "daily_limit": daily_limit,
        }

        return Response(response_result, status=status.HTTP_200_OK)
