#для работы с низкоуровневыми протоколами
import socket

#Создаем место для обмена данными
#SOCK_STREAM - TCP, SOCK_DGRAM - UDP, AF_INET -IPv4
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#подключаемся к серверу и порту, на котором принимают сообщение
s.connect(('127.0.0.1', 8888))
s.send(b'Message')
s.close()