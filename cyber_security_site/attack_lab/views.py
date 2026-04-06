# Импорт функции render для рендеринга HTML шаблонов
# Работа с системой (для command injection)
import os

# Работа с JWT токенами
import jwt

# Библиотека для HTTP запросов (используется в SSRF лаборатории)
import requests

# Настройки Django проекта
from django.conf import settings

# Модель пользователей Django
from django.contrib.auth.models import User

# Хранилище файлов Django
from django.core.files.storage import FileSystemStorage
from django.db import connection
from django.shortcuts import render

# Импорт форм
from .forms import CommentForm, XSSForm

# Импорт моделей
from .models import Comment

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


def xss_reflected(request):
    """
    Reflected XSS лаборатория.

    Reflected XSS = вредоносный payload приходит в запросе
    и сразу отражается в ответе сервера.

    Пример:
    /xss?q=<script>alert(1)</script>

    Браузер выполнит JS → XSS

    - vulnerable → без защиты (уязвимость)
    - secure → через Django Form (защита)
    """
    # 🔧 режим работы (по умолчанию уязвимый)
    mode = request.GET.get("mode", "vulnerable")

    # 🔒 включение CSP (дополнительная защита браузера)
    csp_mode = request.GET.get("csp", "off")

    # 📥 входные данные от пользователя (главный источник XSS)
    query = request.GET.get("q", "")

    form = None

    # 🛡️ SECURE режим
    if mode == "secure":
        # Используем Django Form как слой валидации
        form = XSSForm({"query": query})

        if form.is_valid():
            # cleaned_data → безопасные данные
            query = form.cleaned_data["query"]
    # 🛡️ SUPER SECURE (жесткое экранирование)
    elif mode == "super_secure":
        from django.utils.html import escape

        query = escape(query)
    # ❌ VULNERABLE режим
    else:
        # НИЧЕГО НЕ ДЕЛАЕМ → payload пройдет как есть
        pass

    # 📦 передаем данные в шаблон
    context = {"query": query, "mode": mode, "form": form, "csp": csp_mode}

    response = render(request, "attack_lab/xss_lab.html", context)

    # 🛡️ CSP защита (на уровне браузера)
    if csp_mode == "on":
        # default-src 'self' → ВСЕ ресурсы (картинки, стили, скрипты) можно грузить только с домена хоста
        # script-src 'self' → JS можно грузить только с сайта хоста
        # оставлять только вышеописанное опасно, т.к. <script>alert(1)</script> это inline script, а не внешний файл
        # CSP его иногда не блокирует (зависит от браузера и политики)
        # object-src 'none' Запрещает:<object>, <embed>,<applet> Это старые способы XSS (но все еще используются)
        # base-uri 'self' Запрещает подмену <base> Атака: <base href="https://evil.com/"> все ссылки станут вести на злоумышленника
        response["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'self'"
        )

    return response


def xss_stored(request):
    """
    📚 Stored XSS лаборатория

    Stored XSS = вредоносный код сохраняется в базе данных
    и выполняется каждый раз, когда страница загружается.

    Поток атаки:
    User → вводит payload → сохраняется в DB → другой пользователь открывает страницу → JS выполняется
    """

    # ⚙️ режим работы (берем из POST или GET)
    mode = request.POST.get("mode") or request.GET.get("mode", "vulnerable")

    if request.method == "POST":
        action = request.POST.get("action")

        # 🧹 Очистка базы (для удобства тестирования)
        if action == "clear":
            Comment.objects.all().delete()

        else:
            # 📥 пользовательский ввод (потенциальный XSS payload)
            text = request.POST.get("text", "")

            # ⚠️ Secure режим (через Django Form)
            if mode == "secure":
                form = CommentForm({"text": text})
                if form.is_valid():
                    text = form.cleaned_data["text"]

            # 🛡️ Super Secure режим (принудительное экранирование)
            elif mode == "super_secure":
                from django.utils.html import escape

                text = escape(text)

            # ❗ ВАЖНО:
            # В vulnerable режиме мы сохраняем payload как есть
            # Это демонстрирует Stored XSS
            Comment.objects.create(text=text)

    # 📤 получаем комментарии
    comments = Comment.objects.all().order_by("-id")

    return render(
        request, "attack_lab/xss_stored.html", {"comments": comments, "mode": mode}
    )


def xss_dom(request):
    """
    DOM-based XSS лаборатория (реалистичная).

    Здесь сервер НЕ участвует в атаке.
    Источник данных → location.hash
    Sink → innerHTML (опасно!)

    Пример:
    https://site.com/xss_dom#<script>alert(1)</script>

    Показано три режима:
    - vulnerable → innerHTML, XSS срабатывает
    - secure → innerText, безопасно
    - super_secure → экранируем < и >, супер-защита
    """
    return render(request, "attack_lab/xss_dom.html")


# -------------------------------
# SQL Injection Lab
# -------------------------------


def sqli_lab(request):
    """
    Лаборатория SQL Injection в Django с двумя режимами: уязвимым и защищённым
    В уязвимом режиме используется строковая интерполяция, что позволяет выполнять SQL-инъекции
    В защищённом — параметризованные запросы, которые предотвращают выполнение вредоносного SQL-кода
    """
    # result — переменная для хранения результата SQL-запроса
    # изначально None (если пользователь ещё ничего не отправлял)
    result = None

    # 🔹 Получаем текущую модель пользователя (тут используется кастомный пользователь accounts.User)
    from django.contrib.auth import get_user_model

    User = get_user_model()

    # 🔹 Получаем имя таблицы в базе данных
    # Например: "accounts_user"
    table_name = User._meta.db_table

    # 🔹 Проверяем, была ли отправлена форма
    if request.method == "POST":

        # 🔹 Получаем данные из формы
        # request.POST — словарь с данными формы
        username = request.POST.get("username")
        # password = request.POST.get("password")

        # 🔹 Получаем выбранный режим работы лаборатории
        # если не передан — по умолчанию "vulnerable"
        mode = request.POST.get("mode", "vulnerable")

        # =====================================================
        # ❌ УЯЗВИМЫЙ РЕЖИМ (VULNERABLE)
        # =====================================================
        if mode == "vulnerable":

            # ⚠️ ВАЖНО:
            # Здесь используется f-string → это ОПАСНО
            # пользовательский ввод напрямую вставляется в SQL
            # → это и есть SQL Injection

            query = f"""
                SELECT id, username, email
                FROM {table_name}
                WHERE username = '{username}'
            """

            # 🔹 Открываем курсор для работы с БД
            # cursor позволяет выполнять SQL-запросы
            with connection.cursor() as cursor:

                # 🔹 Выполняем SQL-запрос
                # если в username есть payload → он выполнится
                cursor.execute(query)

                # 🔹 Получаем ВСЕ строки результата
                # результат — список кортежей [(id, username, email), ...]
                result = cursor.fetchall()

        # =====================================================
        # 🛡️ ЗАЩИЩЕННЫЙ РЕЖИМ (SECURE)
        # =====================================================
        else:

            # ✅ Здесь используется параметризованный запрос
            # %s — это placeholder (заглушка)
            # значения передаются отдельно → SQL Injection НЕ работает

            query = f"""
                SELECT id, username, email
                FROM {table_name}
                WHERE username = %s
            """

            with connection.cursor() as cursor:

                # 🔹 Передаём параметры отдельно
                # Django экранирует их автоматически
                # → пользовательский ввод НЕ становится SQL-кодом
                cursor.execute(query, [username])

                # 🔹 Получаем результат
                result = cursor.fetchall()

    # =====================================================
    # 🔹 ЕСЛИ СТРАНИЦА ОТКРЫТА ВПЕРВЫЕ (GET запрос)
    # =====================================================
    else:
        # по умолчанию показываем уязвимый режим
        mode = "vulnerable"

    # =====================================================
    # 🔹 РЕНДЕР ШАБЛОНА
    # =====================================================

    # Передаём данные в HTML:
    # result — результат SQL запроса
    # mode — текущий режим (чтобы отобразить в UI)
    return render(request, "attack_lab/sqli_lab.html", {"result": result, "mode": mode})


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

    return render(
        request, "attack_lab/csrf_lab.html", {"message": message, "mode": mode}
    )


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

    return render(
        request, "attack_lab/upload_lab.html", {"file_url": file_url, "mode": mode}
    )


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

    return render(request, "attack_lab/idor_lab.html", {"user": user, "mode": mode})


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
        except requests.exceptions.ConnectionError:
            response = "Ошибка соединения: невозможно связаться с хостом"
        except requests.exceptions.Timeout:
            response = "Тайм-аут запроса: серверу потребовалось слишком много времени, чтобы ответить"
        except requests.exceptions.TooManyRedirects:
            response = "Слишком много перенаправлений"
        except requests.exceptions.InvalidURL:
            response = "Неверный формат URL"
        except requests.exceptions.RequestException as e:
            response = f"Запрос не выполнен: {str(e)}"

    return render(
        request, "attack_lab/ssrf_lab.html", {"response": response, "mode": mode}
    )


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
                ["ping", "-c", "1", host], capture_output=True, text=True
            ).stdout

    return render(
        request, "attack_lab/command_lab.html", {"output": output, "mode": mode}
    )


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
        except PermissionError:
            content = "Доступ запрещен: недостаточно прав"
        except IsADirectoryError:
            content = "Невозможно прочитать каталог как файл"
        except UnicodeDecodeError:
            content = (
                "Ошибка кодирования файла: невозможно декодировать содержимое файла"
            )
        except OSError as e:
            content = f"Ошибка ОС: {str(e)}"

    return render(
        request,
        "attack_lab/path_traversal_lab.html",
        {"content": content, "mode": mode},
    )


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
                token, SECRET, algorithms=["HS256"], options={"require": ["exp"]}
            )

    return render(
        request,
        "attack_lab/jwt_lab.html",
        {"token": token, "decoded": decoded, "mode": mode},
    )


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

    return render(
        request, "attack_lab/broken_auth_lab.html", {"message": message, "mode": mode}
    )
