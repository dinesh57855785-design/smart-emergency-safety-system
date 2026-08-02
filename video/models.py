import uuid
from django.db import models
from django.conf import settings


class VideoSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="video_sessions")
    room_name = models.CharField(max_length=150)
    room_url = models.URLField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.room_name} ({self.user.email})"


class OfflineRecording(models.Model):
    UPLOAD_STATUS = [
        ("pending", "Pending"),
        ("uploaded", "Uploaded"),
        ("failed", "Failed"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="offline_recordings")
    video_file = models.FileField(upload_to="offline_recordings/")
    recorded_at = models.DateTimeField(auto_now_add=True)
    upload_status = models.CharField(max_length=20, choices=UPLOAD_STATUS, default="pending")
    synced_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Recording {self.id} - {self.user.email}"
