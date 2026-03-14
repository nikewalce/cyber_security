# Импорт системы моделей Django
from django.db import models


# Модель категории статей
class Category(models.Model):
    # Название категории
    name = models.CharField(max_length=200)
    # URL-friendly название (используется в ссылках)
    # Например: web-security
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


# Модель статьи
class Article(models.Model):
    # Заголовок статьи
    title = models.CharField(max_length=300)
    # Slug для URL статьи
    slug = models.SlugField(unique=True)
    # Основной текст статьи
    content = models.TextField()
    # Связь с категорией
    # Одна категория может иметь много статей
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="articles"
    )
    # Дата создания статьи
    created_at = models.DateTimeField(auto_now_add=True)
    # Дата изменения статьи
    updated_at = models.DateTimeField(auto_now=True)

    # индексы ускоряют запросы к базе
    class Meta:
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.title
