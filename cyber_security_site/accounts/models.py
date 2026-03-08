from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/%Y/%m/%d", blank=True)
    github = models.URLField(blank=True)
    skill_level = models.CharField(max_length=50, default="beginner")

    def __str__(self):
        return self.username
