from os import system
from .app import *
from .client import *
from .default import *

system('cls')
print(colors('[G1]{}[CC]'.format(open(real_path('/data/banners.txt')).read())))
