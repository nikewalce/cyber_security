from django.urls import path

from . import views

# если в path указаны "" без значения, то вызывается путь из главного urls (attack_lab/)
# если указано какое-то значение, то вызывается путь из главного urls (attack_lab/) + то,
# что написано в "test" (если в path указаны "" без значения,
# то вызывается путь из главного urls (accounts/test))
urlpatterns = [path("", views.attack_lab_view, name="attack_labs")]

urlpatterns = [
    path("", views.attack_lab_view, name="attack_lab_view"),

    path("xss/", views.xss_lab, name="xss_lab"),
    path("sqli/", views.sqli_lab, name="sqli_lab"),
    path("csrf/", views.csrf_lab, name="csrf_lab"),
    path("upload/", views.upload_lab, name="upload_lab"),
    path("idor/", views.idor_lab, name="idor_lab"),

    path("ssrf/", views.ssrf_lab, name="ssrf_lab"),
    path("command/", views.command_injection_lab, name="command_lab"),
    path("path-traversal/", views.path_traversal_lab, name="path_traversal_lab"),
    path("jwt/", views.jwt_lab, name="jwt_lab"),
    path("auth/", views.broken_auth_lab, name="broken_auth_lab"),
]
