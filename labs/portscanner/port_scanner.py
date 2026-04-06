import socket
import threading

def check_port(host, port, timeout=1):
    """
    Проверяет, открыт ли TCP-порт на указанном хосте.

    Args:
        host (str): IP-адрес или доменное имя
        port (int): номер порта
        timeout (float): таймаут в секундах

    Returns:
        bool: True, если порт открыт, иначе False.
    """
    # создаем TCP сокет
    # SOCK_STREAM - TCP, SOCK_DGRAM - UDP, AF_INET -IPv4
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # таймаут на выполнение, чтобы долго не ждать
    sock.settimeout(timeout)
    # пытаемся подключиться
    # connect_ex возвращает:
    # 0 → успех
    # != 0 → ошибка
    result = sock.connect_ex((host, port))
    sock.close()
    if result == 0:
        print(f"Порт {port} на {host} открыт")
    else:
        print(f"Порт {port} на {host} закрыт или недоступен")
    return result == 0

if __name__ == "__main__":
    host = "127.0.0.1"
    ports = [21, 22, 80, 443, 8888]

    threads = []

    for port in range(1, 1024):
        t = threading.Thread(target=check_port, args=(host, port))

        threads.append(t)

        t.start()

    for t in threads:
        t.join()

    # ports = 10_000
    #
    # for port in range(ports):
    #     if check_port(host, port):
    #         print(f"Порт {port} на {host} открыт")
    #     else:
    #         print(f"Порт {port} на {host} закрыт или недоступен")