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
    PageNumberPagination,
)
from django.shortcuts import get_object_or_404
import os
import uuid
from .models import Works, Files
from .serializers import (
    FileSerializer,
    WorkSerializer,
)

from django.contrib.auth import get_user_model
from django.apps import apps
from django.views import View
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponseForbidden
import traceback
import logging

# Create your views here.


class FilesViewset(viewsets.ViewSet):
    queryset = Files.objects.all()

    serializer_class = FileSerializer

    def list(self, request, *args, **kwargs):
        serializer = FileSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        client = get_object_or_404(self.queryset, pk=pk)
        serializer = FileSerializer(client)
        return Response(serializer.data)


class WorksViewset(viewsets.ViewSet):
    serializer_class = WorkSerializer

    def get_queryset(self, pk=None, **kwargs):
        files_pk = kwargs.get("files_pk")
        music_file = Files.objects.filter(pk=files_pk)
        query = {}
        if music_file.exists():
            query.update({"music_file": music_file.first()})
        if pk:
            query.update({"pk": pk})
        result = Works.objects.filter(**query)
        return result

    def list(self, request, *args, **kwargs):
        client = self.get_queryset(**kwargs)
        serializer = WorkSerializer(client, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        client = self.get_queryset(pk=pk, **kwargs)

        serializer = WorkSerializer(client.first())
        return Response(serializer.data if client.count() else {})
