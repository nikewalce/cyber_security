from django.urls import path

from . import views

# если в path указаны "" без значения, то вызывается путь из главного urls (attack_lab/)
# если указано какое-то значение, то вызывается путь из главного urls (attack_lab/) + то,
# что написано в "test" (если в path указаны "" без значения,
# то вызывается путь из главного urls (accounts/test))
urlpatterns = [path("", views.attack_lab_view, name="attack_labs")]
