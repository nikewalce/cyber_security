import pytest

@pytest.mark.django_db
@pytest.mark.app_name(
    "accounts"
)  # кастомный маркер: указываем, какое приложение тестируем
def test_urls(response, url): # client - встроенная фикстура Django
    """
    Тест проверяет, что все URL приложения:
    - доступны через GET
    - не падают с ошибкой сервера

    Параметр `url` подставляется динамически через pytest_generate_tests
    """
    # 200 — страница успешно открылась
    # 302 — редирект (например, на логин)
    assert response.status_code in (200, 302), f"Ошибка в URL: {url}"
