#для работы с низкоуровневыми протоколами
import socket

#Создаем место для обмена данными
#SOCK_STREAM - TCP, SOCK_DGRAM - UDP, AF_INET -IPv4
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Резервируем адрес и порт для прослушивания и приема пакетов информации
s.bind(('127.0.0.1', 8888))
#Прослушиваем и получаем данные по 1 килобайту
result = s.recv(1024)
print(result)
print('Message decode:', result.decode('utf-8'))
s.close()