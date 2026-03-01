import socket

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
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0

if __name__ == "__main__":
    host = "127.0.0.1"
    ports = [21, 22, 80, 443, 8888]

    for port in ports:
        if check_port(host, port):
            print(f"Порт {port} на {host} открыт")
        else:
            print(f"Порт {port} на {host} закрыт или недоступен")