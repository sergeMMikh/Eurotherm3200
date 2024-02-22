#!/usr/bin/env python3

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 9000))
sock.sendall('Read'.encode())
print(sock.recv(100))
sock.close()
