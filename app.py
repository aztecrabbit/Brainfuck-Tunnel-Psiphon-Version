import os
import app
import time

def main(core = 6):
    for core in range(1, int(core) + 1):
        app.client('data\\psiphon\\tunnel-core-{core}\\psiphon-tunnel-core.exe -config data/psiphon/tunnel-core-{core}/config/psiphon-tunnel-core.json', core).start()

    time.sleep(60*60*24*30)

if __name__ == '__main__':
    main()
