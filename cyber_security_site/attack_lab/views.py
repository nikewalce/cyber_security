# Импорт функции render для рендеринга HTML шаблонов
from django.shortcuts import render

# Импорт для выполнения raw SQL запросов
from django.db import connection

# Хранилище файлов Django
from django.core.files.storage import FileSystemStorage

# Модель пользователей Django
from django.contrib.auth.models import User

# Настройки Django проекта
from django.conf import settings

# Библиотека для HTTP запросов (используется в SSRF лаборатории)
import requests

# Работа с системой (для command injection)
import os

# Работа с JWT токенами
import jwt

# -------------------------------
# Главная страница Attack Lab
# -------------------------------

def attack_lab_view(request):
    """
    Главная страница полигона уязвимостей.
    Отсюда пользователь может перейти в любую лабораторию.
    """
    return render(request, "attack_lab/attack_lab_view.html")


# -------------------------------
# XSS Lab
# -------------------------------

def xss_lab(request):
    """
    Reflected XSS лаборатория.

    Payload для теста:
    <script>alert(1)</script>
    """

    # Получаем значение параметра q из URL
    query = request.GET.get("q", "")

    # Режим лаборатории
    # vulnerable — уязвимый
    # secure — защищённый
    mode = request.GET.get("mode", "vulnerable")

    context = {
        "query": query,
        "mode": mode
    }

    return render(request, "attack_lab/xss_lab.html", context)


# -------------------------------
# SQL Injection Lab
# -------------------------------

def sqli_lab(request):
    """
    SQL Injection лаборатория.

    Пример атаки:
    ' OR 1=1 --
    """

    result = None

    mode = request.GET.get("mode", "vulnerable")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        if mode == "vulnerable":

            # УЯЗВИМЫЙ КОД
            # Используется строковая интерполяция
            # что позволяет внедрить SQL код

            query = f"""
                SELECT * FROM auth_user
                WHERE username = '{username}'
                AND password = '{password}'
            """

            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()

        else:

            # БЕЗОПАСНЫЙ КОД
            # Используются параметризованные запросы

            query = """
                SELECT * FROM auth_user
                WHERE username=%s AND password=%s
            """

            with connection.cursor() as cursor:
                cursor.execute(query, [username, password])
                result = cursor.fetchall()

    return render(request, "attack_lab/sqli_lab.html", {
        "result": result,
        "mode": mode
    })


# -------------------------------
# CSRF Lab
# -------------------------------

def csrf_lab(request):
    """
    CSRF лаборатория.

    Демонстрирует роль CSRF токена.
    """

    message = None

    mode = request.GET.get("mode", "vulnerable")

    if request.method == "POST":

        amount = request.POST.get("amount")

        if mode == "vulnerable":

            # УЯЗВИМАЯ версия
            # CSRF токен не проверяется
            message = f"Transferred {amount}$"

        else:

            # БЕЗОПАСНАЯ версия
            # Django автоматически проверяет CSRF токен
            message = f"Secure transfer of {amount}$"

    return render(request, "attack_lab/csrf_lab.html", {
        "message": message,
        "mode": mode
    })


# -------------------------------
# File Upload Lab
# -------------------------------

def upload_lab(request):
    """
    Лаборатория загрузки файлов.

    Payload для теста:
    shell.php
    """

    file_url = None

    mode = request.GET.get("mode", "vulnerable")

    if request.method == "POST":

        uploaded_file = request.FILES["file"]

        if mode == "vulnerable":

            # УЯЗВИМЫЙ КОД
            # Любой файл может быть загружен

            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)

            file_url = fs.url(filename)

        else:

            # БЕЗОПАСНЫЙ КОД
            # Проверка расширения файла

            allowed = ["jpg", "png", "pdf"]

            ext = uploaded_file.name.split(".")[-1].lower()

            if ext not in allowed:
                file_url = "File type not allowed"
            else:
                fs = FileSystemStorage()
                filename = fs.save(uploaded_file.name, uploaded_file)
                file_url = fs.url(filename)

    return render(request, "attack_lab/upload_lab.html", {
        "file_url": file_url,
        "mode": mode
    })


# -------------------------------
# IDOR Lab
# -------------------------------

def idor_lab(request):
    """
    IDOR лаборатория (Insecure Direct Object Reference).

    Пример:
    user_id=1
    user_id=2
    user_id=3
    """

    user = None

    mode = request.GET.get("mode", "vulnerable")

    user_id = request.GET.get("user_id")

    if user_id:

        if mode == "vulnerable":

            # УЯЗВИМЫЙ КОД
            # Любой пользователь может просмотреть любой профиль

            user = User.objects.filter(id=user_id).first()

        else:

            # БЕЗОПАСНЫЙ КОД
            # Доступ только к своему профилю

            if request.user.is_authenticated and str(request.user.id) == user_id:
                user = request.user

    return render(request, "attack_lab/idor_lab.html", {
        "user": user,
        "mode": mode
    })


# -------------------------------
# SSRF Lab
# -------------------------------

def ssrf_lab(request):
    """
    SSRF лаборатория.

    Примеры атак:
    http://127.0.0.1:8000/admin
    http://169.254.169.254
    """

    response = None

    mode = request.GET.get("mode", "vulnerable")

    if request.method == "POST":

        url = request.POST.get("url")

        try:

            if mode == "vulnerable":

                # УЯЗВИМЫЙ КОД
                # Сервер делает запрос к любому URL

                r = requests.get(url)
                response = r.text[:500]

            else:

                # БЕЗОПАСНЫЙ КОД
                # Разрешаем только внешние домены

                if "127.0.0.1" in url or "localhost" in url:
                    response = "Blocked by SSRF protection"
                else:
                    r = requests.get(url)
                    response = r.text[:500]

        except:
            response = "Request failed"

    return render(request, "attack_lab/ssrf_lab.html", {
        "response": response,
        "mode": mode
    })


# -------------------------------
# Command Injection Lab
# -------------------------------

def command_injection_lab(request):
    """
    Command Injection лаборатория.

    Payload:
    8.8.8.8; ls
    """

    output = None

    mode = request.GET.get("mode", "vulnerable")

    if request.method == "POST":

        host = request.POST.get("host")

        if mode == "vulnerable":

            # УЯЗВИМЫЙ КОД
            command = f"ping -c 1 {host}"
            output = os.popen(command).read()

        else:

            # БЕЗОПАСНЫЙ КОД
            import subprocess

            output = subprocess.run(
                ["ping", "-c", "1", host],
                capture_output=True,
                text=True
            ).stdout

    return render(request, "attack_lab/command_lab.html", {
        "output": output,
        "mode": mode
    })


# -------------------------------
# Path Traversal Lab
# -------------------------------

def path_traversal_lab(request):
    """
    Path Traversal лаборатория.

    Payload:
    ../../settings.py
    """

    content = None

    mode = request.GET.get("mode", "vulnerable")

    filename = request.GET.get("file")

    if filename:

        if mode == "vulnerable":

            # УЯЗВИМЫЙ КОД
            filepath = os.path.join(settings.BASE_DIR, "files", filename)

        else:

            # БЕЗОПАСНЫЙ КОД
            base = os.path.join(settings.BASE_DIR, "files")
            filepath = os.path.normpath(os.path.join(base, filename))

            if not filepath.startswith(base):
                content = "Access denied"

        try:
            with open(filepath) as f:
                content = f.read()
        except:
            if not content:
                content = "File not found"

    return render(request, "attack_lab/path_traversal_lab.html", {
        "content": content,
        "mode": mode
    })


# -------------------------------
# JWT Lab
# -------------------------------

SECRET = "secret123"

def jwt_lab(request):
    """
    JWT лаборатория.
    """

    decoded = None
    token = None

    mode = request.GET.get("mode", "vulnerable")

    if request.method == "POST":

        username = request.POST.get("username")

        token = jwt.encode({"user": username}, SECRET, algorithm="HS256")

        if mode == "vulnerable":

            # УЯЗВИМАЯ версия
            decoded = jwt.decode(token, SECRET, algorithms=["HS256"])

        else:

            # БЕЗОПАСНАЯ версия
            decoded = jwt.decode(
                token,
                SECRET,
                algorithms=["HS256"],
                options={"require": ["exp"]}
            )

    return render(request, "attack_lab/jwt_lab.html", {
        "token": token,
        "decoded": decoded,
        "mode": mode
    })


# -------------------------------
# Broken Authentication Lab
# -------------------------------

def broken_auth_lab(request):
    """
    Broken Authentication лаборатория.
    """

    message = None

    mode = request.GET.get("mode", "vulnerable")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        if mode == "vulnerable":

            # УЯЗВИМАЯ версия
            if username == "admin" and password == "admin":
                message = "Admin access granted"

        else:

            # БЕЗОПАСНАЯ версия
            from django.contrib.auth import authenticate

            user = authenticate(username=username, password=password)

            if user:
                message = "Secure login success"
            else:
                message = "Login failed"

    return render(request, "attack_lab/broken_auth_lab.html", {
        "message": message,
        "mode": mode
    })