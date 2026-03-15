from django.urls import path

from . import views

urlpatterns = [
    # список платформ
    path(
        "", views.ctf_platforms, name="ctf_platforms"  # вызвать функцию ctf_platforms()
    ),
    # задания конкретной платформы
    path(
        "<slug:platform_slug>/",  # любая строка → передать в view
        views.ctf_writeups,
        name="ctf_writeups",
    ),
]
