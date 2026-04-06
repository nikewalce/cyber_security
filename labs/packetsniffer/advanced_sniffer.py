# wrpcap — запись пакетов в файл формата PCAP (его можно открыть в анализаторах трафика)
from scapy.all import sniff, wrpcap
# Импортируем сетевые слои
# IP — IP уровень
# TCP — TCP протокол
# UDP — UDP протокол
from scapy.layers.inet import IP, TCP, UDP
# DNS Query Record — используется для извлечения доменных имен из DNS запросов
from scapy.layers.dns import DNSQR
import time
# Список для хранения всех перехваченных пакетов
# Позже они будут сохранены в PCAP файл
packets = []
# Словарь статистики
# В нем считаем количество разных типов пакетов
stats = {
    "total": 0,  # общее количество пакетов
    "tcp": 0,    # количество TCP пакетов
    "udp": 0,    # количество UDP пакетов
    "dns": 0     # количество DNS запросов
}
# Запоминаем время старта сниффера
start_time = time.time()
# Функция вызывается для каждого перехваченного пакета
def process_packet(packet):
    # Используем глобальную переменную packets
    global packets
    # Увеличиваем общее количество пакетов
    stats["total"] += 1
    # Сохраняем пакет в список
    packets.append(packet)
    # Если пакет содержит TCP слой
    if packet.haslayer(TCP):
        stats["tcp"] += 1
    # Если пакет содержит UDP слой
    if packet.haslayer(UDP):
        stats["udp"] += 1
    # Если пакет содержит DNS запрос
    if packet.haslayer(DNSQR):
        # увеличиваем счетчик DNS
        stats["dns"] += 1
        # извлекаем доменное имя
        domain = packet[DNSQR].qname.decode()
        # выводим домен
        print(f"[DNS] {domain}")
    # Проверяем есть ли IP слой
    if packet.haslayer(IP):
        # IP отправителя
        src = packet[IP].src
        # IP получателя
        dst = packet[IP].dst
        # Если это TCP пакет
        if packet.haslayer(TCP):
            # исходный порт
            sport = packet[TCP].sport
            # порт назначения
            dport = packet[TCP].dport
            # выводим соединение
            print(f"[TCP] {src}:{sport} -> {dst}:{dport}")
        # Если это UDP пакет
        elif packet.haslayer(UDP):
            # исходный порт
            sport = packet[UDP].sport
            # порт назначения
            dport = packet[UDP].dport
            # выводим соединение
            print(f"[UDP] {src}:{sport} -> {dst}:{dport}")
# Функция выводит статистику после остановки сниффера
def show_stats():
    # считаем сколько времени работал сниффер
    duration = time.time() - start_time
    print("\n===== SNIFFER STATS =====")
    # округляем время до 2 знаков
    print("Time:", round(duration, 2), "seconds")
    # выводим статистику
    print("Total packets:", stats["total"])
    print("TCP packets:", stats["tcp"])
    print("UDP packets:", stats["udp"])
    print("DNS queries:", stats["dns"])
try:
    # сообщение о запуске
    print("Sniffer started... Press Ctrl+C to stop\n")
    # запускаем перехват пакетов
    sniff(
        # BPF фильтр
        # перехватываем только TCP и UDP пакеты
        filter="tcp or udp",
        # функция, которая будет вызываться для каждого пакета
        prn=process_packet,
        # не сохраняем пакеты в памяти Scapy
        # мы сами сохраняем их в список packets
        store=False
    )
# перехватываем нажатие Ctrl+C
except KeyboardInterrupt:
    print("\nStopping sniffer...")
    # показываем статистику
    show_stats()
    # сохраняем пакеты в файл
    print("Saving packets to capture.pcap")
    # wrpcap записывает пакеты в PCAP файл
    # этот файл можно открыть в анализаторе трафика
    wrpcap("capture.pcap", packets)
    print("Done.")
