from django.contrib import admin
from notifications.models import SMSNotification
from police.models import PoliceNotification
from video.models import VideoSession

# update notifications admin
@admin.register(SMSNotification)
class SMSNotificationAdmin(admin.ModelAdmin):
    list_display = ('to_number', 'status', 'sent_at', 'created_at', 'sos_event')
    list_filter = ('status', 'created_at')
    search_fields = ('to_number', 'message', 'twilio_sid', 'sos_event__id')
    ordering = ('-created_at',)


# police admin already registered but ensure ordering
@admin.register(PoliceNotification)
class PoliceNotificationAdmin(admin.ModelAdmin):
    list_display = ('sos_event', 'police_station', 'status', 'notified_at')
    list_filter = ('status', 'notified_at')
    search_fields = ('payload', 'police_station__name', 'sos_event__id')
    ordering = ('-notified_at',)


@admin.register(VideoSession)
class VideoSessionAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'sos_event', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('room_name', 'sos_event__id', 'user__username')
    ordering = ('-created_at',)
