# Импортируем модуль админ панели Django
from django.contrib import admin

# Импортируем модели из текущего приложения
from .models import Lab, LabCategory


# Регистрируем модель LabCategory в админ панели
@admin.register(LabCategory)
class LabCategoryAdmin(admin.ModelAdmin):
    # Поля, которые будут отображаться в списке категорий
    list_display = ("id", "name")
    # Поля, по которым можно искать категории
    search_fields = ("name",)


# Регистрируем модель Lab в админ панели
@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    # Поля, которые отображаются в списке лабораторных
    list_display = (
        "id",
        "title",
        "category",
        "difficulty",
    )
    # Фильтры справа в админ панели
    list_filter = (
        "category",
        "difficulty",
    )
    # Поля, по которым работает поиск
    search_fields = (
        "title",
        "description",
    )
