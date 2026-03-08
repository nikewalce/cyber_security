from django.db import models

class Roadmap(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

class RoadmapStep(models.Model):
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField()
