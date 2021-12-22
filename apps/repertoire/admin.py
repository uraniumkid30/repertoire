from django.contrib import admin
from .models import (
    Files,
    Works,
)

admin.site.register(Files)
admin.site.register(Works)
