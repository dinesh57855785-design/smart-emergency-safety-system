from django.db import models
from django.contrib.auth.models import User


class LocationPoint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Location {self.user.username} @ {self.recorded_at}'
