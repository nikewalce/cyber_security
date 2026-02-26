#для работы с низкоуровневыми протоколами
import socket

#Создаем место для обмена данными
#SOCK_STREAM - TCP, SOCK_DGRAM - UDP, AF_INET -IPv4
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Резервируем адрес и порт для прослушивания и приема пакетов информации
s.bind(('127.0.0.1', 8888))
#очередь и ограничение на 5 подключений
s.listen(5)
while 1:
    try:
        #addr - данные об отправителе, client - экземпляр класса socket
        client, addr = s.accept()
    #обработчик остановки работы программы с клавиатуры
    except KeyboardInterrupt:
        s.close()
        break
    else:
        # Прослушиваем и получаем данные по 1 килобайту
        result =client.recv(1024)
        print('Message decode:', result.decode('utf-8'))
