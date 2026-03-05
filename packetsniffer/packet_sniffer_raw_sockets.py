import socket  # Работа с сетевыми соединениями
import struct  # Работа с бинарными данными (разбор заголовков пакетов)
# Локальный IP адрес интерфейса, на котором будем слушать пакеты
HOST = "192.168.1.140"
# Создаём raw socket для перехвата IP-пакетов
# AF_INET — IPv4, SOCK_RAW — "сырые" пакеты, IPPROTO_IP — все IP пакеты
sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
# Привязываем сокет к нашему IP и произвольному порту (0)
# Порт не важен, так как ловим все пакеты
sniffer.bind((HOST, 0))
# Включаем получение полного IP заголовка (без этого будет только payload)
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
# Включаем promiscuous mode: интерфейс передаёт все пакеты, не только адресованные нам
# Работает только на Windows; для Linux требуется другой способ
sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
while True:
    # Получаем пакет. Максимальный размер 65565 байт
    # recvfrom возвращает кортеж (data, addr), берём только data
    raw_packet = sniffer.recvfrom(65565)[0]
    # IP заголовок — первые 20 байт пакета (без опций)
    ip_header = raw_packet[:20]
    # Разбираем IP заголовок на отдельные поля
    # Формат: !BBHHHBBH4s4s
    # ! — big-endian (сетевой порядок байтов)
    # B — 1 байт, H — 2 байта, 4s — 4 байта (IP)
    iph = struct.unpack('!BBHHHBBH4s4s', ip_header)
    # Первый байт: версия IP + длина заголовка (IHL)
    version_ihl = iph[0]
    version = version_ihl >> 4       # первые 4 бита — версия (обычно 4)
    ihl = version_ihl & 15           # последние 4 бита — длина заголовка в 32-бит словах
    iph_length = ihl * 4             # длина заголовка в байтах
    ttl = iph[5]                     # TTL — время жизни пакета
    protocol = iph[6]                # Протокол верхнего уровня (TCP=6, UDP=17, ICMP=1)
    src_ip = socket.inet_ntoa(iph[8])  # Преобразуем 4-байтовый IP в читаемый вид
    dst_ip = socket.inet_ntoa(iph[9])
    # Вывод информации о IP пакете
    print("\n==== IP PACKET ====")
    print("Version:", version)
    print("TTL:", ttl)
    print("Protocol:", protocol)
    print("From:", src_ip)
    print("To:", dst_ip)
    # Если протокол TCP
    if protocol == 6:
        # TCP заголовок сразу после IP заголовка, 20 байт (без опций)
        tcp_header = raw_packet[iph_length:iph_length+20]
        # Разбираем TCP заголовок на поля
        # Формат: !HHLLBBHHH
        # H — 2 байта (порт), L — 4 байта (seq/ack), B — 1 байт (offset/reserved + flags)
        tcph = struct.unpack('!HHLLBBHHH', tcp_header)
        src_port = tcph[0]  # исходный порт
        dst_port = tcph[1]  # порт назначения
        flags = tcph[5]     # флаги TCP (1 байт)
        # Выделяем отдельные флаги с помощью побитовой операции
        syn = (flags & 2) >> 1   # SYN — 2-й бит
        ack = (flags & 16) >> 4  # ACK — 5-й бит
        fin = flags & 1           # FIN — 0-й бит
        # Вывод информации о TCP пакете
        print("---- TCP ----")
        print("Source port:", src_port)
        print("Destination port:", dst_port)
        print("SYN:", syn, "ACK:", ack, "FIN:", fin)
