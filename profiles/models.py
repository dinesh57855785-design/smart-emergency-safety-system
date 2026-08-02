from django.db import models
from django.conf import settings
from django.utils import timezone


def _today():
    return timezone.now().date()


class Profile(models.Model):
    BLOOD_GROUPS = [
        ("A+", "A+"), ("A-", "A-"),
        ("B+", "B+"), ("B-", "B-"),
        ("AB+", "AB+"), ("AB-", "AB-"),
        ("O+", "O+"), ("O-", "O-"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=150, blank=True)
    mobile_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUPS, blank=True)
    height = models.CharField(max_length=20, blank=True, help_text="e.g. 165 cm")
    weight = models.CharField(max_length=20, blank=True, help_text="e.g. 60 kg")
    photo = models.ImageField(upload_to="profile_photos/", blank=True, null=True)
    last_reviewed = models.DateField(default=_today)

    def __str__(self):
        return f"{self.user.email} - Profile"

    def needs_review(self):
        days = (timezone.now().date() - self.last_reviewed).days
        return days >= settings.PROFILE_REVIEW_INTERVAL_DAYS
