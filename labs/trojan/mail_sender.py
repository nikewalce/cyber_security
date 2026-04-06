import smtplib as smtp
from getpass import getpass
import socket
from requests import get

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
public_ip = get('http://api.ipify.org').text
print(f'Хост: {hostname}')
print(f'Локальный IP: {local_ip}')
print(f'Публичный IP: {public_ip}')

# Почта, с которого будет отправлено письмо
email = 'danil123461@yandex.com'
#Пароль приложения https://id.yandex.ru/security/app-passwords
password = "iicrwbkjhdlfxkmm"

# Почта, на которую отправляем письмо
dest_email = 'nikewalce1@gmail.com'
# Тема письма
subject = 'IP'
# Текст письма
email_text = (f'Host: {hostname}\nLocal IP: {local_ip}\nPublic IP: {public_ip}')
message = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(email, dest_email, subject, email_text)

# Настройка подключения к почтовому сервису
server = smtp.SMTP_SSL('smtp.yandex.ru', 465, timeout=10) # SMTP-сервер Яндекса
server.set_debuglevel(1) # Минимизируем вывод ошибок (выводим только фатальные ошибки)
server.ehlo(email) # Отправляем hello-пакет на сервер
# Если сервер не поддерживает EHLO, можно использовать HELO

server.login(email, password) # Заходим на почту, с которой будем отправлять письмо
server.auth_plain() # Авторизуемся

server.sendmail(email, dest_email, message) # Выводим данные для отправки (адреса свой и получателя и само сообщение)
server.quit() # Отключаемся от сервера