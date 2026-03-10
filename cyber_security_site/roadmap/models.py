# Импорт моделей Django
from django.db import models


# Модель Roadmap (план обучения)
class Roadmap(models.Model):
    # Название roadmap
    title = models.CharField(max_length=200)
    # Описание roadmap
    description = models.TextField()


# Модель шага roadmap
class RoadmapStep(models.Model):
    # Связь с roadmap
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE)
    # Название шага
    title = models.CharField(max_length=200)
    # Описание шага
    description = models.TextField()
    # Порядок шага
    order = models.IntegerField()

    # чтобы order был уникальный
    class Meta:
        unique_together = ["roadmap", "order"]
