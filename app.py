import os
import app
import time
import json
from subprocess import Popen

def real_path(file_name):
    return os.path.dirname(os.path.abspath(__file__)) + file_name

def main():
    try:
        app.default_settings()
        config = json.loads(open(real_path('/config/config.json')).read())
        config_core = config['core']
        config_kuota_data_limit = config['kuota_data_limit']
        config_http_ping_url = config['http_ping_url']
        config_http_ping_timeout = config['http_ping_timeout']
        config_http_ping_interval = config['http_ping_interval']
    except:
        app.log('Config error, please run reset.py first!', color='[R1]')
        return

    try:
        command = 'storage\\psiphon\\tunnel-core-{core}\\psiphon-tunnel-core.exe -config storage/psiphon/tunnel-core-{core}/config/psiphon-tunnel-core.json'
        for core in range(config_core): app.client(command, core, config_kuota_data_limit).start()
        time.sleep(10.000)
        with open(os.devnull, 'w') as devnull:
            process = Popen('storage\\http-ping\\http-ping.exe {} -t -w {} -i {}'.format(config_http_ping_url, config_http_ping_timeout, config_http_ping_interval), stdout=devnull, stderr=devnull)
            process.communicate()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
