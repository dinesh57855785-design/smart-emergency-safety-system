from django.contrib import admin
from .models import PoliceStation, PoliceNotification


@admin.register(PoliceStation)
class PoliceStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'latitude', 'longitude')
    search_fields = ('name', 'address')


@admin.register(PoliceNotification)
class PoliceNotificationAdmin(admin.ModelAdmin):
    list_display = ('sos_event', 'police_station', 'status', 'notified_at')
    list_filter = ('status', 'notified_at')
    search_fields = ('payload',)
