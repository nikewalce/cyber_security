from django.db import models

class UserProgress(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    completed_labs = models.IntegerField(default=0)
    completed_articles = models.IntegerField(default=0)
