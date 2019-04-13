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
        array[i] = array[i].strip()
        if array[i].startswith('#'):
            array[i] = ''

    return [x for x in array if x]

def colors(value):
    patterns = {
        'R1' : '\033[31;1m', 'G1' : '\033[32;1m',
        'Y1' : '\033[33;1m', 'P1' : '\033[35;1m',
        'CC' : '\033[0m'
    }

    for code in patterns:
        value = value.replace('[{}]'.format(code), patterns[code])

    return value

def log(value, status='INFO', color='[G1]'):
    value = colors('{color}[{time}] [P1]:: {color}{status} [P1]:: {color}{value}'.format(
        time=datetime.datetime.now().strftime('%H:%M:%S'),
        value=value,
        color=color,
        status=status
    ))
    with lock: print(value)

def log_replace(value, status='INFO', color='[G1]'):
    value = colors('{}{} ({})        \r'.format(color, status, value))
    with lock:
        sys.stdout.write(value)
        sys.stdout.flush()
