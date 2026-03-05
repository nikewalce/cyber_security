# Импортируем функцию sniff из библиотеки Scapy
# sniff используется для перехвата сетевых пакетов
from scapy.all import sniff
# Импортируем слой HTTPRequest
# Он позволяет распознавать HTTP запросы внутри TCP пакетов
from scapy.layers.http import HTTPRequest
# Импортируем слой DNS Query Record
# Используется для извлечения доменных имен из DNS запросов
from scapy.layers.dns import DNSQR
# Импортируем IP слой
# Позволяет получать IP адрес источника и назначения
from scapy.layers.inet import IP
# Эта функция будет вызываться для КАЖДОГО перехваченного пакета
def process_packet(packet):
    # ===== ЛОГ ВСЕХ IP СОЕДИНЕНИЙ =====
    # Проверяем есть ли в пакете IP слой
    if packet.haslayer(IP):
        # packet[IP].src — IP адрес отправителя
        # packet[IP].dst — IP адрес получателя
        print(
            f"{packet[IP].src} -> {packet[IP].dst}"
        )
    # ===== DNS =====
    # Проверяем является ли пакет DNS запросом
    if packet.haslayer(DNSQR):
        # DNSQR.qname содержит доменное имя
        # decode() переводит байты в обычную строку
        domain = packet[DNSQR].qname.decode()
        print("\n[DNS REQUEST]")
        print("Domain:", domain)
    # ===== HTTP =====
    # Проверяем содержит ли пакет HTTP запрос
    if packet.haslayer(HTTPRequest):
        # Получаем IP слой пакета
        ip_layer = packet[IP]
        # Host — домен сайта
        host = packet[HTTPRequest].Host.decode()
        # Path — путь к странице
        path = packet[HTTPRequest].Path.decode()
        # Формируем полный URL
        url = "http://" + host + path
        print("\n[HTTP REQUEST]")
        print("Source:", ip_layer.src)        # IP клиента
        print("Destination:", ip_layer.dst)   # IP сервера
        print("URL:", url)                    # полный URL
        # Проверяем есть ли заголовок User-Agent
        # Он содержит информацию о браузере пользователя
        if packet[HTTPRequest].User_Agent:
            # Преобразуем байты в строку
            user_agent = packet[HTTPRequest].User_Agent.decode()
            print("User-Agent:", user_agent)
# Сообщение о запуске сниффера
print("Sniffer started...\n")
# Запускаем перехват пакетов
sniff(
    # BPF фильтр (Berkeley Packet Filter)
    # tcp port 80 — HTTP трафик
    # udp port 53 — DNS трафик
    filter="tcp port 80 or udp port 53",
    # prn — функция которая вызывается для каждого пакета
    prn=process_packet,
    # store=False — не сохранять пакеты в память
    # это важно, иначе память быстро заполнится
    store=False
)
