# Импорт моделей Django
from django.db import models


# Модель платформы CTF (например HackTheBox, TryHackMe)
class CTFPlatform(models.Model):
    # Название платформы
    name = models.CharField(max_length=200)
    # slug для красивого URL
    slug = models.SlugField(unique=True)

    # строковое представление объекта
    def __str__(self):
        return self.name


# Модель writeup (разбор CTF задания)
class Writeup(models.Model):
    # Название задания
    title = models.CharField(max_length=200)

    # Платформа, на которой находится задание
    # HackTheBox
    # ├── Blue
    # ├── Lame
    # └── Optimum
    platform = models.ForeignKey(
        CTFPlatform, on_delete=models.CASCADE, related_name="writeups"
    )
    # Сложность задания
    difficulty = models.CharField(max_length=50)
    # Описание задания
    description = models.TextField()
    # Решение задания
    solution = models.TextField()
    # slug для красивого URL
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title
