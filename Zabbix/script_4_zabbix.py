#!/usr/bin/env python3

import sys
import socket


def ask_server(sell_num: int) -> str:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 9000))
    sock.sendall(f'Get:{sell_num}'.encode())

    message = sock.recv(10)

    sock.close()

    return message.decode()


if __name__ == '__main__':
    if sys.argv[1] == '-pv':
        print(float(ask_server(1)))
    elif sys.argv[1] == '-sp':
        print(float(ask_server(2)))
    elif sys.argv[1] == '-op':
        print(float(ask_server(4))/10)
    elif sys.argv[1] == '-wsp':
        print(float(ask_server(5)))
    elif sys.argv[1] == '-sprate':
        print(float(ask_server(35))/10)
    else:
        print(f'unknown input: {sys.argv[1]}')
