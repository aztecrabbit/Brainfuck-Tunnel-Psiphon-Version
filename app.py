import app
from os import devnull
from subprocess import Popen

def main():
    try:
        command = 'data\\psiphon\\tunnel-core-{core}\\psiphon-tunnel-core.exe -config data/psiphon/tunnel-core-{core}/config/psiphon-tunnel-core.json'
        app.default_settings()
        for core in range(10):
            app.client(command, core).start()
        with open(devnull, 'w') as null:
            process = Popen('data\\http-ping\\http-ping.exe https://global-4-lvs-curry-1.opera-mini.net -t -i 3', stdout=null, stderr=null)
            process.communicate()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
