from django.db import transaction
from rest_framework import serializers
from rest_framework import fields
from rest_framework.fields import empty

from .models import TimeStampedUUID
from django.forms.models import model_to_dict


class TimeStampedUUIDSerializer(serializers.BaseSerializer):
    def to_internal_value(self, data):
        return data

    def to_representation(self, instance: TimeStampedUUID):
        result = {
            instance.created.strftime(
                "%Y-%m-%d %H:%M:%S.%f"
            ): instance.timestamp_identity
        }
        return result

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
