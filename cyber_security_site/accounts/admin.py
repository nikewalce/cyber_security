from django.contrib import admin

# стандартная админка пользователей Django
from django.contrib.auth.admin import UserAdmin

# используется для безопасного вывода HTML
from django.utils.html import format_html

from .models import User


# регистрируем модель пользователя в админке
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # поля, которые отображаются в списке пользователей
    list_display = (
        "id",
        "avatar_preview",
        "username",
        "email",
        "skill_level",
        "is_staff",
        "date_joined",
    )
    # поля, которые можно изменить
    list_editable = ("skill_level",)
    # поля для поиска
    search_fields = (
        "username",
        "email",
        "github",
    )
    # фильтры справа в админке
    list_filter = (
        "skill_level",
        "is_staff",
        "is_active",
    )
    # сортировка по дате регистрации
    ordering = ("-date_joined",)
    # поле только для чтения
    readonly_fields = ("date_joined",)
    # добавляем дополнительные поля в форму пользователя
    fieldsets = UserAdmin.fieldsets + (
        (
            "Cyber Security Profile",
            {
                "fields": (
                    "bio",
                    "avatar",
                    "github",
                    "skill_level",
                )
            },
        ),
    )

    # отображение миниатюры аватара
    def avatar_preview(self, obj):
        # если аватар есть — показать изображение
        if obj.avatar:
            return format_html(
                '<img src="{}" width="50" height="50" />', obj.avatar.url
            )
        # если аватара нет
        return "-"
