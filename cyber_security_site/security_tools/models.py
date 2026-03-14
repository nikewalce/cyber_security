# Импорт моделей Django
from django.db import models


# Модель инструмента кибербезопасности
class SecurityTool(models.Model):
    # Название инструмента
    name = models.CharField(max_length=200)
    # Slug для URL
    slug = models.SlugField(unique=True)
    # Описание инструмента
    description = models.TextField()
    # Официальный сайт инструмента
    official_site = models.URLField(blank=True)
    # GitHub репозиторий инструмента
    github = models.URLField(blank=True)
    # Уровень сложности изучения инструмента
    difficulty = models.CharField(max_length=50)

    def steps_used_in(self):
        """
        Возвращает все шаги roadmap, где используется этот инструмент.
        """
        return self.steps.all()

    def __str__(self):
        return self.name
