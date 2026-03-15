from django.urls import path

from . import views

# если в path указаны "" без значения, то вызывается путь из главного urls (accounts/)
# если указано какое-то значение, то вызывается путь из главного urls (accounts/) + то,
# что написано в "test" (если в path указаны "" без значения,
# то вызывается путь из главного urls (accounts/test))
urlpatterns = [
    path("", views.accounts_view, name="accounts_view"),
]
