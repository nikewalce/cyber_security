# Импорт админ панели Django
from django.contrib import admin

# Импорт моделей
from .models import LogEvent, LogFile


# Inline отображение событий внутри LogFile
# Это позволяет редактировать события прямо в файле логов
class LogEventInline(admin.TabularInline):
    # Модель, которая будет отображаться
    model = LogEvent
    # Количество пустых форм для добавления
    extra = 0


# Регистрация модели LogFile
@admin.register(LogFile)
class LogFileAdmin(admin.ModelAdmin):
    # Поля, отображаемые в списке файлов логов
    list_display = (
        "id",
        "name",
    )
    # Встраиваем события внутрь файла логов
    inlines = [LogEventInline]


# Регистрация модели LogEvent
@admin.register(LogEvent)
class LogEventAdmin(admin.ModelAdmin):
    # Поля, отображаемые в списке событий
    list_display = (
        "id",
        "log",
        "timestamp",
        "event_type",
    )
    # Фильтр по типу события
    list_filter = ("event_type",)
    # Поиск по тексту сообщения
    search_fields = ("message",)
