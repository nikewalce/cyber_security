from django.db import models

class LabCategory(models.Model):
    name = models.CharField(max_length=200)

class Lab(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(LabCategory, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=50)
    solution = models.TextField(blank=True)
