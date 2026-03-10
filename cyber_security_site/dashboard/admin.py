# Импорт админ панели Django
from django.contrib import admin

# Импорт модели прогресса пользователя
from .models import UserProgress


# Регистрация модели прогресса пользователя
@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    # Поля, отображаемые в списке
    list_display = (
        "id",
        "user",
        "completed_labs",
        "completed_articles",
    )
    # Поиск по имени пользователя
    search_fields = ("user__username",)
