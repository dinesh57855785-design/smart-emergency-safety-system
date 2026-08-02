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
    search_fields = ('payload', 'police_station__name', 'sos_event__id')
    ordering = ('-notified_at',)

    actions = ['create_video_session']

    def create_video_session(self, request, queryset):
        """Admin action: create a video session for the selected police notifications."""
        from video.services import create_video_session
        created = 0
        for pn in queryset:
            try:
                vs = create_video_session(pn.sos_event, user=pn.sos_event.user)
                created += 1
            except Exception:
                pass
        self.message_user(request, f'Created {created} video sessions')

    create_video_session.short_description = 'Create video session for selected notifications'
