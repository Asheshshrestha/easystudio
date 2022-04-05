from django.contrib import admin
from apps.v1.studio.models import StudioProfile,StudioRating

# Register your models here.

admin.site.register(StudioProfile)
admin.site.register(StudioRating)