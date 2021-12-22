from django.db import transaction
from rest_framework import serializers
from rest_framework import fields
from rest_framework.fields import empty

from .models import Files, Works
from django.forms.models import model_to_dict


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = (
            "file_name",
            "work_count",
            "updated",
            "created",
        )


class WorkSerializer(serializers.ModelSerializer):
    music_file = FileSerializer(required=False)

    class Meta:
        model = Works
        fields = (
            "music_file",
            "proprietary_id",
            "iswc",
            "source",
            "title",
            "contributors",
            "updated",
            "created",
        )
