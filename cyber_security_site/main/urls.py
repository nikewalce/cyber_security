from django.urls import path

from . import views  # Импортируем views из текущего приложения (main)

# Список маршрутов (URL patterns) для приложения main
urlpatterns = [
    path("", views.home, name="home"),  # главная страница
    # URL для отображения всех новостей
    # /news/ → вызовет функцию cybersecurity_news без аргумента news_slug
    path("news/", views.cybersecurity_news, name="cybersecurity_news"),
    # URL для отображения конкретной новости по её slug
    # Пример: /news/my-first-news/ → передаст "my-first-news" в аргумент news_slug
    path(
        "news/<slug:news_slug>/",
        views.cybersecurity_news,
        name="cybersecurity_news_detail",
    ),
]
