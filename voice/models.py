from django.db import models
from django.contrib.auth.models import User


class VoiceCommand(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='voice_command')
    phrase = models.CharField(max_length=255, help_text='The spoken phrase that triggers SOS')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'VoiceCommand for {self.user.username}: "{self.phrase}"'
