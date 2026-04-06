from scapy.all import *
from scapy.layers.inet import ICMP

# просмотр своих сетевых интерфейсов
print(get_if_list())
"""
Когда приходит пакет:
[Сетевая карта / Loopback]
        ↓
[Драйвер Npcap (копия пакета)]
        ↓
[TCP/IP стек Windows]
        ↓
[ICMP обработка]
"""

# Эта функция вызывается КАЖДЫЙ РАЗ,
# когда драйвер сетевой карты передает пакет в Scapy
def handle_packets(packet):

    # Проверяем: есть ли внутри пакета уровень ICMP
    # packet — разобранная структура: [Loopback][IP][ICMP][Payload]
    if packet.haslayer(ICMP):

        print(f"""
        [ICMP]

        # IP.src — это поле Source Address (адрес отправителя) из IP-заголовка
        # На уровне железа это просто 32-битное число (IPv4)
        Src: {packet[IP].src}

        # IP.dst — Destination Address (адрес получателя)
        Dst: {packet[IP].dst}

        # len(packet) — полный размер пакета в байтах
        # включая ВСЕ уровни:
        # Loopback header + IP header + ICMP header + payload
        Size: {len(packet)}

        # packet — строковое представление:
        # Scapy показывает, как он "распарсил" сырые байты
        Packet: {packet}
        """)

# sniff — это обертка над pcap (через Npcap на Windows)
sniff(
    filter="icmp",  # BPF фильтр (применяется на уровне драйвера!)
    prn=handle_packets,  # callback функция
    iface="\\Device\\NPF_Loopback"  # интерфейс (виртуальный loopback)
)