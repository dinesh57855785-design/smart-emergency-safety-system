from django.contrib import admin
from .models import LocationPoint


@admin.register(LocationPoint)
class LocationPointAdmin(admin.ModelAdmin):
    list_display = ('user', 'latitude', 'longitude', 'recorded_at')
