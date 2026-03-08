from django.db import models

class LogFile(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to="logs/")

class LogEvent(models.Model):
    log = models.ForeignKey(LogFile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    event_type = models.CharField(max_length=100)
    message = models.TextField()
