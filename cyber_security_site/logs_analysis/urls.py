from django.urls import path

from . import views

urlpatterns = [
    path("", views.logs_analysis_view, name="logs_analysis"),
]
