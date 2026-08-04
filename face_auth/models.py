import json
from django.conf import settings
from django.db import models


class FaceProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="face_profile",
    )
    descriptor = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_descriptor(self, data):
        self.descriptor = json.dumps(data)

    def get_descriptor(self):
        return json.loads(self.descriptor)

    def __str__(self):
        return f"FaceProfile for {self.user.email}"
