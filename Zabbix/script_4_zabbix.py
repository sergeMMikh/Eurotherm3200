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
    match sys.argv[1]:
        case '-pv':
            print(float(ask_server(1)))
        case '-sp':
            print(float(ask_server(2)))
        case '-op':
            print(float(ask_server(4)))
        case '-sprate':
            print(float(ask_server(35)) / 10)
        case _:
            print(f'unknown input: {sys.argv[1]}')
