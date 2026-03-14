from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_security_tools, name="list_security_tools"),
]