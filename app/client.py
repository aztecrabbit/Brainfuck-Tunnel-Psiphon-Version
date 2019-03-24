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

                    if info == 'BytesTransferred':
                        if self.check_kuota_data(line['data']['received'], line['data']['sent']) <= 0: break

                    elif info == 'ConnectingServer':
                        # self.log('Connecting to {} port {}'.format(line['data']['ipAddress'], line['data']['dialPortNumber']))
                        continue

                    elif info == 'ActiveTunnel':
                        self.log('Connected', color='[Y1]')

                    elif info == 'Info':
                        if 'No connection could be made because the target machine actively refused it.' in line['data']['message'] or \
                         'Memory metrics at psiphon' in line['data']['message'] or \
                         'meek connection is closed' in line['data']['message'] or \
                         'meek connection has closed' in line['data']['message'] or \
                         'no such host' in line['data']['message']:
                            continue

                        # self.log(line['data']['message'], color='[Y2]')

                    elif info == 'Alert':
                        if 'A connection attempt failed because the connected party did not properly respond after a period of time' in line['data']['message'] or \
                         'No connection could be made because the target machine actively refused it.' in line['data']['message'] or \
                         'context canceled' in line['data']['message'] or \
                         'API request rejected' in line['data']['message'] or \
                         'unexpected status code:' in line['data']['message'] or \
                         'SOCKS proxy accept error' in line['data']['message'] or \
                         'meek connection is closed' in line['data']['message'] or \
                         'meek connection has closed' in line['data']['message'] or \
                         'no such host' in line['data']['message']:
                            continue

                        self.log(line['data']['message'], color='[R2]')

                    elif info == 'BuildInfo' or \
                     info == 'ListeningSocksProxyPort' or \
                     info == 'ListeningHttpProxyPort' or \
                     info == 'NetworkID' or \
                     info == 'CandidateServers' or \
                     info == 'SessionId' or \
                     info == 'AvailableEgressRegions' or \
                     info == 'ConnectedServer' or \
                     info == 'ClientRegion' or \
                     info == 'Homepage' or \
                     info == 'ServerTimestamp' or \
                     info == 'ActiveAuthorizationIDs' or \
                     info == 'Tunnels' or \
                     info == 'ClientUpgradeAvailable' or \
                     info == 'LocalProxyError' or \
                     info == 'TotalBytesTransferred':
                        continue
            except KeyboardInterrupt:
                pass
            finally:
                process.kill()
                self.log('Disconnected', color='[R1]')
                time.sleep(2.500)
