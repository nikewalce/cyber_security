# Импортируем систему моделей Django
from django.db import models


# Модель категории лабораторных работ
class LabCategory(models.Model):
    # Название категории
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# Модель лабораторной работы
class Lab(models.Model):
    # выбор для сложности задания
    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]
    # Название лабораторной
    title = models.CharField(max_length=200)
    # Описание задания
    description = models.TextField()
    # Связь с категорией (одна категория может иметь много лабораторных)
    category = models.ForeignKey(LabCategory, on_delete=models.CASCADE)
    # Сложность задания (например Easy / Medium / Hard)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    # Решение задания (может быть пустым)
    solution = models.TextField(blank=True)

    def __str__(self):
        return self.title


# Модель формы с комментариями, для проверки Stored XSS
class Comment(models.Model):
    # введенный текст в форме
    text = models.CharField(max_length=200)
    # дата создания комментария
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
