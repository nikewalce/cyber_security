# Импорт моделей Django
from django.db import models


# Модель платформы CTF (например HackTheBox, TryHackMe)
class CTFPlatform(models.Model):
    # Название платформы
    name = models.CharField(max_length=200)


# Модель writeup (разбор CTF задания)
class Writeup(models.Model):
    # Название задания
    title = models.CharField(max_length=200)
    # Платформа, на которой находится задание
    platform = models.ForeignKey(CTFPlatform, on_delete=models.CASCADE)
    # Сложность задания
    difficulty = models.CharField(max_length=50)
    # Описание задания
    description = models.TextField()
    # Решение задания
    solution = models.TextField()
