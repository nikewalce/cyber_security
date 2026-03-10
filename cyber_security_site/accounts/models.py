from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# кастомная модель пользователя
# наследуемся от стандартного AbstractUser
# чтобы расширить функциональность
class User(AbstractUser):
    # описание пользователя
    bio = models.TextField(blank=True)
    # аватар пользователя
    # upload_to задаёт путь сохранения файла
    avatar = models.ImageField(upload_to="avatars/%Y/%m/%d", blank=True)
    # ссылка на github профиль
    github = models.URLField(blank=True)
    # уровень навыков пользователя
    skill_level = models.CharField(max_length=50, default="beginner")
    # дата регистрации
    date_joined = models.DateTimeField(default=timezone.now)

    # строковое представление объекта
    def __str__(self):
        return self.username
