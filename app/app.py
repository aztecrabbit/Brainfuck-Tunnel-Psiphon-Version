import os
import sys
import colorama
import datetime
from threading import RLock

lock = RLock(); colorama.init()

def real_path(file_name):
    return os.path.dirname(os.path.abspath(__file__)) + file_name

def filter_array(array):
    for i in range(len(array)):
        if array[i].startswith('#'):
            array[i] = ''

    return [x for x in array if x]

def colors(value):
    patterns = {
        'CC' : '\033[0m',    'BB' : '\033[1m',
        'D1' : '\033[30;1m', 'D2' : '\033[30;2m',
        'R1' : '\033[31;1m', 'R2' : '\033[31;2m',
        'G1' : '\033[32;1m', 'G2' : '\033[32;2m',
        'Y1' : '\033[33;1m', 'Y2' : '\033[33;2m',
        'B1' : '\033[34;1m', 'B2' : '\033[34;2m',
        'P1' : '\033[35;1m', 'P2' : '\033[35;2m',
        'C1' : '\033[36;1m', 'C2' : '\033[36;2m',
        'W1' : '\033[37;1m', 'W2' : '\033[37;2m'
    }

    for code in patterns:
        value = value.replace('[{}]'.format(code), patterns[code])

    return value

def log(value, status='INFO', color='[G1]'):
    with lock:
        print(colors('{color}[{time}] [P1]:: {color}{status} [P1]:: {color}{value}{endline}'.format(
            time=datetime.datetime.now().strftime('%H:%M:%S'),
            value=value,
            color=color,
            status=status,
            endline='            '
        )))

def log_replace(value, status='INFO', color='[G1]'):
    with lock:
        sys.stdout.write(colors('{}{} ({})        \r'.format(color, status, value)))
        sys.stdout.flush()
