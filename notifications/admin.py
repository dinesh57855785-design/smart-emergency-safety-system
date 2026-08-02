from django.contrib import admin
from .models import SMSNotification


@admin.register(SMSNotification)
class SMSNotificationAdmin(admin.ModelAdmin):
    list_display = ('to_number', 'status', 'sent_at', 'created_at', 'sos_event')
    list_filter = ('status', 'created_at')
    search_fields = ('to_number', 'message', 'twilio_sid')
