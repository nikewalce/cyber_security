# Cyber Security Learning Project

Учебный репозиторий для практики в кибербезопасности: offensive-подходы, сетевые инструменты и безопасная веб-разработка на Django.

> ⚠️ **Важно:** все примеры, скрипты и лаборатории в репозитории предназначены только для обучения и работы в контролируемой среде.

---

## О проекте

Этот проект объединяет два направления:

1. **Практика security-инструментов на Python** (сканеры, sniffer'ы, shell-сценарии, TCP/UDP эксперименты).
2. **Django-платформа** для изучения уязвимостей, демонстрации атак и их исправления.

Цель — изучать кибербезопасность через код, от низкоуровневых сетевых сценариев до web security.

---

## Что уже реализовано

### 1) Реализован набор лабораторных Python-инструментов (`labs/`)

В проекте уже есть отдельные рабочие модули для изучения сетей и атакующих техник:

- **Port Scanner** (`labs/portscanner/port_scanner.py`) — сканирование TCP-портов.
- **TCP/UDP messaging labs** (`labs/tcpmessage`, `labs/udpmessage`) — клиент-серверные эксперименты с сокетами.
- **Packet Sniffer** (`labs/packetsniffer`) — анализ HTTP/DNS и raw sockets.
- **Ping of Death lab** (`labs/ping_of_death`) — учебная демонстрация низкоуровневых сетевых сценариев.
- **Reverse Shell** (`labs/reverseshell`) — клиент/сервер и отдельный инсталлятор.
- **Trojan-related practice scripts** (`labs/trojan`) — вспомогательные учебные скрипты.

Это покрывает базовые навыки по TCP/UDP, разбору трафика, удалённому взаимодействию и построению простых security PoC.

### 2) Поднят Django-проект с модулями по кибербезопасности (`cyber_security_site/`)

Собран много-модульный сайт на Django, в котором уже созданы приложения:

- `main` — базовые страницы и новости;
- `accounts` — пользовательский блок;
- `attack_lab` — практические веб-лаборатории;
- `knowledge_base` — база знаний;
- `security_tools` — каталог/страницы инструментов;
- `logs_analysis` — раздел анализа логов;
- `roadmap` — roadmap развития в кибербезопасности;
- `ctf_writeups` — CTF-заметки;
- `dashboard` — сводная панель;
- `api` — API-слой.

Для приложений уже созданы миграции, шаблоны, urls, views и наборы тестов по структуре проекта.

### 3) Добавлены учебные веб-лаборатории уязвимостей

В `attack_lab/templates/attack_lab/` уже подготовлены страницы для тем:

- XSS (несколько вариантов);
- SQLi;
- CSRF;
- IDOR;
- Path Traversal;
- SSRF;
- небезопасная загрузка файлов;
- JWT/аутентификация и смежные сценарии.

Это формирует базу для безопасного воспроизведения и разбора типовых веб-уязвимостей.

### 4) Подготовлена тестовая инфраструктура

Для большинства приложений есть каркас тестов в `tests/` (views/forms/models/utils), а также настройки `pytest` внутри Django-части (`cyber_security_site/pytest.ini`, `cyber_security_site/conftest.py`).

### 5) Настроена Python-экосистема проекта

На уровне репозитория добавлены:

- `pyproject.toml`
- `requirements.txt`
- `poetry.lock`

То есть проект можно использовать как с `pip`, так и через `poetry`.

---

## Архитектура

```text
cyber_security
├── labs/                    # отдельные практические скрипты и PoC
├── cyber_security_site/     # Django-платформа
├── main.py
├── test.py
├── pyproject.toml
├── requirements.txt
└── README.md
```
---

## Технологии

- Python
- Django
- Django REST Framework
- PostgreSQL
- HTML / CSS / JavaScript
- pytest
- Poetry
- ruff / flake8 / black / isort

---

## Запуск Django-платформы

### 1. Клонирование

```bash
git clone https://github.com/nikewalce/cyber_security.git
cd cyber_security
```

### 2. Установка зависимостей

Вариант через requirements:

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

Или через Poetry:

```bash
poetry install
poetry shell
```

### 3. Переменные окружения

Создайте `.env` (пример):

```env
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=cyber_security
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=127.0.0.1
DB_PORT=5432
```

### 4. Миграции и запуск

```bash
cd cyber_security_site
python manage.py migrate
python manage.py runserver
```

Сайт будет доступен по адресу:

- `http://127.0.0.1:8000/`

---

## Тесты

Пример базового запуска:

```bash
pytest -q
```

Также в проекте есть smoke-подход для URL (проверка доступности маршрутов) и app-level тесты в каждом приложении.

---

## Что это мне дало (результаты обучения)

В рамках проекта я:

- разобрался с базовыми классами web-уязвимостей (XSS, SQLi, CSRF, IDOR, SSRF и др.);
- потренировался писать и анализировать сетевые инструменты;
- научился строить многомодульный Django-проект;
- начал выстраивать тестирование и структуру кода как в реальных проектах.

---

## Планы развития

- Разделить безопасную платформу и учебные offensive-скрипты по слоям/пакетам.
- Углубить тестирование security-сценариев (payload matrix, regression-набор).
- Развивать `api` и добавить контрактные тесты.
- Добавить CI-пайплайн (lint + tests + security checks).
- Развивать модуль `logs_analysis` и визуализацию событий.

---

## Disclaimer

Этот репозиторий создан исключительно для обучения.

Не используйте код и техники против систем, на которые у вас нет официального разрешения.