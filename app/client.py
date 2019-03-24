import json
import time
import threading
import subprocess
from .app import *

class client(threading.Thread):
    def __init__(self, command_line, core):
        super(client, self).__init__()

        self.command_line = command_line.format(core=core)
        self.core = core

        self.kuota_data_origin = 4000000
        self.kuota_data = 0
        self.daemon = True

    def log(self, value, color='[G1]'):
        log('[ core-{} ] {}'.format(self.core, value), color=color)

    def reset_kuota_data(self):
        self.kuota_data = self.kuota_data_origin

    def check_kuota_data(self, received, sent):
        self.kuota_data = self.kuota_data - (int(received) + int(sent))

        return self.kuota_data

    def run(self):
        while True:
            try:
                process = subprocess.Popen(self.command_line, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                self.reset_kuota_data()
                self.log('Connecting')
    
                for line in process.stdout:
                    line = json.loads(line.decode().strip() + '\r')
                    info = line['noticeType']
                    if info in ['Info', 'Alert']: message = line.get('data').get('message')

                    if info == 'BytesTransferred':
                        if self.check_kuota_data(line['data']['received'], line['data']['sent']) <= 0: break

                    elif info == 'ActiveTunnel':
                        self.log('Connected', color='[Y1]')

                    elif info == 'Info':
                        if 'No connection could be made because the target machine actively refused it.' in message or \
                         'Memory metrics at psiphon' in message or \
                         'meek connection is closed' in message or \
                         'meek connection has closed' in message or \
                         'no such host' in message:
                            continue

                        # self.log(message, color='[Y2]')

                    elif info == 'Alert':
                        if 'A connection attempt failed because the connected party did not properly respond after a period of time' in message or \
                         'No connection could be made because the target machine actively refused it.' in message or \
                         'context canceled' in message or \
                         'API request rejected' in message or \
                         'unexpected status code:' in message or \
                         'meek connection is closed' in message or \
                         'meek connection has closed' in message or \
                         'no such host' in message:
                            continue

                        elif 'meek read payload failed' in message or \
                         'underlying conn is closed' in message:
                            self.log(line, color='[R1]')
                            continue

                        elif 'SOCKS proxy accept error' in message or \
                         'psiphon.(*Tunnel).SendAPIRequest#342: EOF' in message:
                            # 'meek round trip failed: EOF' in message:
                            break

                        else:
                            self.log(line, color='[R2]')
                            break

            except KeyboardInterrupt:
                pass
            finally:
                process.kill()
                self.log('Disconnected', color='[R1]')
                time.sleep(2.500)
