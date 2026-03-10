# Импорт админ панели Django
from django.contrib import admin

# Импорт моделей Roadmap и RoadmapStep
from .models import Roadmap, RoadmapStep


# Inline отображение шагов roadmap
class RoadmapStepInline(admin.TabularInline):
    # Модель шагов
    model = RoadmapStep
    # Количество пустых форм для добавления
    extra = 1
    # Сортировка шагов
    ordering = ("order",)


# Регистрация Roadmap
@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    # Поля в списке roadmap
    list_display = (
        "id",
        "title",
    )
    # Встроенные шаги roadmap
    inlines = [RoadmapStepInline]


# Регистрация шагов roadmap
@admin.register(RoadmapStep)
class RoadmapStepAdmin(admin.ModelAdmin):
    # Поля в списке
    list_display = (
        "id",
        "roadmap",
        "title",
        "order",
    )
    # Сортировка шагов
    ordering = ("order",)
