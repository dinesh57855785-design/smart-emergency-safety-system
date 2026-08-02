import uuid
from django.db import models
from django.conf import settings


class VoiceMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="voice_messages")
    audio_file = models.FileField(upload_to="voice_messages/")
    transcript = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Voice {self.id} - {self.user.email}"
