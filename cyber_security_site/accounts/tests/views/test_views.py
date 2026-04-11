import pytest
from bs4 import BeautifulSoup

# Это функция Django, которая позволяет получить URL-адрес по имени представления (view)
# или URL-шаблона. Это обеспечивает гибкость, позволяя менять структуру путей в urls.py
# без необходимости обновлять все ссылки в коде и шаблонах
# from django.urls import reverse


@pytest.mark.app_name(
    "accounts"
)  # кастомный маркер: указываем, какое приложение тестируем
def test_content_type(response):
    """
    Проверяем, что сервер отдает HTML
    """
    assert response.headers["Content-Type"].startswith(
        "text/html"
    ), f"Неверный Content-Type: {response.headers['Content-Type']}"


@pytest.mark.app_name(
    "accounts"
)  # кастомный маркер: указываем, какое приложение тестируем
def test_accounts_title(response):
    """
    Проверяем наличие заголовка страницы
    """
    soup = BeautifulSoup(response.content, "html.parser")

    h1_tags = soup.find_all("h1")

    assert any(h1.text.strip() == "Список аккаунтов" for h1 in h1_tags)


@pytest.mark.app_name(
    "accounts"
)  # кастомный маркер: указываем, какое приложение тестируем
def test_context_has_request(context):
    """
    Django всегда передает request через context processor
    """
    assert "request" in context


@pytest.mark.app_name(
    "accounts"
)  # кастомный маркер: указываем, какое приложение тестируем
def test_user_anonymous(context):
    """
    По умолчанию пользователь не авторизован
    """
    assert context["user"].is_anonymous


@pytest.mark.app_name(
    "accounts"
)  # кастомный маркер: указываем, какое приложение тестируем
def test_csrf_in_context(context):
    """
    Проверяем наличие CSRF токена в контексте
    """
    assert "csrf_token" in context


@pytest.mark.app_name(
    "accounts"
)  # кастомный маркер: указываем, какое приложение тестируем
def test_csrf_in_html(response):
    """
    Проверяем, что CSRF реально вставлен в форму
    """
    html = response.content.decode()
    assert "csrfmiddlewaretoken" in html


@pytest.mark.app_name(
    "accounts"
)  # кастомный маркер: указываем, какое приложение тестируем
def test_template_used(response):
    """
    Проверяем, что используется правильный шаблон
    """
    template_names = [t.name for t in response.templates]

    assert "accounts/accounts_view.html" in template_names


@pytest.mark.app_name(
    "accounts"
)  # кастомный маркер: указываем, какое приложение тестируем
def test_no_reflected_xss(client):
    """
    Проверка на отражённую XSS
    """
    payload = "<script>alert(1)</script>"

    response = client.get(f"/accounts/?q={payload}")
    html = response.content.decode()

    # Проверяем, что payload не исполняется
    assert payload not in html

    # Проверяем, что он экранирован
    assert "&lt;script&gt;" in html or "alert" not in html


@pytest.mark.app_name(
    "accounts"
)  # кастомный маркер: указываем, какое приложение тестируем
def test_csrf_cookie(client, url):
    """
    Проверяем, что CSRF cookie установлена
    """
    client.get(url)

    assert "csrftoken" in client.cookies


@pytest.mark.app_name(
    "accounts"
)  # кастомный маркер: указываем, какое приложение тестируем
def test_not_json(response):
    """
    Проверяем, что это НЕ API endpoint
    """
    assert "application/json" not in response.headers["Content-Type"]

    with pytest.raises(ValueError):
        response.json()
