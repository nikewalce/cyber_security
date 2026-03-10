from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("secure-admin-portal/", admin.site.urls),
    path("", include("main.urls")),
]
