import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
for i in range(1000):
    print(s.connect_ex(('www.google.com', i)))