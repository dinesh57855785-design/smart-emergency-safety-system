from django.db import models
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
    return f'profiles/user_{instance.user.id}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f'Profile: {self.user.username}'
