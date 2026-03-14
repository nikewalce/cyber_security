from django.urls import path
from . import views

urlpatterns = [

    # список roadmap
    path("", views.roadmap_view, name="roadmap"),

    # конкретный roadmap
    path(
        "<slug:roadmap_slug>/",
        views.roadmap_step_view,
        name="roadmap_steps"
    ),
    # конкретный шаг
    path(
        "<slug:roadmap_slug>/<slug:step_slug>/",
        views.roadmap_step_detail,
        name="roadmap_step_detail"
    ),
]
