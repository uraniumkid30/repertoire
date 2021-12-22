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
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [
    #     IsAuthenticated,
    # ]
    queryset = Files.objects.all()

    serializer_class = FileSerializer

    def list(
        self,
        request,
    ):
        serializer = FileSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        client = get_object_or_404(self.queryset, pk=pk)
        serializer = FileSerializer(client)
        return Response(serializer.data)


class WorksViewset(viewsets.ViewSet):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [
    #     IsAuthenticated,
    # ]
    queryset = Works.objects.all()

    serializer_class = WorkSerializer

    def list(
        self,
        request,
    ):
        serializer = WorkSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        client = get_object_or_404(self.queryset, pk=pk)
        serializer = WorkSerializer(client)
        return Response(serializer.data)