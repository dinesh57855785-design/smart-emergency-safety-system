from django.contrib import admin
from .models import VideoSession


@admin.register(VideoSession)
class VideoSessionAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'sos_event', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('room_name', 'sos_event__id', 'user__username')
