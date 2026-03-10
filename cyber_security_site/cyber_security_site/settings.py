# Path — удобный класс для работы с файловыми путями
# os используется для работы с переменными окружения
import os
from pathlib import Path

# load_dotenv загружает переменные из файла .env
from dotenv import load_dotenv

# load_dotenv загружает переменные из файла .env
load_dotenv()
# BASE_DIR — путь к корневой папке проекта.
# __file__ — путь к текущему файлу settings.py
# resolve() — получает абсолютный путь
# parent.parent — поднимается на два уровня вверх
# В итоге BASE_DIR указывает на папку проекта (где manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")
# DEBUG — режим разработки.
# Если True:
# - показываются подробные ошибки
# - включаются дополнительные инструменты для разработки
# Если False:
# - ошибки скрываются (для безопасности в production)
# os.getenv("DEBUG") берет значение из переменной окружения (.env)
DEBUG = os.getenv("DEBUG")
# ALLOWED_HOSTS — список доменов, с которых разрешено открывать сайт.
# Это защита от Host Header Attack.
# В разработке обычно оставляют пустым или добавляют localhost.
# пример production:
# ["example.com", "www.example.com"]
ALLOWED_HOSTS = []


# INSTALLED_APPS — список приложений, подключенных к проекту.
# Django загружает их при запуске и регистрирует модели, админку и т.д.
INSTALLED_APPS = [
    # улучшенная и красивая админка
    "jazzmin",
    # Стандартная админ-панель Django
    "django.contrib.admin",
    # Система пользователей (регистрация, логин, права доступа)
    "django.contrib.auth",
    # Система типов контента (используется для универсальных связей моделей)
    "django.contrib.contenttypes",
    # Сессии пользователей (хранение авторизации)
    "django.contrib.sessions",
    # Система сообщений (flash messages)
    "django.contrib.messages",
    # Работа со статическими файлами (css, js, изображения)
    "django.contrib.staticfiles",
    # Пользовательские приложения проекта
    # приложение для регистрации и авторизации
    "accounts",
    # панель управления (dashboard)
    "dashboard",
    # база знаний по кибербезопасности
    "knowledge_base",
    # инструменты безопасности
    "security_tools",
    # лаборатория атак
    "attack_lab",
    # анализ логов
    "logs_analysis",
    # writeups CTF
    "ctf_writeups",
    # roadmap по обучению
    "roadmap",
    "main",
]
# настройки темы админки Jazzmin
JAZZMIN_SETTINGS = {
    # заголовок страницы
    "site_title": "Cyber Security Admin",
    # название в верхней панели
    "site_header": "Cyber Security Platform",
    # название бренда
    "site_brand": "CyberSecurity",
    # приветственное сообщение
    "welcome_sign": "Welcome to Cyber Security Admin",
    # копирайт
    "copyright": "CyberSecurity",
    # показывать боковую панель
    "show_sidebar": True,
    # раскрывать меню навигации
    "navigation_expanded": True,
}
# MIDDLEWARE — список промежуточных обработчиков запроса.
# Они обрабатывают запрос ДО и ПОСЛЕ view.
MIDDLEWARE = [
    # добавляет базовые настройки безопасности
    "django.middleware.security.SecurityMiddleware",
    # управление сессиями пользователей
    "django.contrib.sessions.middleware.SessionMiddleware",
    # различные улучшения обработки HTTP
    "django.middleware.common.CommonMiddleware",
    # защита от CSRF атак (подделка запросов)
    "django.middleware.csrf.CsrfViewMiddleware",
    # добавляет информацию о текущем пользователе в request.user
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # система сообщений (success, error и т.д.)
    "django.contrib.messages.middleware.MessageMiddleware",
    # защита от Clickjacking атак
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ROOT_URLCONF — основной файл маршрутизации URL.
# Django будет искать URL-пути в файле urls.py
ROOT_URLCONF = "cyber_security_site.urls"

TEMPLATES = [
    {
        # Backend для работы с шаблонами Django
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # папки, где искать шаблоны
        # если пусто — Django ищет templates внутри каждого приложения
        'DIRS': [BASE_DIR / 'templates'],  # <-- глобальные шаблоны
        # разрешает автоматически искать папку templates в приложениях
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                # добавляет request в шаблоны
                "django.template.context_processors.request",
                # добавляет информацию о пользователе
                "django.contrib.auth.context_processors.auth",
                # добавляет систему сообщений
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
# WSGI_APPLICATION — точка входа для web-сервера.
# Используется сервером (gunicorn, uwsgi) для запуска Django приложения
WSGI_APPLICATION = "cyber_security_site.wsgi.application"
# DATABASES — настройки базы данных проекта
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),  # имя базы
        "USER": os.getenv("DB_USER"),  # пользователь
        "PASSWORD": os.getenv("DB_PASSWORD"),  # пароль
        "HOST": os.getenv("DB_HOST"),  # хост
        "PORT": os.getenv("DB_PORT"),  # порт
    }
}
# Password validation
# Валидаторы паролей пользователей
# Django автоматически проверяет пароль при регистрации
AUTH_PASSWORD_VALIDATORS = [
    {
        # проверяет, чтобы пароль не был похож на имя пользователя
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        # минимальная длина пароля
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        # запрещает слишком простые пароли (password123 и т.д.)
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        # запрещает пароль состоящий только из цифр
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
# язык сайта по умолчанию
LANGUAGE_CODE = "en-us"
# часовой пояс
TIME_ZONE = "UTC"
# включает систему переводов Django
USE_I18N = True
# включает работу с часовыми поясами
USE_TZ = True
# Static files
# URL для статических файлов (CSS, JS, изображения)
# пример: example.com/static/style.css
STATIC_URL = "static/"
# использовать кастомную модель пользователя
AUTH_USER_MODEL = "accounts.User"
