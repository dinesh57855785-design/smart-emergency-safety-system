import uuid
from django.db import models
from django.conf import settings


class SOSEvent(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("resolved", "Resolved"),
        ("false_alarm", "False Alarm"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sos_events")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    location_url = models.URLField(blank=True)
    video_room_name = models.CharField(max_length=150, blank=True)
    video_room_url = models.URLField(blank=True)
    voice_message = models.FileField(upload_to="voice_messages/", blank=True, null=True)
    police_station_name = models.CharField(max_length=255, blank=True)
    police_station_address = models.TextField(blank=True)
    police_station_phone = models.CharField(max_length=20, blank=True)
    sms_status = models.CharField(max_length=255, blank=True, default="pending")
    video_status = models.CharField(max_length=50, blank=True, default="pending")
    voice_status = models.CharField(max_length=50, blank=True, default="pending")
    police_status = models.CharField(max_length=255, blank=True, default="pending")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    triggered_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-triggered_at"]

    def __str__(self):
        return f"SOS {self.id} - {self.user.email}"


class SOSEventContact(models.Model):
    sos_event = models.ForeignKey(SOSEvent, on_delete=models.CASCADE, related_name="notified_contacts")
    name = models.CharField(max_length=150)
    relationship = models.CharField(max_length=100, blank=True)
    mobile_number = models.CharField(max_length=20)
    sms_sent = models.BooleanField(default=False)
    sms_error = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.name} ({self.mobile_number})"
