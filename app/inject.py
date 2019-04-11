import socket
import threading
from .app import *
from .domain_fronting import *

class inject(threading.Thread):
    def __init__(self, inject_host, inject_port):
        super(inject, self).__init__()

        self.inject_host = str(inject_host)
        self.inject_port = int(inject_port)

    def log(self, value, color='[G1]'):
        log(value, color=color)

    def run(self):
        try:
            socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_server.bind((self.inject_host, self.inject_port))
            socket_server.listen(2048)
            frontend_domains = open(real_path('/../config/frontend-domains.txt')).readlines()
            frontend_domains = filter_array(frontend_domains)
            if len(frontend_domains) == 0:
                self.log('Frontend Domain not found. Please check config/frontend-domains.txt', color='[R1]')
                self.log('Proxification Rules Psiphon change to Direct', color='[R1]')
                return

            self.log('Domain Fronting running on {} port {}'.format(self.inject_host, self.inject_port))
            while True:
                socket_client, (_, _) = socket_server.accept()
                socket_client.recv(65535)
                domain_fronting(socket_client, frontend_domains).start()
        except Exception as exception:
            self.log('Domain Fronting not running on {} port {}', color='[R1]')
            self.log('Exception: {}'.format(exception))
