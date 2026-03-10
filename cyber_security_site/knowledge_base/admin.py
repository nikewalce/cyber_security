# Импорт админ панели Django
from django.contrib import admin

# Импорт моделей Article и Category из текущего приложения
from .models import Article, Category


# Регистрируем модель Category в админ панели
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Поля, которые будут отображаться в списке категорий
    list_display = (
        "id",
        "name",
        "slug",
    )
    # Автоматически заполняет поле slug на основе name
    # Например: "Web Security" → "web-security"
    prepopulated_fields = {"slug": ("name",)}


# Регистрируем модель Article в админ панели
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # Поля, отображаемые в списке статей
    list_display = (
        "id",
        "title",
        "category",
        "created_at",
    )
    # Фильтры справа в админ панели
    list_filter = (
        "category",
        "created_at",
    )
    # Поля, по которым работает поиск
    search_fields = (
        "title",
        "content",
    )
    # Автоматическое создание slug из title
    prepopulated_fields = {"slug": ("title",)}
