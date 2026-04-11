import pytest
from django.urls import URLPattern, URLResolver, get_resolver


def pytest_generate_tests(metafunc):
    """
    Хук pytest, который динамически генерирует параметры для тестов.

    Вызывается ДО запуска тестов и позволяет:
    - автоматически подставлять данные в тесты
    - заменяет @pytest.mark.parametrize(...)
    """

    # Проверяем, есть ли аргумент 'url' в тесте
    # (иначе не нужно ничего генерировать)
    if "url" in metafunc.fixturenames:

        # Получаем кастомный маркер @pytest.mark.app_name("main")
        marker = metafunc.definition.get_closest_marker("app_name")

        # Если маркер есть → берём имя приложения
        # Если нет → тестируем ВСЕ URL проекта
        app_name = marker.args[0] if marker else None

        # Получаем все URL (или только нужного приложения)
        urls = collect_urls(get_resolver(), app_name)

        # Фильтруем URL, которые можно тестировать
        testable_urls = [
            "/" + url.lstrip("/")  # нормализуем URL (чтобы всегда был / в начале)
            for url in urls
            if is_testable_url(url)
        ]

        # Динамически создаём тесты:
        # test_urls[/news/]
        # test_urls[/categories/]
        metafunc.parametrize(
            "url",
            testable_urls,
            ids=testable_urls,  # 👈 красиво отображает URL в pytest выводе
        )


def collect_urls(resolver, app_name=None, prefix=""):
    """
    Рекурсивно собирает все URL проекта.

    :param resolver: объект URLResolver (обычно get_resolver())
    :param app_name: имя приложения (например "main", "attack_lab")
                     если None → собрать ВСЕ URL
    :param prefix: используется для сборки полного пути (для include)
    :return: список строк URL
    """
    urls = []

    for pattern in resolver.url_patterns:

        # --- Обычный URL (path / re_path) ---
        if isinstance(pattern, URLPattern):

            view = pattern.callback  # функция или class-based view
            module = view.__module__  # например: "main.views"

            # Фильтр по приложению:
            # проверяем, что view принадлежит нужному приложению
            if app_name is None or app_name in module:
                urls.append(prefix + str(pattern.pattern))

        # --- include() → вложенные URL ---
        elif isinstance(pattern, URLResolver):

            # Рекурсивно обходим вложенные маршруты
            urls.extend(
                collect_urls(
                    pattern, app_name=app_name, prefix=prefix + str(pattern.pattern)
                )
            )

    return urls


def is_testable_url(url: str) -> bool:
    """
    Фильтр URL, которые можно тестировать через GET.

    Исключаем:
    - динамические URL (<slug>, <id>) → без данных не откроются
    - админку → требует авторизацию
    - служебные URL (delete/change/history)
    """

    return (
        "<" not in url  # динамические параметры
        and "admin" not in url  # админка
        and not url.endswith("delete/")
        and not url.endswith("change/")
        and not url.endswith("history/")
    )


# --- (опционально) универсальные фикстуры ---


@pytest.fixture
def urls_all():
    """
    Возвращает все URL проекта (без фильтрации по приложению)
    """
    return collect_urls(get_resolver())


@pytest.fixture
def urls_by_app():
    """
    Фабрика фикстур → позволяет получать URL любого приложения

    Использование:
        urls = urls_by_app("main")
    """

    def _get_urls(app_name: str):
        return collect_urls(get_resolver(), app_name)

    return _get_urls

@pytest.fixture
def response(client, url): # client - встроенная фикстура Django
    return client.get(url)

@pytest.fixture
def context(response):
    return response.context[-1] if response.context else {}