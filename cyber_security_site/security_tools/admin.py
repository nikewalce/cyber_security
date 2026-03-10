# Импорт админ панели Django
from django.contrib import admin

# Импорт модели SecurityTool
from .models import SecurityTool


# Регистрация модели инструментов безопасности
@admin.register(SecurityTool)
class SecurityToolAdmin(admin.ModelAdmin):
    # Поля, отображаемые в списке инструментов
    list_display = (
        "id",
        "name",
        "difficulty",
    )
    # Поиск по названию и описанию
    search_fields = (
        "name",
        "description",
    )
    # Фильтр по сложности
    list_filter = ("difficulty",)
    # Автоматическое создание slug из name
    prepopulated_fields = {"slug": ("name",)}
