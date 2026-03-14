from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("secure-admin-portal/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("attack_lab/", include("attack_lab.urls")),
    path("ctf/", include("ctf_writeups.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("categories/", include("knowledge_base.urls")),
    path("roadmap/", include("roadmap.urls")),
    path("security_tools/", include("security_tools.urls")),
    path("", include("main.urls")),
]
# если запрос начинается с /media/ — брать файл из папки MEDIA_ROOT
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
