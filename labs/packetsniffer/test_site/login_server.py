# Импортируем классы для создания HTTP сервера
# BaseHTTPRequestHandler — класс для обработки HTTP запросов
# HTTPServer — сам сервер, который принимает соединения
from http.server import BaseHTTPRequestHandler, HTTPServer
# IP адрес, на котором будет слушать сервер
# 0.0.0.0 означает "слушать на всех сетевых интерфейсах"
# То есть подключиться можно с любого IP
HOST = "0.0.0.0"
# Порт сервера
PORT = 8000
# Класс обработчика HTTP запросов
# Наследуется от BaseHTTPRequestHandler
class LoginHandler(BaseHTTPRequestHandler):
    # Метод вызывается когда приходит HTTP GET запрос
    def do_GET(self):
        # Проверяем путь запроса
        # Если пользователь открыл главную страницу
        if self.path == "/":
            # HTML страница с простой формой логина
            html = """
            <html>
            <body>
            <h2>Login Page</h2>

            <form method="POST" action="/login">
                Username: <input type="text" name="username"><br><br>
                Password: <input type="password" name="password"><br><br>
                <input type="submit" value="Login">
            </form>

            </body>
            </html>
            """
            # Отправляем HTTP статус 200 (OK)
            self.send_response(200)
            # Отправляем заголовок Content-Type
            # браузер поймет что это HTML
            self.send_header("Content-type", "text/html")
            # Завершаем отправку заголовков
            self.end_headers()
            # Отправляем HTML страницу клиенту
            # encode() переводит строку в байты
            self.wfile.write(html.encode())
    # Метод вызывается когда приходит HTTP POST запрос
    def do_POST(self):
        # Проверяем что POST отправлен на /login
        if self.path == "/login":
            # Получаем размер тела запроса
            # Content-Length указывает сколько байт данных отправил клиент
            content_length = int(self.headers["Content-Length"])
            # Читаем тело POST запроса
            # rfile — поток входящих данных
            post_data = self.rfile.read(content_length)
            # Выводим полученные данные в консоль
            print("\n[LOGIN DATA RECEIVED]")
            # decode() преобразует байты в строку
            print(post_data.decode())
            # Ответ сервера
            response = "<h1>Login received</h1>"
            # Отправляем статус OK
            self.send_response(200)
            # Указываем тип ответа
            self.send_header("Content-type", "text/html")
            # Завершаем заголовки
            self.end_headers()
            # Отправляем HTML ответ браузеру
            self.wfile.write(response.encode())
# Создаем HTTP сервер
# (HOST, PORT) — адрес и порт
# LoginHandler — класс обработчик запросов
server = HTTPServer((HOST, PORT), LoginHandler)
# Сообщение в консоль о запуске сервера
print(f"Server running on http://localhost:{PORT}")
# Запускаем сервер
# serve_forever() — сервер работает бесконечно,
# пока программа не будет остановлена
server.serve_forever()
