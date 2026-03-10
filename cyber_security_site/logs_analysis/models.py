# Импорт моделей Django
from django.db import models


# Модель файла логов
class LogFile(models.Model):
    # Название лог файла
    name = models.CharField(max_length=200)
    # Описание файла
    description = models.TextField()
    # Сам файл логов
    # Загружается в папку media/logs/
    file = models.FileField(upload_to="logs/")


# Модель события в логе
class LogEvent(models.Model):
    # Связь с лог файлом
    # Один файл может содержать много событий
    log = models.ForeignKey(LogFile, on_delete=models.CASCADE)
    # Время события
    timestamp = models.DateTimeField()
    # Тип события (например: ERROR, WARNING, INFO)
    event_type = models.CharField(max_length=100)
    # Сообщение события
    message = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=["timestamp"]),
            models.Index(fields=["event_type"]),
        ]
