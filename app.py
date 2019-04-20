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
    except:
        app.log('Config error, please run reset.py first!', color='[R1]')
        return

    app.inject('127.0.0.1', '8080').start()
    time.sleep(1.500)

    try:
        command = 'storage\\psiphon\\{port}\\psiphon-tunnel-core.exe -config storage/psiphon/{port}/config/psiphon-tunnel-core.json'
        for core in range(config_core):
            port = 3080 + core
            app.client(command, port, config_kuota_data_limit).start()
            time.sleep(0.200)
        with open(os.devnull, 'w') as devnull:
            process = Popen('ping.exe 141.0.11.241 -t', stdout=devnull, stderr=devnull)
            process.communicate()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
