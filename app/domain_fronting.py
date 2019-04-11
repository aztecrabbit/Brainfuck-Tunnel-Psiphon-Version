import random
import socket
import select
import threading
from .app import *

class domain_fronting(threading.Thread):
    def __init__(self, socket_client, frontend_domains):
        super(domain_fronting, self).__init__()

        self.frontend_domains = frontend_domains
        self.socket_tunnel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client = socket_client
        self.buffer_size = 65535
        self.daemon = True

    def log(self, value, status='INFO', color='[G1]'):
        log(value, status=status, color=color)

    def handler(self):
        sockets = [self.socket_tunnel, self.socket_client]
        timeout = 0
        while True:
            timeout += 1
            socket_io, _, errors = select.select(sockets, [], sockets, 3)
            if errors: break
            if socket_io:
                for sock in socket_io:
                    try:
                        data = sock.recv(self.buffer_size)
                        if not data: break
                        # SENT -> RECEIVED
                        elif sock is self.socket_client:
                            self.socket_tunnel.sendall(data)
                        elif sock is self.socket_tunnel:
                            self.socket_client.sendall(data)
                        timeout = 0
                    except: break
            if timeout == 30: break

    def run(self):
        try:
            proxy_host = random.choice(self.frontend_domains)
            proxy_host = proxy_host.strip()

            self.socket_tunnel.connect((proxy_host, 80))
            self.socket_client.sendall(b'HTTP/1.1 200 OK\r\n\r\n')
            self.handler()
            self.socket_client.close()
            self.socket_tunnel.close()
        except Exception as exception:
            self.log('Exception: {}'.format(exception), color='[R1]')
            return
