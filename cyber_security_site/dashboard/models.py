# Импорт моделей Django
from django.db import models


# Модель прогресса пользователя
class UserProgress(models.Model):
    # Связь с пользователем (модель пользователя из приложения accounts)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    # Количество выполненных лабораторных
    completed_labs = models.IntegerField(default=0)
    # Количество прочитанных статей / writeups
    completed_articles = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)
