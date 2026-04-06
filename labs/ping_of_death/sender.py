from scapy.all import *

"""
Ping работает через протокол:

ICMP (Echo Request / Echo Reply)

Структура:

[IP Header][ICMP Header][Payload]
"""

payload = "A" * 600000  # создаем 60000 байт данных

# Создаем IP пакет
packet_small = IP(dst="127.0.0.1")/ICMP()

# Что происходит:
# IP() — создаёт IP заголовок
# ICMP() — создаёт ICMP Echo Request
# / — оператор "инкапсуляции"
# (как вложенные структуры в сети)

# Большой пакет
#packet_big = IP(src="185.215.4.19", dst="192.168.56.1")/ICMP()/payload #spoofing подмена своего адреса отправителя на чужой
packet_big = IP(dst="127.0.0.1")/ICMP()/payload

# разбиваем пакеты по частям, чтобы большой пакет отправить полностью
fragments = fragment(packet_big, fragsize=1480)
# смотрим размер фрагментов, проверяем, что он реально разбил пакеты и на какое кол-во
print(len(fragments))
for f in fragments:
    send(f)

print(packet_small)
print(packet_big)

# send() — отправка через raw socket
send(packet_small)
#send(packet_big)
