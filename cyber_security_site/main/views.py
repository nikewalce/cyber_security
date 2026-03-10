from django.shortcuts import get_object_or_404, render

from .models import News

def home(request):
    """
    Главная страница сайта.
    Просто перенаправляем на новости или показываем последние 5 новостей.
    """
    latest_news = News.objects.all().order_by('-created_at')[:5]  # последние 5 новостей
    return render(request, 'main/home.html', {
        'latest_news': latest_news,
    })

# Функциональное представление для вывода новостей
def cybersecurity_news(request, news_slug=None):
    """
    Если передан news_slug, отображает конкретную новость.
    Иначе выводит список всех новостей.
    """
    # Получаем все новости из базы
    news = News.objects.all().order_by(
        "-created_at"
    )  # сортируем по дате создания, новые сверху

    item = None  # по умолчанию конкретной новости нет

    if news_slug:
        # Получаем объект новости по slug или возвращаем 404, если не найден
        item = get_object_or_404(News, slug=news_slug)

    # Передаём данные в шаблон
    return render(
        request,
        "main/news.html",
        {
            "item": item,  # конкретная новость (None если не выбран)
            "news": news,  # список всех новостей
        },
    )
