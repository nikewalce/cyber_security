from django.db import models

class SecurityTool(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    official_site = models.URLField(blank=True)
    github = models.URLField(blank=True)
    difficulty = models.CharField(max_length=50)
