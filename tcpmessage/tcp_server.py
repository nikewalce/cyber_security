#для работы с низкоуровневыми протоколами
import socket
#Несколько потоков
import threading

def handle_client(client, addr):
    print("Connected:", addr)
    while True:
        # Прослушиваем и получаем данные по 1 килобайту
        data = client.recv(1024)#можно поставить 4096 байт
        if not data:
            break
        print(f"Connected:{addr}: {data.decode()}")#decode('ascii') - сохраняем байтовые данные и преобразуем их из кодировки ASCII
    # закрываем соединение с клиентом
    client.close()
    print("Disconnected:", addr)

#Создаем место для обмена данными
#SOCK_STREAM - TCP, SOCK_DGRAM - UDP, AF_INET -IPv4
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Резервируем адрес и порт для прослушивания и приема пакетов информации
s.bind(('127.0.0.1', 8888))
#максимум 5 подключений могут ждать в очереди беклога, пока сервер не вызовет accept()
s.listen(5)
print("Server started")

while True:
    # addr - данные об отправителе, client - экземпляр класса socket
    client, addr = s.accept()
    thread = threading.Thread(
        target=handle_client,
        args=(client, addr)
    )
    thread.start()
    # закрываем соединение с сервером
    s.close()

