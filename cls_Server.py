import socket
import select


# http://theembeddedlab.com/tutorials/simple-socket-server-python/

class SocketServer:
    """ Simple socket server that listens to one single client. """

    def __init__(self, host='0.0.0.0', port=9000):
        """ Initialize the server with a host and port to listen to. """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = host
        self.port = port
        self.sock.bind((host, port))
        self.sock.listen(1)

    def close(self):
        """ Close the server socket. """
        print('Closing server socket (host {}, port {})'.format(self.host, self.port))
        if self.sock:
            self.sock.close()
            self.sock = None

    def run_server(self, M_data):
        """ Accept and handle an incoming connection. """
        print('Starting socket server (host {}, port {})'.format(self.host, self.port))

        SocketServer.client_sock, SocketServer.client_addr = self.sock.accept()

        print('Client {} connected'.format(SocketServer.client_addr))

        stop = False
        while not stop:
            if SocketServer.client_sock:
                # Check if the client is still connected and if data is available:
                try:
                    rdy_read, rdy_write, sock_err = select.select([SocketServer.client_sock, ], [], [])
                except select.error:
                    print('Select() failed on socket with {}'.format(SocketServer.client_addr))
                    return 1

                if len(rdy_read) > 0:
                    read_data = SocketServer.client_sock.recv(255)
                    # Check if socket has been closed
                    if len(read_data) == 0:
                        print('{} closed the socket.'.format(SocketServer.client_addr))
                        stop = True
                    else:
                        print('>>> Received: {}'.format(read_data.rstrip()))
                        if read_data.rstrip() == 'quit':
                            stop = True
                        else:
                            SocketServer.client_sock.send(M_data.encode())
            else:
                print("No client is connected, SocketServer can't receive data")
                stop = True

        # Close socket
        print('Closing connection with {}'.format(SocketServer.client_addr))
        SocketServer.client_sock.close()
        return 0

    def recvServerData(self):
        """ Accept and handle an incoming connection. """
        print('Starting socket server (host {}, port {})'.format(self.host, self.port))

        SocketServer.client_sock, SocketServer.client_addr = self.sock.accept()

        print('Client {} connected'.format(SocketServer.client_addr))

        stop = False
        while not stop:
            if SocketServer.client_sock:
                # Check if the client is still connected and if data is available:
                try:
                    rdy_read, rdy_write, sock_err = select.select([SocketServer.client_sock, ], [], [])
                except select.error:
                    print('Select() failed on socket with {}'.format(SocketServer.client_addr))
                    return 1

                if len(rdy_read) > 0:
                    read_data = SocketServer.client_sock.recv(1024)
                    # Check if socket has been closed
                    if len(read_data) == 0:
                        print('{} closed the socket.'.format(SocketServer.client_addr))
                        stop = True
                    else:
                        print('>>> Received: {}'.format(read_data.rstrip()))
                        stop = True
            else:
                print("No client is connected, SocketServer can't receive data")
                stop = True
                # Close socket
                print('Closing connection with {}'.format(SocketServer.client_addr))
                SocketServer.client_sock.close()

        return read_data

    def sendServerData(self, M_data):
        SocketServer.client_sock.send(M_data.encode())
        # Close socket
        print('Closing connection with {}'.format(SocketServer.client_addr))
        SocketServer.client_sock.close()
        return 0

    def sendStrServerData(self, M_data):
        print('M_data', M_data)
        SocketServer.client_sock.send(M_data.encode())
        # Close socket
        print('Closing connection with {}'.format(SocketServer.client_addr))
        SocketServer.client_sock.close()
        return 0
