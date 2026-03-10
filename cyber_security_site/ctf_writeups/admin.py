# Импорт админ панели Django
from django.contrib import admin

# Импорт моделей
from .models import CTFPlatform, Writeup


# Регистрация платформы CTF
@admin.register(CTFPlatform)
class CTFPlatformAdmin(admin.ModelAdmin):
    # Поля, отображаемые в списке платформ
    list_display = ("id", "name")
    # Поиск по названию платформы
    search_fields = ("name",)


# Регистрация writeup (разборов задач)
@admin.register(Writeup)
class WriteupAdmin(admin.ModelAdmin):
    # Поля, отображаемые в списке writeup
    list_display = (
        "id",
        "title",
        "platform",
        "difficulty",
    )
    # Фильтры справа
    list_filter = (
        "platform",
        "difficulty",
    )
    # Поля для поиска
    search_fields = (
        "title",
        "description",
    )
