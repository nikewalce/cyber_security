from django.db import models

class CTFPlatform(models.Model):
    name = models.CharField(max_length=200)

class Writeup(models.Model):
    title = models.CharField(max_length=200)
    platform = models.ForeignKey(CTFPlatform, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=50)
    description = models.TextField()
    solution = models.TextField()
