import pytest

# Это функция Django, которая позволяет получить URL-адрес по имени представления (view)
# или URL-шаблона. Это обеспечивает гибкость, позволяя менять структуру путей в urls.py
# без необходимости обновлять все ссылки в коде и шаблонах
# from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.app_name(
    "security_tools"
)  # кастомный маркер: указываем, какое приложение тестируем
def test_urls(client, url):
    """
    Тест проверяет, что все URL приложения:
    - доступны через GET
    - не падают с ошибкой сервера

    Параметр `url` подставляется динамически через pytest_generate_tests
    """
    print(url)
    response = client.get(url)

    # 200 — страница успешно открылась
    # 302 — редирект (например, на логин)
    assert response.status_code in (200, 302), f"Ошибка в URL: {url}"
