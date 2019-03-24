import os
import app
from subprocess import Popen

def main():
    try:
        for core in range(6):
            app.client('data\\psiphon\\tunnel-core-{core}\\psiphon-tunnel-core.exe -config data/psiphon/tunnel-core-{core}/config/psiphon-tunnel-core.json', core).start()
        with open(os.devnull, 'w') as devnull:
            process = Popen('data\\http-ping\\http-ping.exe https://global-4-lvs-curry-1.opera-mini.net -t -i 0', stdout=devnull, stderr=devnull)
            process.communicate()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
