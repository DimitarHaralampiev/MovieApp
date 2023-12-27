from django.contrib.auth.models import User
from django.db import models
from django.db.models import OneToOneField

from user.consts import CITIES
from user.utils import user_directory_path


class LocationUser(models.Model):
    address_1 = models.CharField(max_length=128, blank=True)
    address_2 = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=64, default='Sofia', choices=CITIES)

    def __str__(self):
        return self.id


class UserProfile(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10, blank=True)
    photo_profile = models.ImageField(upload_to=user_directory_path, blank=True)
    location = models.OneToOneField(LocationUser, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username
