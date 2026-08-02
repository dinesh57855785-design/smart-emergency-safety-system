from django.db import models
from django.contrib.auth.models import User


def default_room_name():
    return ''


class VideoSession(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('ended', 'Ended'),
    ]

    sos_event = models.ForeignKey('sos.SosEvent', on_delete=models.CASCADE, related_name='video_sessions')
    room_name = models.CharField(max_length=255)
    meeting_url = models.URLField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'VideoSession {self.room_name} ({self.status})'
