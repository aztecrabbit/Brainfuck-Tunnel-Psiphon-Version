import json
import time
import threading
import subprocess
from .app import *

class client(threading.Thread):
    def __init__(self, command, core, kuota_data_limit):
        super(client, self).__init__()

        self.kuota_data_limit = kuota_data_limit
        self.command = command.format(core=core)
        self.core = core

        self.kuota_data = 0
        self.force_stop = False
        self.connected = False
        self.daemon = True

    def log(self, value, color='[G1]'):
        log('[ core-{} ] {}'.format(self.core, value), color=color)

    def log_replace(self, value, color='[G1]'):
        log_replace('[ core-{} ] {}'.format(self.core, value), color=color)

    def size(self, bytes, suffixes=['B', 'KB', 'MB', 'GB'], i=0):
        while bytes >= 1000 and i < len(suffixes) - 1:
            bytes /= 1000; i += 1

        return '{:.3f} {}'.format(bytes, suffixes[i])

    def reset_kuota_data(self):
        self.kuota_data = 0

    def check_kuota_data(self, received, sent):
        self.kuota_data = self.kuota_data + received + sent

        if self.kuota_data_limit > 0 and self.kuota_data >= self.kuota_data_limit and (received == 0 or (sent == 0 and received <= 20000)):
            return False

        return True

    def run(self):
        self.log('Connecting')
        while True:
            try:
                self.reset_kuota_data()
                process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                for line in process.stdout:
                    line = json.loads(line.decode().strip() + '\r')
                    info = line['noticeType']
                    if info in ['Info', 'Alert']: message = line['data']['message']

                    if info == 'BytesTransferred':
                        if not self.check_kuota_data(line['data']['received'], line['data']['sent']):
                            self.log_replace(self.size(self.kuota_data), color='[R1]')
                            break
                        self.log_replace(self.size(self.kuota_data))

                    elif info == 'ActiveTunnel':
                        self.connected = True
                        self.log('Connected', color='[Y1]')

                    elif info == 'Info':
                        if 'No connection could be made because the target machine actively refused it.' in message or \
                         'Memory metrics at psiphon' in message or \
                         'meek connection is closed' in message or \
                         'meek connection has closed' in message or \
                         'no such host' in message:
                            continue

                    elif info == 'Alert':
                        if 'SOCKS proxy accept error' in message:
                            if not self.connected: break

                        elif 'A connection attempt failed because the connected party did not properly respond after a period of time' in message or \
                         'No connection could be made because the target machine actively refused it.' in message or \
                         'context canceled' in message or \
                         'API request rejected' in message or \
                         'close tunnel ssh error' in message or \
                         'tactics request failed' in message or \
                         'unexpected status code:' in message or \
                         'meek connection is closed' in message or \
                         'meek connection has closed' in message or \
                         'no such host' in message:
                            continue

                        elif 'psiphon.(*Tunnel).sendSshKeepAlive#1295:' in message or \
                         'psiphon.(*Tunnel).SendAPIRequest#342:' in message or \
                         'meek round trip failed' in message or \
                         'meek read payload failed' in message or \
                         'underlying conn is closed' in message or \
                         'tunnel failed:' in message:
                            self.log('Connection closed', color='[R1]')
                            break

                        else: self.log(line, color='[R1]')
            except json.decoder.JSONDecodeError:
                self.force_stop = True
                self.log('Another process is running!', color='[R1]')
            except KeyboardInterrupt:
                pass
            finally:
                if self.force_stop: break
                try:
                    process.kill()
                    self.connected = False
                    time.sleep(2.500)
                    self.log('Reconnecting ({})'.format(self.size(self.kuota_data)))
                except Exception as exception:
                    self.log('Exception: {}'.format(exception), color='[R1]')
                    self.log('Stopped', color='[R1]')
                    break
