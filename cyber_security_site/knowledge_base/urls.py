from django.urls import path
from . import views

urlpatterns = [

    # список категорий
    path("", views.category_list, name="category_list"),

    # статьи категории
    path(
        "<slug:category_slug>/",
        views.articles_by_category,
        name="articles_by_category"
    ),

    # статья
    path(
        "articles/<slug:article_slug>/",
        views.article_detail,
        name="article_detail"
    ),
]