import os
import shutil
from .app import *

def get_file_names():
    return [
        'database/psiphon.boltdb',
        'database/psiphon.boltdb.lock',
        'psiphon-tunnel-core.exe'
    ]

def reset_to_default_settings():
    for core in range(core = 6):
        for file_name in get_file_names():
            try:
                path = '/../data/psiphon/tunnel-core-{}/'.format(core)
                os.remove(real_path('/../' + file_name))
            except: pass

    default_settings()

def default_settings():
    for core in range(core = 6):
        for file_name in get_file_names():
            try:
                path = '/../data/psiphon/tunnel-core-{}/'.format(core)
                open(real_path(path + file_name))
            except:
                shutil.copyfile(real_path('/default/' + file_name), real_path(path + file_name))
