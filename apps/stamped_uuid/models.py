from datetime import datetime
from sqlite3 import Timestamp
from django.db import models
from django.conf import settings
import uuid


class TimeStampedUUID(models.Model):
    ALLOWED_COUNT_PER_DAY: int = (
        50  # sorry mate i cant let you have more than this number of items per day.
    )
    timestamp_identity = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True
    )
    updated = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def can_create_more_rows(self):
        daily_count: int = self.__class__.objects.filter(
            created__month=datetime.today().month,
            created__day=datetime.today().day,
        ).count()
        return daily_count < self.ALLOWED_COUNT_PER_DAY

    def save(self, *args, **kwargs):
        if self.can_create_more_rows():
            super(TimeStampedUUID, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.timestamp_identity} - {self.created}"
