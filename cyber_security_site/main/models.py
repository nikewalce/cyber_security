# Импорт моделей Django
from django.db import models


# Модель новости
class News(models.Model):
    # Заголовок новости
    title = models.CharField(max_length=200)
    # Текст новости
    content = models.TextField()
    # Дата создания
    created_at = models.DateTimeField(auto_now_add=True)
    # Slug для URL
    slug = models.SlugField(unique=True)

    class Meta:
        # Сортировка по названию
        ordering = ("title",)
        # Название модели в админке (единственное число)
        verbose_name = "Новость"
        # Название модели во множественном числе
        verbose_name_plural = "Новости"

    # Строковое представление объекта
    # Будет отображаться в админ панели
    def __str__(self):
        return self.title
