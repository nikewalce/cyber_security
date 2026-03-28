# import pytest
# # Функция, которая используется для преобразования URL-адресов в представления (views)
# # и обратно в пути. Она позволяет программно анализировать все зарегистрированные пути,
# # reverse-функции и структуру URL-конфигурации проекта
# from django.urls import get_resolver
#
# from django.urls import URLPattern, URLResolver
#
#
# def get_all_urls(resolver, prefix=""):
#     urls = []
#
#     for pattern in resolver.url_patterns:
#         if isinstance(pattern, URLPattern):
#             urls.append(prefix + str(pattern.pattern))
#
#         elif isinstance(pattern, URLResolver):
#             urls.extend(
#                 get_all_urls(pattern, prefix + str(pattern.pattern))
#             )
#
#     return urls
#
# @pytest.fixture
# def all_urls():
#     """Фикстура, которая возвращает список всех URL приложения"""
#     resolver = get_resolver()
#     return get_all_urls(resolver)
#
# @pytest.fixture
# def urls_main():
#     """Фикстура, которая возвращает список всех URL приложения"""
#     return collect_urls(get_resolver(), "main")
