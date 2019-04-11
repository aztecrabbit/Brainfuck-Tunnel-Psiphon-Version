import os
import shutil
from .app import *

def get_file_names():
    return [
        'config/config.json',
        'config/frontend-domains.txt'
    ]

def get_psiphon_file_names():
    return [
        'database/psiphon.boltdb',
        'psiphon-tunnel-core.exe'
    ]

def get_path():
    return '/../storage/psiphon/tunnel-core-{}/'

def reset_default_settings():
    for file_name in get_file_names():
        try:
            os.remove(real_path('/../' + file_name))
        except: pass

    for core in range(10):
        file_names = get_psiphon_file_names()
        file_names.remove('database/psiphon.boltdb')
        file_names.append('database/psiphon.boltdb.lock')
        for file_name in file_names:
            try:
                os.remove(real_path(get_path().format(core) + file_name))
            except: pass

def default_settings():
    for file_name in get_file_names():
        try:
            open(real_path('/../' + file_name))
        except:
            shutil.copyfile(real_path('/default/root/' + file_name), real_path('/../' + file_name))

    for core in range(10):
        for file_name in get_psiphon_file_names():
            try:
                open(real_path(get_path().format(core) + file_name))
            except:
                shutil.copyfile(real_path('/default/' + file_name), real_path(get_path().format(core) + file_name))
