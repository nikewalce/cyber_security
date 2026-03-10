# Импорт админ панели Django
from django.contrib import admin

# Импорт модели News
from .models import News


# Регистрация модели новостей
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    # Поля, отображаемые в списке новостей
    list_display = (
        "id",
        "title",
        "created_at",
    )
    # Поиск по заголовку и тексту
    search_fields = (
        "title",
        "content",
    )
    # Сортировка по дате (новые сверху)
    ordering = ("-created_at",)
