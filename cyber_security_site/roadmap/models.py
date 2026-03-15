# Импорт моделей Django
from django.db import models

# Что делает slugify: переводит текст в lowercase (Web Pentesting → web pentesting)
# удаляет спецсимволы (SQL Injection!!! → sql injection)
# заменяет пробелы на дефис (sql injection → sql-injection)
from django.utils.text import slugify


# Модель Roadmap (план обучения)
class Roadmap(models.Model):
    # Название roadmap
    title = models.CharField(max_length=200)
    # Описание roadmap
    description = models.TextField()
    # Уникальный слаг
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


# Модель шага roadmap
class RoadmapStep(models.Model):
    # Связь с roadmap
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE, related_name="steps")
    # Название шага
    title = models.CharField(max_length=200)
    # Описание шага
    description = models.TextField()
    # Порядок шага
    order = models.IntegerField()
    # Уникальный слаг
    slug = models.SlugField(blank=True)
    # связь с инструментами
    # один шаг roadmap может включать несколько инструментов
    # один инструмент может использоваться в нескольких шагах
    tools = models.ManyToManyField(
        "security_tools.SecurityTool", blank=True, related_name="steps"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            # проверяем, есть ли такой slug в этом roadmap
            while RoadmapStep.objects.filter(roadmap=self.roadmap, slug=slug).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)

    # чтобы order был уникальный
    class Meta:
        unique_together = [["roadmap", "order"], ["roadmap", "slug"]]
        ordering = ["order"]

    def __str__(self):
        return self.title
