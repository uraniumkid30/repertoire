from datetime import datetime
from django.db import models
from django.conf import settings


class Files(models.Model):
    file_name = models.CharField(max_length=255, blank=True, null=True)
    work_count = models.IntegerField(blank=True, null=True)
    updated = models.DateTimeField(null=True, blank=True)
    created = models.DateField(auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name = "File - History"
        verbose_name_plural = "Files - History"

    def __str__(self):
        return f"{self.file_name}"


class Works(models.Model):
    music_file = models.ForeignKey(
        to="Files",
        related_name="music_file",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    proprietary_id = models.IntegerField(null=True, blank=True)
    iswc = models.CharField(max_length=255, null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    contributors = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)
    created = models.DateField(auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name = "Music - Work"
        verbose_name_plural = "Music - Works"

    def save(self, *args, **kwargs):
        # On save, update timestamps
        if not self.id:
            self.update = datetime.today()
        super(Works, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.proprietary_id}"
