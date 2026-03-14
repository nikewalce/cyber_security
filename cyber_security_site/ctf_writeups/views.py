from django.shortcuts import render, get_object_or_404
from .models import CTFPlatform


# Страница со списком всех CTF платформ
def ctf_platforms(request):
    # получаем все платформы из базы
    # Django делает SQL запрос: SELECT * FROM ctfplatform;
    platforms = CTFPlatform.objects.all()
    # Берём HTML шаблон, вставляем туда данные, отправляем пользователю
    return render(
        request,
        "ctf_writeups/ctf_platforms.html",
        {"platforms": platforms}
    )


# Страница с заданиями конкретной платформы
# platform_slug приходит из URL:
# /ctf/hackthebox/
# platform_slug = "hackthebox"
def ctf_writeups(request, platform_slug):
    # получаем платформу по slug
    # Django делает запрос: SELECT * FROM ctfplatform WHERE slug = "hackthebox";
    # Если не найдено → возвращает 404 страницу
    platform = get_object_or_404(CTFPlatform, slug=platform_slug)
    # получаем все writeups этой платформы. Это благодаря related_name
    # SELECT * FROM writeup
    # WHERE platform_id = platform.id;
    writeups = platform.writeups.all()
    return render(
        request,
        "ctf_writeups/ctf_writeups.html",
        {
            "platform": platform,
            "writeups": writeups
        }
    )